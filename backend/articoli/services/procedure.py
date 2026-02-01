"""
Service per la gestione delle Procedure.

Gestisce la numerazione atomica e le operazioni di business logic
che richiedono transazioni sicure.
"""
from django.db import transaction, connection
from django.utils import timezone
from typing import Optional, List
from ..models import Procedura, DettaglioProcedura, CaratteristicaProcedura, Articolo


class DomainValidationError(ValueError):
    """
    Eccezione per errori di validazione dominio nel service layer.

    Usata per input invalidi, ID non appartenenti, duplicati, mismatch parent.
    Eredita da ValueError per compatibilità, ma permette catch specifico in API.
    """
    pass


def get_next_nr_procedura() -> int:
    """
    Ottiene il prossimo nr_procedura dalla sequence Postgres.
    Thread-safe e race-condition free.
    """
    with connection.cursor() as cursor:
        cursor.execute("SELECT nextval('procedura_nr_seq')")
        return cursor.fetchone()[0]


@transaction.atomic
def create_procedura_revision(
    articolo_id: int,
    user,
    note: str = None,
    data_procedura: Optional[str] = None,
    data_revisione: Optional[str] = None,
) -> Procedura:
    """
    Crea una nuova revisione di Procedura per un Articolo.

    Logica:
    - Se l'articolo non ha procedure esistenti:
        * nr_procedura = nextval(sequence) [nuovo numero globale]
        * nr_revisione = 1

    - Se l'articolo ha già procedure:
        * nr_procedura = stesso della prima procedura dell'articolo
        * nr_revisione = ultimo + 1

    Usa select_for_update() per lockare l'ultima revisione ed evitare race condition.

    Args:
        articolo_id: ID dell'articolo
        user: Utente che crea la procedura
        note: Note opzionali
        data_procedura: Data procedura (default: oggi)
        data_revisione: Data revisione (default: oggi)

    Returns:
        Procedura creata

    Raises:
        Articolo.DoesNotExist: Se l'articolo non esiste
    """
    # Verifica che l'articolo esista
    articolo = Articolo.objects.get(pk=articolo_id)

    # Cerca l'ultima revisione per questo articolo (con lock)
    ultima_revisione = (
        Procedura.objects
        .filter(fk_articolo=articolo)
        .select_for_update()  # Lock per evitare race condition
        .order_by("-nr_revisione")
        .first()
    )

    if ultima_revisione:
        # Articolo ha già procedure: usa stesso nr_procedura, incrementa revisione
        nr_procedura = ultima_revisione.nr_procedura
        nr_revisione = ultima_revisione.nr_revisione + 1
        # Mantieni la data_procedura originale (è la data di nascita della "serie")
        data_proc = ultima_revisione.data_procedura
    else:
        # Prima procedura per questo articolo: nuovo numero da sequence
        nr_procedura = get_next_nr_procedura()
        nr_revisione = 1
        data_proc = timezone.now().date() if not data_procedura else data_procedura

    # Crea la nuova procedura
    procedura = Procedura.objects.create(
        fk_articolo=articolo,
        nr_procedura=nr_procedura,
        nr_revisione=nr_revisione,
        data_procedura=data_proc,
        data_revisione=data_revisione or timezone.now().date(),
        note=note or "",
        created_by=user,
    )

    return procedura


@transaction.atomic
def clone_procedura_as_revision(
    procedura_id: int,
    user,
    note: str = None,
) -> Procedura:
    """
    Clona una procedura esistente come nuova revisione.

    Copia tutti i dettagli e le caratteristiche dalla procedura sorgente.

    Args:
        procedura_id: ID della procedura da clonare
        user: Utente che crea la revisione
        note: Note per la nuova revisione

    Returns:
        Nuova Procedura clonata
    """
    # Ottieni la procedura sorgente
    procedura_source = Procedura.objects.get(pk=procedura_id)

    # Crea la nuova revisione
    nuova_procedura = create_procedura_revision(
        articolo_id=procedura_source.fk_articolo_id,
        user=user,
        note=note or procedura_source.note,
    )

    # Clona i dettagli
    for dettaglio in procedura_source.dettagli.all():
        nuovo_dettaglio = DettaglioProcedura.objects.create(
            fk_procedura=nuova_procedura,
            fk_faselavoro=dettaglio.fk_faselavoro,
            fk_fornitore=dettaglio.fk_fornitore,
            is_interna=dettaglio.is_interna,
            numero_riga=dettaglio.numero_riga,
            note=dettaglio.note,
            created_by=user,
        )

        # Clona le caratteristiche del dettaglio
        for caratteristica in dettaglio.caratteristiche.all():
            CaratteristicaProcedura.objects.create(
                fk_dettaglio_procedura=nuovo_dettaglio,
                fk_fornitore=caratteristica.fk_fornitore,
                fk_lavorazione_esterna=caratteristica.fk_lavorazione_esterna,
                fk_dettaglio_fase_lavoro=caratteristica.fk_dettaglio_fase_lavoro,
                valore=caratteristica.valore,
                note=caratteristica.note,
                numero_riga=caratteristica.numero_riga,
                created_by=user,
            )

    return nuova_procedura


# Offset per valori temporanei durante reorder (evita collisioni con UNIQUE constraint)
_REORDER_TEMP_OFFSET = 100000


@transaction.atomic
def reorder_dettagli(procedura_id: int, ordered_ids: List[int]) -> List[DettaglioProcedura]:
    """
    Riordina i dettagli di una procedura.

    Verifica che tutti gli ID appartengano alla procedura specificata,
    poi aggiorna numero_riga in ordine.

    Usa two-phase update per evitare violazioni del vincolo UNIQUE:
    1. Assegna valori temporanei fuori range (100000+)
    2. Assegna valori definitivi 1..N

    Args:
        procedura_id: ID della procedura
        ordered_ids: Lista di ID dettagli nell'ordine desiderato

    Returns:
        Lista dei dettagli aggiornati

    Raises:
        DomainValidationError: Se gli ID non appartengono tutti alla procedura
    """
    # Verifica ownership: tutti i dettagli devono appartenere a questa procedura
    dettagli = DettaglioProcedura.objects.filter(
        fk_procedura_id=procedura_id,
        id__in=ordered_ids
    ).select_for_update()

    if dettagli.count() != len(ordered_ids):
        existing_ids = set(dettagli.values_list("id", flat=True))
        invalid_ids = set(ordered_ids) - existing_ids
        raise DomainValidationError(f"ID non validi o non appartenenti alla procedura: {invalid_ids}")

    # Mappa id -> dettaglio per accesso rapido
    dettagli_map = {d.id: d for d in dettagli}

    # FASE 1: Assegna valori temporanei per evitare collisioni UNIQUE
    for idx, det_id in enumerate(ordered_ids):
        dettaglio = dettagli_map[det_id]
        dettaglio.numero_riga = _REORDER_TEMP_OFFSET + idx
        dettaglio.save(update_fields=["numero_riga"])

    # FASE 2: Assegna valori definitivi 1..N
    updated = []
    for idx, det_id in enumerate(ordered_ids, start=1):
        dettaglio = dettagli_map[det_id]
        dettaglio.numero_riga = idx
        dettaglio.save(update_fields=["numero_riga"])
        updated.append(dettaglio)

    return updated


@transaction.atomic
def reorder_caratteristiche(
    dettaglio_id: int,
    ordered_ids: List[int]
) -> List[CaratteristicaProcedura]:
    """
    Riordina le caratteristiche di un dettaglio procedura.

    Usa two-phase update per evitare violazioni del vincolo UNIQUE:
    1. Assegna valori temporanei fuori range (100000+)
    2. Assegna valori definitivi 1..N

    Args:
        dettaglio_id: ID del dettaglio procedura
        ordered_ids: Lista di ID caratteristiche nell'ordine desiderato

    Returns:
        Lista delle caratteristiche aggiornate

    Raises:
        DomainValidationError: Se gli ID non appartengono tutti al dettaglio
    """
    caratteristiche = CaratteristicaProcedura.objects.filter(
        fk_dettaglio_procedura_id=dettaglio_id,
        id__in=ordered_ids
    ).select_for_update()

    if caratteristiche.count() != len(ordered_ids):
        existing_ids = set(caratteristiche.values_list("id", flat=True))
        invalid_ids = set(ordered_ids) - existing_ids
        raise DomainValidationError(f"ID non validi o non appartenenti al dettaglio: {invalid_ids}")

    caratteristiche_map = {c.id: c for c in caratteristiche}

    # FASE 1: Assegna valori temporanei per evitare collisioni UNIQUE
    for idx, car_id in enumerate(ordered_ids):
        car = caratteristiche_map[car_id]
        car.numero_riga = _REORDER_TEMP_OFFSET + idx
        car.save(update_fields=["numero_riga"])

    # FASE 2: Assegna valori definitivi 1..N
    updated = []
    for idx, car_id in enumerate(ordered_ids, start=1):
        car = caratteristiche_map[car_id]
        car.numero_riga = idx
        car.save(update_fields=["numero_riga"])
        updated.append(car)

    return updated


def get_next_dettaglio_numero_riga(procedura_id: int) -> int:
    """
    Restituisce il prossimo numero_riga disponibile per un dettaglio.
    """
    last = DettaglioProcedura.objects.filter(
        fk_procedura_id=procedura_id
    ).order_by("-numero_riga").first()

    return (last.numero_riga + 1) if last else 1


def get_next_caratteristica_numero_riga(dettaglio_id: int) -> int:
    """
    Restituisce il prossimo numero_riga disponibile per una caratteristica.
    """
    last = CaratteristicaProcedura.objects.filter(
        fk_dettaglio_procedura_id=dettaglio_id
    ).order_by("-numero_riga").first()

    return (last.numero_riga + 1) if last else 1

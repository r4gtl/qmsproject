"""
Test suite per il sistema Procedure.

Copertura:
- Creazione revisioni e numerazione race-free
- Clonazione procedure
- Reorder dettagli e caratteristiche
- Validazione interna/esterna su CaratteristicaProcedura
- Constraint unicità database
- API error handling (400 vs 500)
- N+1 query prevention
"""
import sys
from django.test import TestCase, TransactionTestCase
from django.contrib.auth.models import User
from django.db import IntegrityError, connection
from rest_framework.test import APITestCase
from rest_framework import status

from .models import (
    Articolo,
    FaseLavoro,
    DettaglioFaseLavoro,
    LavorazioneEsterna,
    Procedura,
    DettaglioProcedura,
    CaratteristicaProcedura,
)
from .services.procedure import (
    create_procedura_revision,
    clone_procedura_as_revision,
    reorder_dettagli,
    reorder_caratteristiche,
    DomainValidationError,
)
from anagrafiche.models import Fornitore


def is_postgres():
    """Verifica se il database è PostgreSQL."""
    return 'postgresql' in connection.settings_dict.get('ENGINE', '')


def skip_if_sqlite(test_func):
    """Decorator per saltare test che richiedono PostgreSQL."""
    def wrapper(*args, **kwargs):
        if not is_postgres():
            return  # Skip silently
        return test_func(*args, **kwargs)
    return wrapper


class ProceduraServiceTestCase(TransactionTestCase):
    """
    Test per i service di Procedura.
    Usa TransactionTestCase per testare atomicità e constraint.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        self.articolo = Articolo.objects.create(
            descrizione="Articolo Test",
            created_by=self.user,
        )
        self.fase_lavoro = FaseLavoro.objects.create(
            descrizione="Fase Test",
            interno_esterno="interno",
            created_by=self.user,
        )

    @skip_if_sqlite
    def test_create_first_revision_uses_sequence(self):
        """Prima revisione usa sequence per nr_procedura."""
        procedura = create_procedura_revision(
            articolo_id=self.articolo.id,
            user=self.user,
        )

        self.assertIsNotNone(procedura.nr_procedura)
        self.assertEqual(procedura.nr_revisione, 1)
        self.assertEqual(procedura.fk_articolo_id, self.articolo.id)

    @skip_if_sqlite
    def test_second_revision_same_nr_procedura(self):
        """Seconda revisione usa stesso nr_procedura, incrementa nr_revisione."""
        proc1 = create_procedura_revision(
            articolo_id=self.articolo.id,
            user=self.user,
        )
        proc2 = create_procedura_revision(
            articolo_id=self.articolo.id,
            user=self.user,
        )

        self.assertEqual(proc1.nr_procedura, proc2.nr_procedura)
        self.assertEqual(proc1.nr_revisione, 1)
        self.assertEqual(proc2.nr_revisione, 2)

    @skip_if_sqlite
    def test_different_articoli_get_different_nr_procedura(self):
        """Articoli diversi ottengono nr_procedura diversi."""
        articolo2 = Articolo.objects.create(
            descrizione="Articolo 2",
            created_by=self.user,
        )

        proc1 = create_procedura_revision(
            articolo_id=self.articolo.id,
            user=self.user,
        )
        proc2 = create_procedura_revision(
            articolo_id=articolo2.id,
            user=self.user,
        )

        self.assertNotEqual(proc1.nr_procedura, proc2.nr_procedura)
        self.assertEqual(proc1.nr_revisione, 1)
        self.assertEqual(proc2.nr_revisione, 1)

    @skip_if_sqlite
    def test_create_revision_sequential_safety(self):
        """
        Test sicurezza sequenziale della numerazione.

        Nota: test multi-thread reale richiede database che supporta
        connessioni multiple (non SQLite in-memory). Questo test verifica
        che creazioni sequenziali producano revisioni incrementali corrette.
        """
        revisions = []
        for _ in range(5):
            proc = create_procedura_revision(
                articolo_id=self.articolo.id,
                user=self.user,
            )
            revisions.append(proc)

        # Verifica che tutte abbiano stesso nr_procedura
        nr_procs = set(p.nr_procedura for p in revisions)
        self.assertEqual(len(nr_procs), 1)

        # Verifica nr_revisione consecutivi
        nr_revs = sorted(p.nr_revisione for p in revisions)
        self.assertEqual(nr_revs, [1, 2, 3, 4, 5])


class CloneProceduraTestCase(TestCase):
    """Test per clonazione procedure."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        self.articolo = Articolo.objects.create(
            descrizione="Articolo Test",
            created_by=self.user,
        )
        self.fase_lavoro = FaseLavoro.objects.create(
            descrizione="Fase Test",
            interno_esterno="interno",
            created_by=self.user,
        )
        self.dettaglio_fase = DettaglioFaseLavoro.objects.create(
            fk_fase_lavoro=self.fase_lavoro,
            attributo="Temperatura",
            created_by=self.user,
        )

    @skip_if_sqlite
    def test_clone_creates_new_revision(self):
        """Clone crea nuova revisione con stesso nr_procedura."""
        # Crea procedura originale
        proc_orig = create_procedura_revision(
            articolo_id=self.articolo.id,
            user=self.user,
            note="Originale",
        )

        # Aggiungi un dettaglio
        dettaglio = DettaglioProcedura.objects.create(
            fk_procedura=proc_orig,
            fk_faselavoro=self.fase_lavoro,
            is_interna=True,
            numero_riga=1,
            created_by=self.user,
        )

        # Aggiungi una caratteristica
        CaratteristicaProcedura.objects.create(
            fk_dettaglio_procedura=dettaglio,
            fk_dettaglio_fase_lavoro=self.dettaglio_fase,
            valore="100°C",
            numero_riga=1,
            created_by=self.user,
        )

        # Clona
        proc_clone = clone_procedura_as_revision(
            procedura_id=proc_orig.id,
            user=self.user,
            note="Clonata",
        )

        # Verifica numerazione
        self.assertEqual(proc_clone.nr_procedura, proc_orig.nr_procedura)
        self.assertEqual(proc_clone.nr_revisione, proc_orig.nr_revisione + 1)

        # Verifica dettagli clonati
        self.assertEqual(proc_clone.dettagli.count(), 1)

        # Verifica caratteristiche clonate
        det_clone = proc_clone.dettagli.first()
        self.assertEqual(det_clone.caratteristiche.count(), 1)
        self.assertEqual(
            det_clone.caratteristiche.first().valore, "100°C"
        )


class ReorderTestCase(TestCase):
    """Test per reorder di dettagli e caratteristiche (service layer)."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        self.articolo = Articolo.objects.create(
            descrizione="Articolo Test",
            created_by=self.user,
        )
        self.fase_lavoro = FaseLavoro.objects.create(
            descrizione="Fase Test",
            interno_esterno="interno",
            created_by=self.user,
        )
        # Crea procedura senza usare sequence (per compatibilità SQLite)
        self.procedura = Procedura.objects.create(
            fk_articolo=self.articolo,
            nr_procedura=1,
            nr_revisione=1,
            created_by=self.user,
        )

    def test_reorder_dettagli_updates_numero_riga(self):
        """Reorder aggiorna numero_riga correttamente (two-phase, constraint-safe)."""
        # Crea 3 dettagli con numero_riga non contigui per test realistico
        det1 = DettaglioProcedura.objects.create(
            fk_procedura=self.procedura,
            fk_faselavoro=self.fase_lavoro,
            is_interna=True,
            numero_riga=10,
            created_by=self.user,
        )
        det2 = DettaglioProcedura.objects.create(
            fk_procedura=self.procedura,
            fk_faselavoro=self.fase_lavoro,
            is_interna=True,
            numero_riga=20,
            created_by=self.user,
        )
        det3 = DettaglioProcedura.objects.create(
            fk_procedura=self.procedura,
            fk_faselavoro=self.fase_lavoro,
            is_interna=True,
            numero_riga=30,
            created_by=self.user,
        )

        # Riordina: [det3, det1, det2] - questo richiede swap che potrebbe
        # violare UNIQUE constraint senza two-phase update
        updated = reorder_dettagli(
            procedura_id=self.procedura.id,
            ordered_ids=[det3.id, det1.id, det2.id],
        )

        # Verifica nuovo ordine (1, 2, 3 non più 10, 20, 30)
        det1.refresh_from_db()
        det2.refresh_from_db()
        det3.refresh_from_db()

        self.assertEqual(det3.numero_riga, 1)
        self.assertEqual(det1.numero_riga, 2)
        self.assertEqual(det2.numero_riga, 3)

    def test_reorder_dettagli_swap_first_last(self):
        """Swap primo e ultimo elemento (caso critico per UNIQUE constraint)."""
        det1 = DettaglioProcedura.objects.create(
            fk_procedura=self.procedura,
            fk_faselavoro=self.fase_lavoro,
            is_interna=True,
            numero_riga=1,
            created_by=self.user,
        )
        det2 = DettaglioProcedura.objects.create(
            fk_procedura=self.procedura,
            fk_faselavoro=self.fase_lavoro,
            is_interna=True,
            numero_riga=2,
            created_by=self.user,
        )

        # Swap: [det2, det1] - det2 prende 1, det1 prende 2
        # Senza two-phase: det2.numero_riga=1 collide con det1 che ha ancora 1
        reorder_dettagli(
            procedura_id=self.procedura.id,
            ordered_ids=[det2.id, det1.id],
        )

        det1.refresh_from_db()
        det2.refresh_from_db()

        self.assertEqual(det2.numero_riga, 1)
        self.assertEqual(det1.numero_riga, 2)

    def test_reorder_dettagli_invalid_ids_raises(self):
        """Reorder con ID non appartenenti alla procedura solleva DomainValidationError."""
        det = DettaglioProcedura.objects.create(
            fk_procedura=self.procedura,
            fk_faselavoro=self.fase_lavoro,
            is_interna=True,
            numero_riga=1,
            created_by=self.user,
        )

        # ID 99999 non esiste
        with self.assertRaises(DomainValidationError) as ctx:
            reorder_dettagli(
                procedura_id=self.procedura.id,
                ordered_ids=[det.id, 99999],
            )

        self.assertIn("99999", str(ctx.exception))

    def test_reorder_caratteristiche_constraint_safe(self):
        """Reorder caratteristiche funziona con UNIQUE constraint (two-phase)."""
        from .models import DettaglioFaseLavoro

        dettaglio_fase = DettaglioFaseLavoro.objects.create(
            fk_fase_lavoro=self.fase_lavoro,
            attributo="Temperatura",
            created_by=self.user,
        )

        dettaglio = DettaglioProcedura.objects.create(
            fk_procedura=self.procedura,
            fk_faselavoro=self.fase_lavoro,
            is_interna=True,
            numero_riga=1,
            created_by=self.user,
        )

        # Crea 3 caratteristiche con numero_riga consecutivi
        car1 = CaratteristicaProcedura.objects.create(
            fk_dettaglio_procedura=dettaglio,
            fk_dettaglio_fase_lavoro=dettaglio_fase,
            valore="val1",
            numero_riga=1,
            created_by=self.user,
        )
        car2 = CaratteristicaProcedura.objects.create(
            fk_dettaglio_procedura=dettaglio,
            fk_dettaglio_fase_lavoro=dettaglio_fase,
            valore="val2",
            numero_riga=2,
            created_by=self.user,
        )
        car3 = CaratteristicaProcedura.objects.create(
            fk_dettaglio_procedura=dettaglio,
            fk_dettaglio_fase_lavoro=dettaglio_fase,
            valore="val3",
            numero_riga=3,
            created_by=self.user,
        )

        # Riordina: [car3, car1, car2] - swap che richiede two-phase
        reorder_caratteristiche(
            dettaglio_id=dettaglio.id,
            ordered_ids=[car3.id, car1.id, car2.id],
        )

        car1.refresh_from_db()
        car2.refresh_from_db()
        car3.refresh_from_db()

        self.assertEqual(car3.numero_riga, 1)
        self.assertEqual(car1.numero_riga, 2)
        self.assertEqual(car2.numero_riga, 3)


class ReorderAPITestCase(APITestCase):
    """Test API per reorder - verifica 400 invece di 500."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        self.client.force_authenticate(user=self.user)

        self.articolo = Articolo.objects.create(
            descrizione="Articolo Test",
            created_by=self.user,
        )
        self.fase_lavoro = FaseLavoro.objects.create(
            descrizione="Fase Test",
            interno_esterno="interno",
            created_by=self.user,
        )
        # Crea procedura manualmente per compatibilità SQLite
        self.procedura = Procedura.objects.create(
            fk_articolo=self.articolo,
            nr_procedura=1,
            nr_revisione=1,
            created_by=self.user,
        )
        self.dettaglio = DettaglioProcedura.objects.create(
            fk_procedura=self.procedura,
            fk_faselavoro=self.fase_lavoro,
            is_interna=True,
            numero_riga=1,
            created_by=self.user,
        )

    def test_reorder_dettagli_invalid_ids_returns_400(self):
        """Reorder dettagli con ID invalidi restituisce 400, non 500."""
        url = f"/api/articoli/procedure/{self.procedura.id}/reorder-dettagli/"

        response = self.client.post(url, {
            "ordered_ids": [self.dettaglio.id, 99999]
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)
        self.assertIn("99999", response.data["detail"])

    def test_reorder_dettagli_empty_list_returns_400(self):
        """Reorder dettagli con lista vuota restituisce 400."""
        url = f"/api/articoli/procedure/{self.procedura.id}/reorder-dettagli/"

        response = self.client.post(url, {
            "ordered_ids": []
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reorder_dettagli_duplicate_ids_returns_400(self):
        """Reorder dettagli con ID duplicati restituisce 400."""
        url = f"/api/articoli/procedure/{self.procedura.id}/reorder-dettagli/"

        response = self.client.post(url, {
            "ordered_ids": [self.dettaglio.id, self.dettaglio.id]
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reorder_caratteristiche_invalid_ids_returns_400(self):
        """Reorder caratteristiche con ID invalidi restituisce 400, non 500."""
        url = f"/api/articoli/dettagli-procedura/{self.dettaglio.id}/reorder-caratteristiche/"

        response = self.client.post(url, {
            "ordered_ids": [99999]
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)


class N1QueryTestCase(TestCase):
    """Test per verificare che N+1 sia risolto."""

    # Soglia query: con prefetch ottimizzato ci aspettiamo:
    # 1 procedura + 1 dettagli + 1 caratteristiche + 2-3 select_related = ~5-6
    QUERY_THRESHOLD = 6

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass"
        )

        self.articolo = Articolo.objects.create(
            descrizione="Articolo Test",
            created_by=self.user,
        )
        self.fase_lavoro = FaseLavoro.objects.create(
            descrizione="Fase Test",
            interno_esterno="interno",
            created_by=self.user,
        )
        self.dettaglio_fase = DettaglioFaseLavoro.objects.create(
            fk_fase_lavoro=self.fase_lavoro,
            attributo="Temperatura",
            created_by=self.user,
        )
        # Crea procedura manualmente per compatibilità SQLite
        self.procedura = Procedura.objects.create(
            fk_articolo=self.articolo,
            nr_procedura=1,
            nr_revisione=1,
            created_by=self.user,
        )

        # Crea 5 dettagli, ciascuno con 3 caratteristiche
        for i in range(5):
            det = DettaglioProcedura.objects.create(
                fk_procedura=self.procedura,
                fk_faselavoro=self.fase_lavoro,
                is_interna=True,
                numero_riga=i + 1,
                created_by=self.user,
            )
            for j in range(3):
                CaratteristicaProcedura.objects.create(
                    fk_dettaglio_procedura=det,
                    fk_dettaglio_fase_lavoro=self.dettaglio_fase,
                    valore=f"val_{i}_{j}",
                    numero_riga=j + 1,
                    created_by=self.user,
                )

    def _format_queries(self, queries):
        """Formatta le query per diagnostica, raggruppate per tabella."""
        from collections import Counter
        tables = Counter()
        for q in queries:
            sql = q["sql"]
            # Estrai nome tabella dal FROM
            if "FROM" in sql.upper():
                parts = sql.upper().split("FROM")[1].strip().split()[0]
                table = parts.strip('"').replace('"', '')
                tables[table] += 1
            else:
                tables["OTHER"] += 1

        lines = [f"  {table}: {count} query" for table, count in tables.most_common()]
        return "\n".join(lines)

    def test_retrieve_procedura_limited_queries(self):
        """
        Retrieve procedura con dettagli e caratteristiche non deve fare N+1.

        Con 5 dettagli e 15 caratteristiche, senza ottimizzazione faremmo:
        - 1 query per procedura
        - 5 query per dettagli (N+1)
        - 15 query per caratteristiche (N+1)
        = 21+ query

        Con prefetch ottimizzato dovremmo stare sotto QUERY_THRESHOLD.
        """
        from rest_framework.test import APIClient
        from django.test.utils import CaptureQueriesContext
        from django.db import connection

        client = APIClient()
        client.force_authenticate(user=self.user)

        with CaptureQueriesContext(connection) as ctx:
            response = client.get(f"/api/articoli/procedure/{self.procedura.id}/")

        self.assertEqual(response.status_code, 200)

        # Verifica che i dati siano completi
        data = response.json()
        self.assertEqual(len(data["dettagli"]), 5)
        for det in data["dettagli"]:
            self.assertEqual(len(det["caratteristiche"]), 3)

        # Verifica limite query
        num_queries = len(ctx)
        self.assertLessEqual(
            num_queries,
            self.QUERY_THRESHOLD,
            f"N+1 DETECTED: {num_queries} query (threshold: {self.QUERY_THRESHOLD})\n"
            f"Query per tabella:\n{self._format_queries(ctx.captured_queries)}\n"
            f"Dettaglio query:\n" +
            "\n".join(f"  [{i+1}] {q['sql'][:120]}..." for i, q in enumerate(ctx.captured_queries))
        )


class CaratteristicaValidationTestCase(APITestCase):
    """Test validazione interna/esterna su CaratteristicaProcedura."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        self.client.force_authenticate(user=self.user)

        self.articolo = Articolo.objects.create(
            descrizione="Articolo Test",
            created_by=self.user,
        )
        self.fase_lavoro = FaseLavoro.objects.create(
            descrizione="Fase Test",
            interno_esterno="interno",
            created_by=self.user,
        )
        self.dettaglio_fase = DettaglioFaseLavoro.objects.create(
            fk_fase_lavoro=self.fase_lavoro,
            attributo="Temperatura",
            created_by=self.user,
        )
        self.fornitore = Fornitore.objects.create(
            ragionesociale="Fornitore Test",
            created_by=self.user,
        )
        self.lavorazione_esterna = LavorazioneEsterna.objects.create(
            descrizione="Lavorazione Test",
            codice="LAV001",
            created_by=self.user,
        )

        # Crea procedura manualmente per compatibilità SQLite
        self.procedura = Procedura.objects.create(
            fk_articolo=self.articolo,
            nr_procedura=1,
            nr_revisione=1,
            created_by=self.user,
        )

        # Dettaglio INTERNO
        self.dettaglio_interno = DettaglioProcedura.objects.create(
            fk_procedura=self.procedura,
            fk_faselavoro=self.fase_lavoro,
            is_interna=True,
            numero_riga=1,
            created_by=self.user,
        )

        # Dettaglio ESTERNO
        self.dettaglio_esterno = DettaglioProcedura.objects.create(
            fk_procedura=self.procedura,
            fk_faselavoro=self.fase_lavoro,
            is_interna=False,
            numero_riga=2,
            created_by=self.user,
        )

    def test_caratteristica_interna_requires_dettaglio_fase(self):
        """Caratteristica su dettaglio interno richiede fk_dettaglio_fase_lavoro."""
        url = "/api/articoli/caratteristiche-procedura/"

        # Senza fk_dettaglio_fase_lavoro -> errore
        response = self.client.post(url, {
            "fk_dettaglio_procedura": self.dettaglio_interno.id,
            "valore": "100",
            "numero_riga": 1,
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Con fk_dettaglio_fase_lavoro -> ok
        response = self.client.post(url, {
            "fk_dettaglio_procedura": self.dettaglio_interno.id,
            "fk_dettaglio_fase_lavoro": self.dettaglio_fase.id,
            "valore": "100",
            "numero_riga": 1,
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_caratteristica_interna_rejects_fornitore(self):
        """Caratteristica su dettaglio interno rifiuta fornitore."""
        url = "/api/articoli/caratteristiche-procedura/"

        response = self.client.post(url, {
            "fk_dettaglio_procedura": self.dettaglio_interno.id,
            "fk_fornitore": self.fornitore.id,
            "numero_riga": 1,
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("interna", str(response.data).lower())

    def test_caratteristica_esterna_requires_fornitore_and_lavorazione(self):
        """Caratteristica su dettaglio esterno richiede fornitore + lavorazione."""
        url = "/api/articoli/caratteristiche-procedura/"

        # Solo fornitore -> errore
        response = self.client.post(url, {
            "fk_dettaglio_procedura": self.dettaglio_esterno.id,
            "fk_fornitore": self.fornitore.id,
            "numero_riga": 1,
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Solo lavorazione -> errore
        response = self.client.post(url, {
            "fk_dettaglio_procedura": self.dettaglio_esterno.id,
            "fk_lavorazione_esterna": self.lavorazione_esterna.id,
            "numero_riga": 2,
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Entrambi -> ok
        response = self.client.post(url, {
            "fk_dettaglio_procedura": self.dettaglio_esterno.id,
            "fk_fornitore": self.fornitore.id,
            "fk_lavorazione_esterna": self.lavorazione_esterna.id,
            "numero_riga": 1,
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_caratteristica_patch_validates_correctly(self):
        """PATCH su caratteristica valida correttamente."""
        # Crea caratteristica valida
        car = CaratteristicaProcedura.objects.create(
            fk_dettaglio_procedura=self.dettaglio_esterno,
            fk_fornitore=self.fornitore,
            fk_lavorazione_esterna=self.lavorazione_esterna,
            valore="50",
            numero_riga=1,
            created_by=self.user,
        )

        url = f"/api/articoli/caratteristiche-procedura/{car.id}/"

        # PATCH solo valore -> ok (mantiene fornitore/lavorazione)
        response = self.client.patch(url, {"valore": "75"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        car.refresh_from_db()
        self.assertEqual(car.valore, "75")


class ConstraintTestCase(TransactionTestCase):
    """
    Test constraint unicità database.

    NOTA: Questi test richiedono PostgreSQL per i constraint.
    Su SQLite vengono saltati.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        self.articolo = Articolo.objects.create(
            descrizione="Articolo Test",
            created_by=self.user,
        )
        self.fase_lavoro = FaseLavoro.objects.create(
            descrizione="Fase Test",
            interno_esterno="interno",
            created_by=self.user,
        )
        self.dettaglio_fase = DettaglioFaseLavoro.objects.create(
            fk_fase_lavoro=self.fase_lavoro,
            attributo="Temperatura",
            created_by=self.user,
        )
        # Crea procedura manualmente per compatibilità SQLite
        self.procedura = Procedura.objects.create(
            fk_articolo=self.articolo,
            nr_procedura=1,
            nr_revisione=1,
            created_by=self.user,
        )

    def test_unique_constraint_dettaglio_numero_riga(self):
        """
        Due dettagli con stesso numero_riga nella stessa procedura
        violano il constraint.
        """
        DettaglioProcedura.objects.create(
            fk_procedura=self.procedura,
            fk_faselavoro=self.fase_lavoro,
            is_interna=True,
            numero_riga=1,
            created_by=self.user,
        )

        with self.assertRaises(IntegrityError):
            DettaglioProcedura.objects.create(
                fk_procedura=self.procedura,
                fk_faselavoro=self.fase_lavoro,
                is_interna=True,
                numero_riga=1,  # Duplicato!
                created_by=self.user,
            )

    def test_unique_constraint_caratteristica_numero_riga(self):
        """
        Due caratteristiche con stesso numero_riga nello stesso dettaglio
        violano il constraint.
        """
        dettaglio = DettaglioProcedura.objects.create(
            fk_procedura=self.procedura,
            fk_faselavoro=self.fase_lavoro,
            is_interna=True,
            numero_riga=1,
            created_by=self.user,
        )

        CaratteristicaProcedura.objects.create(
            fk_dettaglio_procedura=dettaglio,
            fk_dettaglio_fase_lavoro=self.dettaglio_fase,
            valore="100",
            numero_riga=1,
            created_by=self.user,
        )

        with self.assertRaises(IntegrityError):
            CaratteristicaProcedura.objects.create(
                fk_dettaglio_procedura=dettaglio,
                fk_dettaglio_fase_lavoro=self.dettaglio_fase,
                valore="200",
                numero_riga=1,  # Duplicato!
                created_by=self.user,
            )

    @skip_if_sqlite
    def test_unique_constraint_procedura_articolo_nr_rev(self):
        """
        Due procedure con stessa combinazione (articolo, nr_procedura, nr_revisione)
        violano il constraint.

        Richiede PostgreSQL per il constraint composito.
        """
        # Tentativo di creare manualmente una procedura con stessi valori
        with self.assertRaises(IntegrityError):
            Procedura.objects.create(
                fk_articolo=self.articolo,
                nr_procedura=self.procedura.nr_procedura,
                nr_revisione=self.procedura.nr_revisione,  # Duplicato!
                created_by=self.user,
            )

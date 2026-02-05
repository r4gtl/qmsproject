"""
seed_geo - Seed idempotente per tabelle geografiche LWG.

Carica regioni, subregioni e nazioni dai file JSON in acquistopelli/seed/.
Se le tabelle sono gia' popolate (sentinella IT + count>=200), esce con skip
(a meno che --force).

FAIL FAST:
- dataset incoerente (FK non risolvibili) -> ValueError
- collisioni su vincoli unique (ISO2/ISO3) -> IntegrityError rilanciata
"""
import json
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction

from acquistopelli.models import LwgRegione, LwgSubregione, Nazione

SEED_DIR = Path(settings.BASE_DIR) / "acquistopelli" / "seed"


def _norm_str(v: Any) -> Optional[str]:
    """Normalizza stringhe: strip, vuoto->None."""
    if v is None:
        return None
    s = str(v).strip()
    return s or None


def _norm_int(v: Any) -> Optional[int]:
    """Normalizza interi: None o stringa numerica -> int."""
    if v is None:
        return None
    if isinstance(v, int):
        return v
    s = str(v).strip()
    if not s:
        return None
    try:
        return int(s)
    except ValueError:
        raise ValueError(f"Valore intero non valido: {v!r}")


class Command(BaseCommand):
    help = "Seed tabelle geografiche (regioni, subregioni, nazioni) da JSON."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Forza il seed anche se le tabelle sono gia' popolate.",
        )

    def handle(self, *args, **options):
        force: bool = options["force"]

        # Skip robusto: skippa solo se siamo ragionevolmente certi che sia completo.
        if not force:
            it_exists = Nazione.objects.filter(sigla__iexact="IT").exists()
            n_count = Nazione.objects.count()
            if it_exists and n_count >= 200:
                self.stdout.write(
                    self.style.WARNING(
                        "Tabelle geografiche gia' popolate (sentinella IT + count>=200) — skip. "
                        "Usa --force per forzare l'upsert."
                    )
                )
                return

        regioni_path = SEED_DIR / "lwg_regioni.json"
        subregioni_path = SEED_DIR / "lwg_subregioni.json"
        nazioni_path = SEED_DIR / "nazioni.json"

        for p in (regioni_path, subregioni_path, nazioni_path):
            if not p.exists():
                raise FileNotFoundError(f"File seed mancante: {p}")

        regioni_data = json.loads(regioni_path.read_text(encoding="utf-8"))
        subregioni_data = json.loads(subregioni_path.read_text(encoding="utf-8"))
        nazioni_data = json.loads(nazioni_path.read_text(encoding="utf-8"))

        with transaction.atomic():
            regione_map, reg_stats = self._seed_regioni(regioni_data)
            subregione_map, sub_stats = self._seed_subregioni(subregioni_data, regione_map)
            naz_stats = self._seed_nazioni(nazioni_data, regione_map, subregione_map)

        self.stdout.write(
            self.style.SUCCESS(
                "Seed geografico completato. "
                f"Regioni: {reg_stats[0]} create, {reg_stats[1]} aggiornate. "
                f"Subregioni: {sub_stats[0]} create, {sub_stats[1]} aggiornate. "
                f"Nazioni: {naz_stats[0]} create, {naz_stats[1]} aggiornate."
            )
        )

    # ------------------------------------------------------------------
    # Regioni
    # ------------------------------------------------------------------
    def _seed_regioni(self, data) -> Tuple[Dict[int, LwgRegione], Tuple[int, int]]:
        """Ritorna (dict {codice_m49: LwgRegione}, (created, updated))."""
        created = updated = 0
        regione_map: Dict[int, LwgRegione] = {}

        for row in data:
            codice = _norm_int(row.get("codice_m49"))
            nome = _norm_str(row.get("nome_regione"))
            if not nome:
                raise ValueError(f"Regione con nome_regione mancante/vuoto: {row!r}")

            if codice is not None:
                obj, is_new = LwgRegione.objects.update_or_create(
                    codice_m49=codice,
                    defaults={"nome_regione": nome},
                )
                regione_map[codice] = obj
            else:
                # NOTA: non usare codice_m49=None come chiave (UNIQUE consente piu' NULL in Postgres)
                obj, is_new = LwgRegione.objects.update_or_create(
                    nome_regione=nome,
                    defaults={},
                )

            if is_new:
                created += 1
            else:
                updated += 1

        self.stdout.write(f"  Regioni: {created} create, {updated} aggiornate")
        return regione_map, (created, updated)

    # ------------------------------------------------------------------
    # Subregioni
    # ------------------------------------------------------------------
    def _seed_subregioni(
        self,
        data,
        regione_map: Dict[int, LwgRegione],
    ) -> Tuple[Dict[int, LwgSubregione], Tuple[int, int]]:
        """Ritorna (dict {codice_m49: LwgSubregione}, (created, updated))."""
        created = updated = 0
        subregione_map: Dict[int, LwgSubregione] = {}

        for row in data:
            codice = _norm_int(row.get("codice_m49"))
            nome = _norm_str(row.get("nome_subregione"))
            reg_codice = _norm_int(row.get("regione_codice_m49"))

            if not nome:
                raise ValueError(f"Subregione con nome_subregione mancante/vuoto: {row!r}")
            if reg_codice is None:
                raise ValueError(f"Subregione '{nome}': regione_codice_m49 mancante: {row!r}")
            if reg_codice not in regione_map:
                raise ValueError(
                    f"Subregione '{nome}': regione con codice_m49={reg_codice} non trovata nel seed regioni."
                )

            regione = regione_map[reg_codice]

            if codice is not None:
                obj, is_new = LwgSubregione.objects.update_or_create(
                    codice_m49=codice,
                    defaults={"nome_subregione": nome, "regione": regione},
                )
                subregione_map[codice] = obj
            else:
                # Fallback su nome (ma in teoria codice_m49 dovrebbe esserci sempre nel seed)
                obj, is_new = LwgSubregione.objects.update_or_create(
                    nome_subregione=nome,
                    defaults={"regione": regione},
                )

            if is_new:
                created += 1
            else:
                updated += 1

        self.stdout.write(f"  Subregioni: {created} create, {updated} aggiornate")
        return subregione_map, (created, updated)

    # ------------------------------------------------------------------
    # Nazioni
    # ------------------------------------------------------------------
    def _seed_nazioni(
        self,
        data,
        regione_map: Dict[int, LwgRegione],
        subregione_map: Dict[int, LwgSubregione],
    ) -> Tuple[int, int]:
        """Ritorna (created, updated)."""
        created = updated = 0

        for row in data:
            sigla = _norm_str(row.get("sigla"))  # ISO2
            sigla_estesa = _norm_str(row.get("sigla_estesa"))  # ISO3
            descrizione = _norm_str(row.get("descrizione"))
            codice_m49 = _norm_int(row.get("codice_m49"))

            reg_codice = _norm_int(row.get("regione_codice_m49"))
            sub_codice = _norm_int(row.get("subregione_codice_m49"))

            # FAIL FAST su riferimenti incoerenti
            regione = None
            subregione = None
            if reg_codice is not None:
                regione = regione_map.get(reg_codice)
                if regione is None:
                    raise ValueError(
                        f"Nazione '{descrizione or sigla or sigla_estesa}': "
                        f"regione_codice_m49={reg_codice} non trovata nel seed regioni."
                    )
            if sub_codice is not None:
                subregione = subregione_map.get(sub_codice)
                if subregione is None:
                    raise ValueError(
                        f"Nazione '{descrizione or sigla or sigla_estesa}': "
                        f"subregione_codice_m49={sub_codice} non trovata nel seed subregioni."
                    )

            if not (sigla or sigla_estesa or descrizione):
                raise ValueError(f"Nazione senza chiavi (sigla/sigla_estesa/descrizione): {row!r}")

            # Trova record esistente: ISO2 > ISO3 > descrizione (case-insensitive)
            obj = None
            if sigla:
                obj = Nazione.objects.filter(sigla__iexact=sigla).first()
            if obj is None and sigla_estesa:
                obj = Nazione.objects.filter(sigla_estesa__iexact=sigla_estesa).first()
            if obj is None and descrizione:
                obj = Nazione.objects.filter(descrizione__iexact=descrizione).first()

            defaults: Dict[str, Any] = {
                "descrizione": descrizione,
                "codice_m49": codice_m49,
                "regione": regione,
                "subregione": subregione,
            }
            if sigla is not None:
                defaults["sigla"] = sigla
            if sigla_estesa is not None:
                defaults["sigla_estesa"] = sigla_estesa

            try:
                if obj:
                    for attr, val in defaults.items():
                        setattr(obj, attr, val)
                    obj.save()
                    updated += 1
                else:
                    Nazione.objects.create(**defaults)
                    created += 1
            except IntegrityError as e:
                # FAIL FAST: collisioni su vincoli unique (ISO2/ISO3) devono bloccare il seed
                raise IntegrityError(
                    "Collisione vincoli unique durante seed nazioni. "
                    f"sigla={sigla!r}, sigla_estesa={sigla_estesa!r}, descrizione={descrizione!r}"
                ) from e

        self.stdout.write(f"  Nazioni: {created} create, {updated} aggiornate")
        return created, updated

"""
Test suite per Human Resources API.

Copertura:
- Vincolo unicità ValutazioneOperatore (fk_hr, fk_centro_di_lavoro)
- API error handling (409 per duplicati)
- Delete lookup in uso (409 se protetto)
- Validazione date dipendente
"""
from datetime import date
from django.test import TestCase, TransactionTestCase
from django.contrib.auth.models import User
from django.db import IntegrityError, connection
from rest_framework.test import APITestCase
from rest_framework import status

from .models import (
    HumanResource,
    CentrodiLavoro,
    Ward,
    Role,
    ValutazioneOperatore,
)


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


class ValutazioneConstraintTestCase(TransactionTestCase):
    """
    Test vincolo unicità su ValutazioneOperatore.

    Il constraint ux_valutazione_hr_centro impedisce di avere
    più di una valutazione per la stessa coppia (dipendente, centro di lavoro).
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        self.dipendente = HumanResource.objects.create(
            cognomedipendente="Rossi",
            nomedipendente="Mario",
            dataassunzione=date(2020, 1, 1),
        )
        self.centro = CentrodiLavoro.objects.create(
            description="Centro Test",
        )

    def test_unique_constraint_valutazione_db(self):
        """
        Due valutazioni con stessa coppia (fk_hr, fk_centro_di_lavoro)
        violano il constraint a livello DB.
        """
        # Prima valutazione: ok
        ValutazioneOperatore.objects.create(
            fk_hr=self.dipendente,
            fk_centro_di_lavoro=self.centro,
            valutazione="medio",
        )

        # Seconda valutazione con stessi FK: IntegrityError
        with self.assertRaises(IntegrityError):
            ValutazioneOperatore.objects.create(
                fk_hr=self.dipendente,
                fk_centro_di_lavoro=self.centro,
                valutazione="massimo",
            )

    def test_different_centro_same_hr_allowed(self):
        """
        Stesso dipendente può avere valutazioni su centri diversi.
        """
        centro2 = CentrodiLavoro.objects.create(
            description="Centro 2",
        )

        # Prima valutazione
        ValutazioneOperatore.objects.create(
            fk_hr=self.dipendente,
            fk_centro_di_lavoro=self.centro,
            valutazione="medio",
        )

        # Seconda valutazione su centro diverso: ok
        val2 = ValutazioneOperatore.objects.create(
            fk_hr=self.dipendente,
            fk_centro_di_lavoro=centro2,
            valutazione="massimo",
        )

        self.assertIsNotNone(val2.id)

    def test_different_hr_same_centro_allowed(self):
        """
        Stesso centro può avere valutazioni per dipendenti diversi.
        """
        dipendente2 = HumanResource.objects.create(
            cognomedipendente="Bianchi",
            nomedipendente="Luigi",
            dataassunzione=date(2021, 1, 1),
        )

        # Prima valutazione
        ValutazioneOperatore.objects.create(
            fk_hr=self.dipendente,
            fk_centro_di_lavoro=self.centro,
            valutazione="medio",
        )

        # Seconda valutazione per altro dipendente: ok
        val2 = ValutazioneOperatore.objects.create(
            fk_hr=dipendente2,
            fk_centro_di_lavoro=self.centro,
            valutazione="massimo",
        )

        self.assertIsNotNone(val2.id)


class ValutazioneAPITestCase(APITestCase):
    """
    Test API per ValutazioneOperatore.
    Verifica che duplicati restituiscano 409, non 500.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        self.client.force_authenticate(user=self.user)

        self.dipendente = HumanResource.objects.create(
            cognomedipendente="Rossi",
            nomedipendente="Mario",
            dataassunzione=date(2020, 1, 1),
        )
        self.centro = CentrodiLavoro.objects.create(
            description="Centro Test",
        )

    def test_create_valutazione_success(self):
        """POST valutazione valida restituisce 201."""
        url = "/api/human-resources/valutazioni/"

        response = self.client.post(url, {
            "fk_hr": self.dipendente.id,
            "fk_centro_di_lavoro": self.centro.id,
            "valutazione": "medio",
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["valutazione"], "medio")

    def test_create_duplicate_valutazione_returns_409(self):
        """POST valutazione duplicata restituisce 409 con detail."""
        # Crea prima valutazione
        ValutazioneOperatore.objects.create(
            fk_hr=self.dipendente,
            fk_centro_di_lavoro=self.centro,
            valutazione="medio",
        )

        url = "/api/human-resources/valutazioni/"

        # Tenta duplicato
        response = self.client.post(url, {
            "fk_hr": self.dipendente.id,
            "fk_centro_di_lavoro": self.centro.id,
            "valutazione": "massimo",
        })

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertIn("detail", response.data)
        self.assertIn("già una valutazione", response.data["detail"])

    def test_update_valutazione_same_centro_ok(self):
        """PATCH valutazione esistente sullo stesso centro funziona."""
        val = ValutazioneOperatore.objects.create(
            fk_hr=self.dipendente,
            fk_centro_di_lavoro=self.centro,
            valutazione="medio",
        )

        url = f"/api/human-resources/valutazioni/{val.id}/"

        response = self.client.patch(url, {
            "valutazione": "massimo",
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        val.refresh_from_db()
        self.assertEqual(val.valutazione, "massimo")


class LookupDeleteAPITestCase(APITestCase):
    """
    Test delete lookup tables.

    Con FK PROTECT su ValutazioneOperatore.fk_centro_di_lavoro,
    la delete di un CentrodiLavoro usato deve fallire con 409.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        self.client.force_authenticate(user=self.user)

        self.dipendente = HumanResource.objects.create(
            cognomedipendente="Rossi",
            nomedipendente="Mario",
            dataassunzione=date(2020, 1, 1),
        )
        self.centro = CentrodiLavoro.objects.create(
            description="Centro Test",
        )
        self.reparto = Ward.objects.create(
            description="Reparto Test",
        )
        self.mansione = Role.objects.create(
            description="Mansione Test",
            fk_reparto=self.reparto,
        )

    def test_delete_centro_unused_success(self):
        """DELETE centro non usato restituisce 204."""
        url = f"/api/human-resources/centri-di-lavoro/{self.centro.id}/"

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CentrodiLavoro.objects.filter(id=self.centro.id).exists())

    def test_delete_centro_in_use_returns_409(self):
        """DELETE centro usato da valutazione restituisce 409 con detail."""
        # Crea una valutazione che usa il centro
        ValutazioneOperatore.objects.create(
            fk_hr=self.dipendente,
            fk_centro_di_lavoro=self.centro,
            valutazione="medio",
        )

        url = f"/api/human-resources/centri-di-lavoro/{self.centro.id}/"

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertIn("detail", response.data)
        self.assertIn("elemento in uso", response.data["detail"].lower())
        # Verifica che il centro esista ancora
        self.assertTrue(CentrodiLavoro.objects.filter(id=self.centro.id).exists())

    def test_delete_reparto_unused_success(self):
        """DELETE reparto non usato restituisce 204."""
        # Prima rimuovi mansione che lo usa
        self.mansione.delete()

        url = f"/api/human-resources/reparti/{self.reparto.id}/"

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_mansione_unused_success(self):
        """DELETE mansione non usata restituisce 204."""
        url = f"/api/human-resources/mansioni/{self.mansione.id}/"

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class HumanResourceDateValidationTestCase(APITestCase):
    """Test validazione date su HumanResource."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        self.client.force_authenticate(user=self.user)

    def test_create_dipendente_valid_dates(self):
        """POST dipendente con date valide restituisce 201."""
        url = "/api/human-resources/dipendenti/"

        response = self.client.post(url, {
            "cognomedipendente": "Rossi",
            "nomedipendente": "Mario",
            "dataassunzione": "2020-01-01",
            "datadimissioni": "2023-12-31",
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_dipendente_invalid_dates_returns_400(self):
        """POST dipendente con datadimissioni < dataassunzione restituisce 400."""
        url = "/api/human-resources/dipendenti/"

        response = self.client.post(url, {
            "cognomedipendente": "Rossi",
            "nomedipendente": "Mario",
            "dataassunzione": "2020-01-01",
            "datadimissioni": "2019-01-01",  # Prima dell'assunzione!
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Verifica che l'errore sia sulla data
        self.assertTrue(
            "datadimissioni" in str(response.data) or
            "dimissioni" in str(response.data).lower()
        )


class ConstraintExistsTestCase(TestCase):
    """
    Test per verificare che il constraint esista nel database.

    Utile per CI/CD per verificare che le migration siano applicate.
    """

    @skip_if_sqlite
    def test_constraint_exists_in_postgres(self):
        """
        Verifica che il constraint ux_valutazione_hr_centro esista in PostgreSQL.
        """
        from django.db import connection

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT constraint_name
                FROM information_schema.table_constraints
                WHERE table_name = 'human_resources_valutazioneoperatore'
                  AND constraint_type = 'UNIQUE'
                  AND constraint_name = 'ux_valutazione_hr_centro'
            """)
            result = cursor.fetchone()

        self.assertIsNotNone(
            result,
            "Constraint ux_valutazione_hr_centro non trovato. "
            "Eseguire: python manage.py migrate human_resources"
        )

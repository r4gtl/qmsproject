import unittest
from django.test import TestCase
from django.db.models import Max
from django import forms
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from .models import (
    Facility,
    FacilityContact,
    Fornitore,
    LwgFornitore,
    # Deleted models (migration 0047):
    # FornitorePelli,
    # FornitoreProdottiChimici,
    # FornitoreLavorazioniEsterne,
    # FornitoreServizi,
    # FornitoreRifiuti,
    # FornitoreManutenzioni,
    # Macello,
    gestore_documenti_upload_to,
    smaltitore_documenti_upload_to,
    trasportatore_documenti_upload_to,
    XrDocumentiGestore,
    XrDocumentiSmaltitore,
    XrDocumentiTrasportatore,
    TransferValue,
    XrTransferValueLwgFornitore,
    Cliente,
)
from .forms import (
    FormFornitore,
    FormXrDocumentiGestore,
    FormLwgFornitore,
    # Deleted forms (models removed in migration 0047):
    # FormFornitorePelli,
    # FormFornitoreLavorazioniEsterne,
    # FormFornitoreProdottiChimici,
    # FormFornitoreServizi,
    # FormFornitoreRifiuti,
    # FormFornitoreManutenzioni,
    # FormMacello,
)
from django.contrib.auth.models import User
from datetime import date
from django_countries.fields import Country


class FacilityModelTest(TestCase):
    def setUp(self):
        self.facility = Facility.objects.create(
            nome_sito="Conceria Alfa",
            logo="test_logo.png",
            urn="12345",
            piva="01234567890",
            indirizzo="Via Roma, 1",
            cap="00100",
            city="Roma",
            provincia="RM",
            country="IT",
            phone="0123456789",
            primary_cat=Facility.CAT3,
            secondary_cat=Facility.CAT5,
            tertiary_cat=Facility.CAT6,
            latitude=41.9028,
            longitude=12.4964,
            site_area=5000.0,
            facility_description="Conceria specializzata in pelle di alta qualità.",
        )

    def test_facility_creation(self):
        self.assertEqual(Facility.objects.count(), 1)
        self.assertEqual(self.facility.nome_sito, "Conceria Alfa")
        self.assertEqual(self.facility.primary_cat, Facility.CAT3)
        self.assertAlmostEqual(self.facility.latitude, 41.9028)

    def test_facility_default_values(self):
        facility = Facility.objects.create(nome_sito="Conceria Beta")
        self.assertEqual(facility.primary_cat, Facility.CAT0)
        self.assertEqual(facility.secondary_cat, Facility.CAT0)
        self.assertEqual(facility.tertiary_cat, Facility.CAT0)

    def test_facility_country_field(self):
        self.assertIsInstance(self.facility.country, Country)
        self.assertEqual(self.facility.country.code, "IT")

    def test_facility_get_absolute_url(self):
        self.assertEqual(
            self.facility.get_absolute_url(),
            f"/anagrafiche/edit_facility_details/{self.facility.pk}/",
        )

    def test_str_method(self):
        self.assertEqual(str(self.facility), "Conceria Alfa")


class FacilityContactModelTest(TestCase):
    def setUp(self):
        self.facility = Facility.objects.create(nome_sito="Conceria Alfa")
        self.contact = FacilityContact.objects.create(
            fk_facility=self.facility,
            contact_type=FacilityContact.CONT_1,
            name="Mario Rossi",
            position="Direttore",
            email="mario.rossi@example.com",
        )

    def test_facility_contact_creation(self):
        self.assertEqual(FacilityContact.objects.count(), 1)
        self.assertEqual(self.contact.name, "Mario Rossi")
        self.assertEqual(self.contact.position, "Direttore")
        self.assertEqual(self.contact.contact_type, FacilityContact.CONT_1)
        self.assertEqual(self.contact.email, "mario.rossi@example.com")

    def test_facility_contact_relationship(self):
        self.assertEqual(self.contact.fk_facility, self.facility)
        self.assertEqual(self.facility.contacts.count(), 1)
        self.assertIn(self.contact, self.facility.contacts.all())

    def test_contact_default_type(self):
        contact = FacilityContact.objects.create(
            fk_facility=self.facility,
            name="Luigi Verdi",
            position="Responsabile Ambiente",
        )
        self.assertEqual(contact.contact_type, FacilityContact.CONT_4)


class FornitoreModelTest(TestCase):
    def setUp(self):
        self.fornitore_data = {
            "ragionesociale": "Test Supplier",
            "indirizzo": "Via Test, 123",
            "cap": "12345",
            "city": "TestCity",
            "provincia": "TC",
            "country": "IT",
            "e_mail": "test@supplier.com",
        }
        # Creazione di un fornitore con categoria PELLI
        self.fornitore_data["categoria"] = Fornitore.PELLI
        self.fornitore = Fornitore.objects.create(**self.fornitore_data)

    def tearDown(self):
        """
        Questo metodo viene chiamato automaticamente dopo ogni test per ripulire risorse.
        """
        Fornitore.objects.all().delete()
        # FornitoreRifiuti deleted in migration 0047

    # Tests below skipped: models deleted in migration 0047
    @unittest.skip("Model FornitorePelli deleted in migration 0047")
    def test_creazione_fornitore_categoria_pelli(self):
        """
        Testa la creazione di un fornitore con categoria 'PELLI' e verifica
        che l'istanza FornitorePelli sia stata creata.
        """
        pass

    @unittest.skip("Model FornitoreProdottiChimici deleted in migration 0047")
    def test_creazione_fornitore_categoria_prodotti_chimici(self):
        """Testa la creazione di un fornitore con categoria 'PRODOTTI CHIMICI'."""
        pass

    @unittest.skip("Model FornitoreLavorazioniEsterne deleted in migration 0047")
    def test_creazione_fornitore_categoria_lavorazioni_esterne(self):
        """Testa la creazione di un fornitore con categoria 'LAVORAZIONI ESTERNE'."""
        pass

    @unittest.skip("Model FornitoreServizi deleted in migration 0047")
    def test_creazione_fornitore_categoria_servizi(self):
        """Testa la creazione di un fornitore con categoria 'SERVIZI'."""
        pass

    @unittest.skip("Model FornitoreManutenzioni deleted in migration 0047")
    def test_fornitore_manutenzioni(self):
        """Tests manutenzioni fornitore."""
        pass

    '''def test_creazione_fornitore_categoria_prodotti_chimici(self):
        """Testa la creazione di un fornitore con categoria 'PRODOTTI CHIMICI'."""
        self.fornitore_data["categoria"] = Fornitore.PRODOTTI_CHIMICI
        fornitore = Fornitore.objects.create(**self.fornitore_data)

        # Creazione del fornitore_prodotti_chimici
        fornitore_prodotti_chimici = FornitoreProdottiChimici.objects.create(
            fornitore_ptr=fornitore
        )

        # Verifica che l'istanza di FornitoreProdottiChimici sia stata creata
        self.assertEqual(FornitoreProdottiChimici.objects.count(), 1)
        fornitore_prodotti_chimici = FornitoreProdottiChimici.objects.first()

        # Verifica la relazione tra FornitoreProdottiChimici e Fornitore
        self.assertEqual(fornitore_prodotti_chimici.fornitore_ptr, fornitore)

        # Verifica che il campo 'categoria' del fornitore sia impostato correttamente
        self.assertEqual(
            fornitore_prodotti_chimici.fornitore_ptr.categoria,
            Fornitore.PRODOTTI_CHIMICI,
        )'''

    def test_lwg_fornitore_creation(self):
        """Verifica la creazione di un LwgFornitore collegato a Fornitore."""
        lwg_fornitore = LwgFornitore.objects.create(
            lwg_urn="LWG12345",
            lwg_score="80",
            lwg_range="Gold",
            lwg_date=date(2024, 1, 1),
            lwg_expiry=date(2025, 1, 1),
            fk_fornitore=self.fornitore,
        )
        # Verifica che l'oggetto LwgFornitore sia stato creato correttamente
        self.assertEqual(lwg_fornitore.lwg_urn, "LWG12345")
        self.assertEqual(lwg_fornitore.fk_fornitore, self.fornitore)
        self.assertEqual(lwg_fornitore.lwg_score, "80")
        self.assertEqual(lwg_fornitore.lwg_range, "Gold")
        self.assertEqual(lwg_fornitore.lwg_date, date(2024, 1, 1))
        self.assertEqual(lwg_fornitore.lwg_expiry, date(2025, 1, 1))

        # Creazione di un mock per l'istanza del modello di documento
        """class MockInstance:
            def __init__(self, fornitore_rifiuti):
                self.fornitore_rifiuti = fornitore_rifiuti

        # Istanziazione della classe MockInstance con fornitore_rifiuti
        mock_instance = MockInstance(fornitore_rifiuti)

        # Nome del file per il test
        filename = "documento_test.pdf"

        # Esecuzione della funzione `gestore_documenti_upload_to`
        result = gestore_documenti_upload_to(mock_instance, filename)

        # Verifica del percorso generato
        expected_path = "rifiuti/gestore_documenti/test_fornitore/documento_test.pdf"
        self.assertEqual(result, expected_path)"""


@unittest.skip("Model FornitoreRifiuti deleted in migration 0047")
class DocumentiModelTests(TestCase):
    """Tests skipped: FornitoreRifiuti model deleted in migration 0047."""
    pass


@unittest.skip("Model Macello deleted in migration 0047")
class MacelloModelTest(TestCase):
    """Tests skipped: Macello model deleted in migration 0047."""
    pass


class TransferValueModelTest(TestCase):
    def setUp(self):
        # Creazione di un'istanza di TransferValue
        self.transfer_value = TransferValue.objects.create(
            description="Test Transfer Value", unit="kg"
        )

    def test_transfer_value_creation(self):
        # Verifica che l'istanza sia creata correttamente
        self.assertEqual(self.transfer_value.description, "Test Transfer Value")
        self.assertEqual(self.transfer_value.unit, "kg")


class XrTransferValueLwgFornitoreModelTest(TestCase):
    def setUp(self):
        # Creazione di un utente per il test
        self.user = User.objects.create_user(username="testuser", password="password")

        # Creazione di un fornitore
        self.fornitore = Fornitore.objects.create(
            ragionesociale="Fornitore Test",  # Usa il campo ragionesociale o altri esistenti
            indirizzo="Via Test 123",
            e_mail="fornitore@test.com",
        )

        # Creazione di un'istanza di TransferValue e LwgFornitore
        self.transfer_value = TransferValue.objects.create(
            description="Test Transfer Value", unit="kg"
        )
        self.lwg_fornitore = LwgFornitore.objects.create(
            lwg_urn="Test LwgFornitore",
            fk_fornitore=self.fornitore,  # Passiamo l'oggetto Fornitore
        )
        # Creazione di un'istanza di XrTransferValueLwgFornitore
        self.xr_transfer_value = XrTransferValueLwgFornitore.objects.create(
            fk_lwgcertificato=self.lwg_fornitore,
            fk_transfervalue=self.transfer_value,
            quantity=99.99,
            created_by=self.user,
        )

    def test_xr_transfer_value_creation(self):
        # Verifica che l'istanza sia creata correttamente
        self.assertEqual(
            self.xr_transfer_value.fk_lwgcertificato.lwg_urn, "Test LwgFornitore"
        )
        self.assertEqual(
            self.xr_transfer_value.fk_transfervalue.description, "Test Transfer Value"
        )
        self.assertEqual(self.xr_transfer_value.quantity, 99.99)
        self.assertEqual(self.xr_transfer_value.created_by.username, "testuser")

    def test_quantity_range(self):
        # Test di valore limite per quantity
        self.xr_transfer_value.quantity = 99.99999999  # Testa un valore molto grande
        self.xr_transfer_value.save()
        self.assertEqual(self.xr_transfer_value.quantity, 99.99999999)

    def test_negative_quantity(self):
        # Verifica che la quantità non possa essere negativa se non consentito
        with self.assertRaises(ValidationError):
            self.xr_transfer_value.quantity = -1
            self.xr_transfer_value.full_clean()

    def test_fk_relationship(self):
        # Verifica la relazione FK
        self.assertEqual(
            self.xr_transfer_value.fk_lwgcertificato.lwg_urn, "Test LwgFornitore"
        )
        self.assertEqual(
            self.xr_transfer_value.fk_transfervalue.description, "Test Transfer Value"
        )

    def test_modification(self):
        # Verifica che la modifica dei dati funzioni
        self.xr_transfer_value.quantity = 99.56
        self.xr_transfer_value.save()
        self.assertEqual(self.xr_transfer_value.quantity, 99.56)

    def test_unique_constraint(self):
        # Se esiste una constraint unica, verifica che venga applicata
        with self.assertRaises(IntegrityError):
            XrTransferValueLwgFornitore.objects.create(
                fk_lwgcertificato=self.lwg_fornitore,
                fk_transfervalue=self.transfer_value,
                quantity=99.99999999,
                created_by=self.user,
            )


class ClienteModelTest(TestCase):
    def setUp(self):
        # Creazione di un utente per il test
        self.user = User.objects.create_user(username="testuser", password="password")
        # Creazione di un'istanza di Cliente
        self.cliente = Cliente.objects.create(
            ragionesociale="Test Cliente",
            indirizzo="Via Test, 123",
            cap="12345",
            city="Test City",
            provincia="Test Provincia",
            country="IT",  # Codice del paese per l'Italia
            created_by=self.user,
        )

    def test_cliente_creation(self):
        # Verifica che l'istanza sia creata correttamente
        self.assertEqual(self.cliente.ragionesociale, "Test Cliente")
        self.assertEqual(self.cliente.indirizzo, "Via Test, 123")
        self.assertEqual(self.cliente.cap, "12345")
        self.assertEqual(self.cliente.city, "Test City")
        self.assertEqual(self.cliente.provincia, "Test Provincia")
        self.assertEqual(self.cliente.country.code, "IT")
        self.assertEqual(self.cliente.created_by.username, "testuser")


# FORMS


class FormFornitoreTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.fornitore_data = {
            "ragionesociale": "Test Fornitore",
            "indirizzo": "Via Test, 123",
            "cap": "12345",
            "city": "Test City",
            "provincia": "TC",
            "country": "IT",
            "sito_web": "https://example.com",
            "e_mail": "test@example.com",
            "categoria": "pelli",
            "created_by": self.user,
        }

    def test_form_fornitore_valid(self):
        form = FormFornitore(data=self.fornitore_data)
        self.assertTrue(form.is_valid())

    def test_form_fornitore_invalid(self):
        form_data = self.fornitore_data.copy()
        form_data["e_mail"] = "invalid-email"  # Invalid email
        form = FormFornitore(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("e_mail", form.errors)

    def test_form_fornitore_readonly_categoria(self):
        form = FormFornitore(data=self.fornitore_data)
        categoria_field = form.fields["categoria"]
        self.assertEqual(categoria_field.widget.attrs["readonly"], "readonly")


@unittest.skip("Model FornitoreRifiuti deleted in migration 0047")
class FormXrDocumentiGestoreTests(TestCase):
    """Tests skipped: FornitoreRifiuti model deleted in migration 0047."""
    pass


class FormLwgFornitoreTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")

        # Crea un oggetto Fornitore con ID 1
        self.fornitore = Fornitore.objects.create(
            ragionesociale="Fornitore Test",
            categoria="pelli",  # Usa una categoria valida
            # Aggiungi altri campi necessari per creare un oggetto Fornitore
        )

        self.lwg_fornitore_data = {
            "lwg_urn": "LWG12345",
            "lwg_score": "80",
            "lwg_range": "Gold",
            "lwg_date": "2024-01-01",
            "lwg_expiry": "2025-01-01",
            "fk_fornitore": self.fornitore.id,  # Assuming an existing Fornitore with ID 1
        }

    def test_form_lwg_fornitore_valid(self):
        form = FormLwgFornitore(data=self.lwg_fornitore_data)
        self.assertTrue(form.is_valid())

    def test_form_lwg_fornitore_invalid(self):
        form_data = self.lwg_fornitore_data.copy()
        form_data["lwg_date"] = "invalid-date"  # Invalid date
        form = FormLwgFornitore(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("lwg_date", form.errors)

    def test_form_lwg_fornitore_hidden_fk_fornitore(self):
        form = FormLwgFornitore(data=self.lwg_fornitore_data)
        fk_field = form.fields["fk_fornitore"]
        self.assertEqual(fk_field.widget.__class__, forms.HiddenInput)


class FornitoreFormsTestCase(TestCase):

    def setUp(self):
        self.base_fornitore_data = {
            "ragionesociale": "Fornitore Test",
            "indirizzo": "Via Test 123",
            "cap": "12345",
            "city": "Test City",
            "provincia": "Test Province",
            "country": "IT",
            "sito_web": "http://www.test.com",
            "e_mail": "test@test.com",
            "categoria": Fornitore.PELLI,
        }

    # Form tests skipped: models/forms deleted in migration 0047
    @unittest.skip("Form/Model deleted in migration 0047")
    def test_form_fornitore_pelli(self):
        pass

    @unittest.skip("Form/Model deleted in migration 0047")
    def test_form_fornitore_lavorazioni_esterne(self):
        pass

    @unittest.skip("Form/Model deleted in migration 0047")
    def test_form_fornitore_prodotti_chimici(self):
        pass

    @unittest.skip("Form/Model deleted in migration 0047")
    def test_form_fornitore_servizi(self):
        pass

    @unittest.skip("Form/Model deleted in migration 0047")
    def test_form_fornitore_rifiuti(self):
        pass

    @unittest.skip("Form/Model deleted in migration 0047")
    def test_form_fornitore_manutenzioni(self):
        pass

    @unittest.skip("Form/Model deleted in migration 0047")
    def test_form_macello(self):
        pass

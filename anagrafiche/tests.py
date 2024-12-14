from django.test import TestCase
from django import forms
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from .models import (
    Facility,
    FacilityContact,
    Fornitore,
    LwgFornitore,
    FornitorePelli,
    FornitoreProdottiChimici,
    FornitoreLavorazioniEsterne,
    FornitoreServizi,
    FornitoreRifiuti,
    gestore_documenti_upload_to,
    smaltitore_documenti_upload_to,
    trasportatore_documenti_upload_to,
    XrDocumentiGestore,
    XrDocumentiSmaltitore,
    XrDocumentiTrasportatore,
    FornitoreManutenzioni,
    Macello,
    TransferValue,
    XrTransferValueLwgFornitore,
    Cliente,
    LwgFornitore,
)
from .forms import FormFornitore, FormXrDocumentiGestore, FormLwgFornitore
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


class FornitoreModelTests(TestCase):
    def setUp(self):
        # Creazione utente
        self.user = User.objects.create_user(username="testuser", password="testpass")

        # Creazione Fornitore
        self.fornitore = Fornitore.objects.create(
            ragionesociale="Test Fornitore",
            indirizzo="Via Test, 123",
            cap="12345",
            city="Test City",
            provincia="TC",
            country="IT",
            sito_web="https://example.com",
            e_mail="test@example.com",
            categoria=Fornitore.PELLI,
            created_by=self.user,
        )

    def test_fornitore_creation(self):
        """Verifica che un fornitore venga creato correttamente."""
        self.assertEqual(self.fornitore.ragionesociale, "Test Fornitore")
        self.assertEqual(str(self.fornitore), "Test Fornitore")
        self.assertEqual(self.fornitore.created_by, self.user)

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
        self.assertEqual(lwg_fornitore.lwg_urn, "LWG12345")
        self.assertEqual(lwg_fornitore.fk_fornitore, self.fornitore)

    def test_fornitore_pelli_creation(self):
        """Verifica la creazione e l'ereditarietà di FornitorePelli."""
        fornitore_pelli = FornitorePelli.objects.create(
            fornitore_ptr=self.fornitore,
            is_lwg=True,
            urn="URN123",
            tipo_fornitore=FornitorePelli.MACELLO,
            latitude=45.4642,
            longitude=9.1900,
        )
        self.assertEqual(fornitore_pelli.fornitore_ptr, self.fornitore)
        self.assertTrue(fornitore_pelli.is_lwg)
        self.assertEqual(fornitore_pelli.urn, "URN123")

    def test_fornitore_prodotti_chimici_creation(self):
        """Verifica la creazione e l'ereditarietà di FornitoreProdottiChimici."""
        prodotti_chimici = FornitoreProdottiChimici.objects.create(
            fornitore_ptr=self.fornitore, id_zdhc="12345"
        )
        self.assertEqual(prodotti_chimici.fornitore_ptr, self.fornitore)
        self.assertEqual(prodotti_chimici.id_zdhc, "12345")

    def test_fornitore_lavorazioni_esterne_creation(self):
        """Verifica la creazione e l'ereditarietà di FornitoreLavorazioniEsterne."""
        lavorazioni_esterne = FornitoreLavorazioniEsterne.objects.create(
            fornitore_ptr=self.fornitore,
            is_lwg=True,
            audit=FornitoreLavorazioniEsterne.MANUFACTURER,
        )
        self.assertEqual(lavorazioni_esterne.fornitore_ptr, self.fornitore)
        self.assertTrue(lavorazioni_esterne.is_lwg)
        self.assertEqual(
            lavorazioni_esterne.audit, FornitoreLavorazioniEsterne.MANUFACTURER
        )

    def test_fornitore_servizi_creation(self):
        """Verifica la creazione e l'ereditarietà di FornitoreServizi."""
        servizi = FornitoreServizi.objects.create(
            fornitore_ptr=self.fornitore, prova="Test prova"
        )
        self.assertEqual(servizi.fornitore_ptr, self.fornitore)
        self.assertEqual(servizi.prova, "Test prova")

    def test_gestore_documenti_upload_to(self):
        # Creazione di un fornitore e di un fornitore_rifiuti associato
        fornitore = Fornitore.objects.create(
            ragionesociale="Test Fornitore",
            categoria=Fornitore.RIFIUTI,
        )
        fornitore_rifiuti = FornitoreRifiuti.objects.create(
            fornitore_ptr=fornitore,
            ragionesociale=fornitore.ragionesociale,
        )

        # Creazione di un mock per l'istanza del modello di documento
        class MockInstance:
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
        self.assertEqual(result, expected_path)


class DocumentiModelTests(TestCase):
    def setUp(self):
        # Creazione di un utente e di un fornitore
        self.user = User.objects.create_user(username="testuser", password="password")
        self.fornitore = Fornitore.objects.create(
            ragionesociale="Test Fornitore",
            categoria=Fornitore.RIFIUTI,
        )
        self.fornitore_rifiuti = FornitoreRifiuti.objects.create(
            fornitore_ptr=self.fornitore,
            ragionesociale=self.fornitore.ragionesociale,
        )

    def test_gestore_documenti_upload_to(self):
        # Creazione di un'istanza per XrDocumentiGestore
        documento = XrDocumentiGestore.objects.create(
            fornitore_rifiuti=self.fornitore_rifiuti,
            numero="1234",
            data_documento="2024-01-01",
            data_scadenza="2025-01-01",
            documento=None,  # Nessun file per il test
            created_by=self.user,
        )

        # Verifica che il percorso di upload sia corretto
        expected_path = "rifiuti/gestore_documenti/test_fornitore/1234.pdf"
        result = gestore_documenti_upload_to(documento, "1234.pdf")
        self.assertEqual(result, expected_path)

    def test_smaltitore_documenti_upload_to(self):
        # Creazione di un'istanza per XrDocumentiSmaltitore
        documento = XrDocumentiSmaltitore.objects.create(
            fornitore_rifiuti=self.fornitore_rifiuti,
            numero="5678",
            data_documento="2024-01-01",
            data_scadenza="2025-01-01",
            documento=None,  # Nessun file per il test
        )

        # Verifica che il percorso di upload sia corretto
        expected_path = "rifiuti/smaltitore_documenti/test_fornitore/5678.pdf"
        result = smaltitore_documenti_upload_to(documento, "5678.pdf")
        self.assertEqual(result, expected_path)

    def test_trasportatore_documenti_upload_to(self):
        # Creazione di un'istanza per XrDocumentiTrasportatore
        documento = XrDocumentiTrasportatore.objects.create(
            fornitore_rifiuti=self.fornitore_rifiuti,
            numero="91011",
            data_documento="2024-01-01",
            data_scadenza="2025-01-01",
            documento=None,  # Nessun file per il test
        )

        # Verifica che il percorso di upload sia corretto
        expected_path = "rifiuti/_documenti/test_fornitore/91011.pdf"
        result = trasportatore_documenti_upload_to(documento, "91011.pdf")
        self.assertEqual(result, expected_path)

    def test_fornitore_manutenzioni(self):
        # Creazione di un'istanza per FornitoreManutenzioni
        manutenzione = FornitoreManutenzioni.objects.create(
            fornitore_ptr=self.fornitore,
            prova="Test Prova",
        )

        # Verifica che l'istanza sia correttamente associata al fornitore
        self.assertEqual(
            manutenzione.fornitore_ptr.ragionesociale, self.fornitore.ragionesociale
        )
        self.assertEqual(manutenzione.prova, "Test Prova")


class MacelloModelTest(TestCase):
    def setUp(self):
        # Creazione di un utente per il test
        self.user = User.objects.create_user(username="testuser", password="password")
        # Creazione di un'istanza di Macello
        self.macello = Macello.objects.create(
            ragionesociale="Test Macello", is_group=True, created_by=self.user
        )

    def test_macello_creation(self):
        # Verifica che l'istanza sia creata correttamente
        self.assertEqual(self.macello.ragionesociale, "Test Macello")
        self.assertTrue(self.macello.is_group)
        self.assertEqual(self.macello.created_by.username, "testuser")


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


class FormXrDocumentiGestoreTests(TestCase):
    def setUp(self):
        # Crea l'utente
        self.user = User.objects.create_user(username="testuser", password="testpass")

        # Crea un oggetto Fornitore (modello padre)
        self.fornitore = Fornitore.objects.create(
            ragionesociale="Fornitore Test",
            categoria="pelli",  # Usa una categoria valida
            # Aggiungi altri campi necessari per creare un oggetto Fornitore
        )

        # Crea un oggetto FornitoreRifiuti (supponendo che sia un modello esistente)
        self.fornitore_rifiuti = FornitoreRifiuti.objects.create(
            # Assicurati di includere i campi necessari per creare un oggetto FornitoreRifiuti
            fornitore_ptr=self.fornitore,
        )

        # Dati del form, ora includi fornitore_rifiuti
        self.xr_documenti_data = {
            "numero": "12345",
            "data_documento": "2024-01-01",
            "data_scadenza": "2025-01-01",
            "note": "Test note",
            "created_by": self.user,
            "fornitore_rifiuti": self.fornitore_rifiuti,  # Aggiungi il campo obbligatorio
        }

    def test_form_xr_documenti_gestore_valid(self):
        form = FormXrDocumentiGestore(data=self.xr_documenti_data)
        self.assertTrue(form.is_valid())

    def test_form_xr_documenti_gestore_invalid(self):
        form_data = self.xr_documenti_data.copy()
        form_data["data_documento"] = "invalid-date"  # Invalid date
        form = FormXrDocumentiGestore(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("data_documento", form.errors)

    def test_form_xr_documenti_gestore_placeholder(self):
        form = FormXrDocumentiGestore(data=self.xr_documenti_data)
        numero_field = form.fields["numero"]
        self.assertEqual(
            numero_field.widget.attrs["placeholder"],
            "Inserisci il numero dell'autorizzazione...",
        )


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

import os
from datetime import date

from django.apps import apps
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError, models
from django.urls import reverse
from django_countries.fields import CountryField
from core.models import CompanyOwnedModel  # Import the mixin


class Facility(CompanyOwnedModel):
    #
    # Categorie produzione
    CAT0 = "Nessuna categoria"
    CAT1 = "A - Raw hide/skin to tanned"
    CAT2 = "B - Raw hide/skin to crust"
    CAT3 = "C - Raw hide/skin to finished leather"
    CAT4 = "D - Tanned hide/skin to finished leather"
    CAT5 = "E - Crust hide/skin to finished leather"
    CAT6 = "F - Tanned hide/skin to crust leather"
    CAT7 = "G - Raw hide/skin to pickled/pre-tanned material"

    CHOICES_PRODUCTION_CATEGORY = (
        (CAT0, "Nessuna categoria"),
        (CAT1, "A - Raw hide/skin to tanned"),
        (CAT2, "B - Raw hide/skin to crust"),
        (CAT3, "C - Raw hide/skin to finished leather"),
        (CAT4, "D - Tanned hide/skin to finished leather"),
        (CAT5, "E - Crust hide/skin to finished leather"),
        (CAT6, "F - Tanned hide/skin to crust leather"),
        (CAT7, "G - Raw hide/skin to pickled/pre-tanned material"),
    )

    nome_sito = models.CharField(max_length=100)
    logo = models.ImageField(default="avatar.png", upload_to="logo")
    urn = models.CharField(max_length=50, blank=True, null=True)
    piva = models.CharField(max_length=11, blank=True, null=True)
    indirizzo = models.CharField(max_length=100, blank=True, null=True)
    cap = models.CharField(max_length=5, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    provincia = models.CharField(max_length=2, blank=True, null=True)
    country = CountryField(blank_label="(seleziona Paese)")
    phone = models.CharField(max_length=50, blank=True, null=True)
    primary_cat = models.CharField(
        max_length=50, choices=CHOICES_PRODUCTION_CATEGORY, default=CAT0
    )
    secondary_cat = models.CharField(
        max_length=50, choices=CHOICES_PRODUCTION_CATEGORY, default=CAT0
    )
    tertiary_cat = models.CharField(
        max_length=50, choices=CHOICES_PRODUCTION_CATEGORY, default=CAT0
    )
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    site_area = models.FloatField(blank=True, null=True)
    facility_description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='facility_created')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome_sito

    def get_absolute_url(self):
        return reverse("anagrafiche:edit_facility_details", kwargs={"pk": self.pk})


class FacilityContact(CompanyOwnedModel):
    #
    # Tipo Contatti
    CONT_1 = "6a - Principal Contact Name and position"
    CONT_2 = "6b - Ultimately responsible for environmental issue at this site"
    CONT_3 = (
        "6c - Responsible on a day-to-day basis for environmental issue at this site"
    )
    CONT_4 = "7 - Others"

    CHOICES_CONTACT_TYPE = (
        (CONT_1, "6a - Principal Contact Name and position"),
        (CONT_2, "6b - Ultimately responsible for environmental issue at this site"),
        (
            CONT_3,
            "6c - Responsible on a day-to-day basis for environmental issue at this site",
        ),
        (CONT_4, "7 - Others"),
    )

    fk_facility = models.ForeignKey(
        Facility, related_name="contacts", on_delete=models.CASCADE
    )
    contact_type = models.CharField(
        max_length=100, choices=CHOICES_CONTACT_TYPE, default=CONT_4
    )
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='facility_contact_created')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)


class Fornitore(CompanyOwnedModel):
    # Categorie disponibili
    NESSUNA = "nessuna"
    PELLI = "pelli"
    MACELLO = "macello"
    PRODOTTI_CHIMICI = "prodotti chimici"
    LAVORAZIONI_ESTERNE = "lavorazioni esterne"
    SERVIZI = "servizi"
    MANUTENZIONI = "manutenzioni"
    RIFIUTI = "rifiuti"

    CHOICES_CATEGORY = (
        (NESSUNA, "Manca categoria"),
        (PELLI, "Pelli"),
        (MACELLO, "Macello"),
        (PRODOTTI_CHIMICI, "Prodotti Chimici"),
        (LAVORAZIONI_ESTERNE, "Lavorazioni Esterne"),
        (SERVIZI, "Servizi"),
        (MANUTENZIONI, "Manutenzioni"),
        (RIFIUTI, "Rifiuti"),
    )

    # Campi comuni
    ragionesociale = models.CharField(max_length=50)
    indirizzo = models.CharField(max_length=100, blank=True, null=True)
    cap = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    provincia = models.CharField(max_length=50, blank=True, null=True)
    country = CountryField(blank_label="(seleziona Paese)", default='IT')
    sito_web = models.CharField(max_length=200, blank=True, null=True)
    e_mail = models.EmailField(blank=True, null=True)
    categoria = models.CharField(max_length=50, choices=CHOICES_CATEGORY, default=NESSUNA)
    created_by = models.ForeignKey(User, related_name="fornitori", null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    # ======================
    # Campi per categoria PELLI
    # ======================
    MACELLO = "macello"
    COMMERCIANTE = "commerciante"
    ALTRO = "altro"
    CHOICES_SUPPLIER_TYPE = (
        (MACELLO, "Macello"),
        (COMMERCIANTE, "Commerciante"),
        (ALTRO, "Altro"),
    )

    is_lwg = models.BooleanField(default=False)
    urn = models.CharField(max_length=50, blank=True, null=True)
    tipo_fornitore = models.CharField(max_length=50, choices=CHOICES_SUPPLIER_TYPE, null=True, blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    # ======================
    # Campi per categoria PRODOTTI CHIMICI
    # ======================
    id_zdhc = models.CharField(max_length=50, blank=True, null=True)

    # ======================
    # Campi per categoria LAVORAZIONI ESTERNE
    # ======================
    NOT_AUDITED = "not_audited"
    MANUFACTURER = "leather_manufacturer_audit_protocol"
    SUBCONTRACTOR = "subcontractor_audit_protocol"
    MINI = "mini_audit_protocol"

    CHOICES_AUDIT = (
        (NOT_AUDITED, "Nessun Audit"),
        (MANUFACTURER, "Leather Manufacturer Audit Protocol"),
        (SUBCONTRACTOR, "Subcontractor Audit Protocol"),
        (MINI, "Mini-Audit Protocol"),
    )

    audit = models.CharField(max_length=50, choices=CHOICES_AUDIT, blank=True, null=True)

    # ======================
    # Campi per categoria MANUTENZIONI
    # ======================
    manutenzione_note = models.CharField(max_length=50, blank=True, null=True)

    # ======================
    # Campi per categoria MACELLO
    # ======================
    #is_group = models.BooleanField(default=False)

    class Meta:
        ordering = ["ragionesociale"]

    def __str__(self):
        return self.ragionesociale



def gestore_documenti_upload_to(instance, filename):
    if not instance.fornitore_rifiuti:
        raise ValueError("L'istanza 'fornitore_rifiuti' non è definita.")
    if not instance.fornitore_rifiuti.fornitore_ptr:
        raise ValueError("L'istanza 'fornitore_ptr' non è definita.")

    # Normalizza la ragione sociale per evitare caratteri non validi nei nomi delle cartelle
    """ragione_sociale_normalizzata = (
        instance.fornitore_rifiuti.fornitore_ptr_ragionesociale.replace(
            " ", "_"
        ).lower()
    )"""
    ragione_sociale_normalizzata = instance.fornitore_rifiuti.ragionesociale.replace(
        " ", "_"
    ).lower()

    # Crea il percorso: rifiuti/gestore_documenti/[ragionesociale]/[filename]
    return os.path.join(
        "rifiuti", "gestore_documenti", ragione_sociale_normalizzata, filename
    )


class XrDocumentiGestore(CompanyOwnedModel):
    fornitore_rifiuti = models.ForeignKey(
        Fornitore, on_delete=models.CASCADE, related_name="documenti_gestore"
    )
    numero = models.CharField(max_length=50, blank=True, null=True)
    data_documento = models.DateField(blank=True, null=True)
    data_scadenza = models.DateField(blank=True, null=True)
    documento = models.FileField(
        upload_to=gestore_documenti_upload_to, null=True, blank=True
    )
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        User,
        related_name="documenti_gestore",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Documenti Gestore"

    def __str__(self):
        return f"Aut. N. {self.numero} del {self.data_documento}"


def smaltitore_documenti_upload_to(instance, filename):
    ragione_sociale_normalizzata = (
        instance.fornitore_rifiuti.fornitore_ptr.ragionesociale.replace(
            " ", "_"
        ).lower()
    )
    return os.path.join(
        "rifiuti", "smaltitore_documenti", ragione_sociale_normalizzata, filename
    )


class XrDocumentiSmaltitore(CompanyOwnedModel):
    fornitore_rifiuti = models.ForeignKey(
        Fornitore, on_delete=models.CASCADE, related_name="documenti_smaltitore"
    )
    numero = models.CharField(max_length=50, blank=True, null=True)
    data_documento = models.DateField(blank=True, null=True)
    data_scadenza = models.DateField(blank=True, null=True)
    documento = models.FileField(upload_to=smaltitore_documenti_upload_to)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='documenti_smaltitore_created')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Documenti Smaltitore"


def trasportatore_documenti_upload_to(instance, filename):
    ragione_sociale_normalizzata = (
        instance.fornitore_rifiuti.fornitore_ptr.ragionesociale.replace(
            " ", "_"
        ).lower()
    )
    return os.path.join("rifiuti", "_documenti", ragione_sociale_normalizzata, filename)


class XrDocumentiTrasportatore(CompanyOwnedModel):
    fornitore_rifiuti = models.ForeignKey(
        Fornitore,
        on_delete=models.CASCADE,
        related_name="documenti_trasportatore",
    )
    numero = models.CharField(max_length=50, blank=True, null=True)
    data_documento = models.DateField(blank=True, null=True)
    data_scadenza = models.DateField(blank=True, null=True)
    documento = models.FileField(upload_to=trasportatore_documenti_upload_to)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='documenti_trasportatore_created')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Documenti Trasportatore"






class LwgFornitore(CompanyOwnedModel):
    lwg_urn = models.CharField(max_length=50)
    lwg_score = models.CharField(max_length=50, blank=True, null=True)
    lwg_range = models.CharField(max_length=100, blank=True, null=True)
    lwg_date = models.DateField(blank=True, null=True)
    lwg_expiry = models.DateField(blank=True, null=True)
    documento = models.FileField(upload_to="lwg_certificates/", null=True, blank=True)
    fk_fornitore = models.ForeignKey(Fornitore, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='lwg_fornitore_created')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)


"""I PROSSIMI MODELLI SONO PER GESTIRE LE CATEGORIE SFRUTTANDO L'EREDITARIETA' DEL MODELLO FORNITORE"""



class TransferValue(models.Model):
    description = models.CharField(max_length=50)
    unit = models.CharField(max_length=20)

    class Meta:
        ordering = ["description"]

    def __str__(self):
        return self.description


def validate_positive_quantity(value):
    if value < 0:
        raise ValidationError("Quantity cannot be negative.")


class XrTransferValueLwgFornitore(CompanyOwnedModel):

    fk_lwgcertificato = models.ForeignKey(LwgFornitore, on_delete=models.CASCADE)
    fk_transfervalue = models.ForeignKey(TransferValue, on_delete=models.CASCADE)
    quantity = models.DecimalField(
        max_digits=10, decimal_places=8, validators=[validate_positive_quantity]
    )
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        User,
        related_name="xrtransfervaluelwgfornitore",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["fk_lwgcertificato", "fk_transfervalue"],
                name="unique_lwgcertificato_transfervalue",
            )
        ]


class Cliente(CompanyOwnedModel):
    ragionesociale = models.CharField(max_length=50, blank=False, null=False)
    indirizzo = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    partita_iva = models.CharField(max_length=50, blank=True, null=True)
    cap = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    provincia = models.CharField(max_length=50, blank=True, null=True)
    country = CountryField(blank_label="(seleziona Paese)", default='IT')
    created_by = models.ForeignKey(
        User, related_name="clienti", on_delete=models.CASCADE, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["ragionesociale"]

    def __str__(self):
        return self.ragionesociale

    def get_absolute_url(self):
        return reverse("anagrafiche:modifica_cliente", kwargs={"pk": self.pk})


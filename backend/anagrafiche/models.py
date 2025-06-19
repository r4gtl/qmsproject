import os
from datetime import date

from django.apps import apps
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError, models
from django.urls import reverse
from django_countries.fields import \
    CountryField  # Field from django countries app


class Facility(models.Model):
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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome_sito

    def get_absolute_url(self):
        return reverse("anagrafiche:edit_facility_details", kwargs={"pk": self.pk})


class FacilityContact(models.Model):
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



'''class Fornitore(models.Model):
    #
    # Categoria
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
    ragionesociale = models.CharField(max_length=50, blank=False, null=False)
    indirizzo = models.CharField(max_length=100, blank=True, null=True)
    cap = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    provincia = models.CharField(max_length=50, blank=True, null=True)
    country = CountryField(blank_label="(seleziona Paese)")
    sito_web = models.CharField(max_length=200, blank=True, null=True)
    e_mail = models.EmailField(blank=True, null=True)
    categoria = models.CharField(
        max_length=50, choices=CHOICES_CATEGORY, default=NESSUNA
    )
    created_by = models.ForeignKey(
        User, related_name="fornitori", null=True, blank=True, on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ["ragionesociale"]

    def __str__(self):
        return self.ragionesociale

    def get_absolute_url(self):
        return reverse("anagrafiche:vedi_fornitore", kwargs={"pk": self.pk})

    def associa_categoria(self):
        """
        Metodo per associare il fornitore alla sottoclasse di categoria corrispondente.
        """
        # Stampa il valore corrente della categoria per debug
        # print(f"Categoria fornita: {self.categoria}")

        # Gestione del caso 'NESSUNA'
        if self.categoria.upper() == "NESSUNA":
            # print("Categoria 'NESSUNA' selezionata, nessun modello da associare.")
            return  # Nessuna associazione necessaria

        # Normalizza il nome del modello
        categoria_model_name = f'Fornitore{self.categoria.title().replace(" ", "")}'

        # print(f"Nome del modello categoria: {categoria_model_name}")

        try:
            # Tenta di recuperare il modello per la categoria
            categoria_model = apps.get_model(
                app_label="anagrafiche", model_name=categoria_model_name
            )
        except LookupError:
            raise ValidationError(
                f"Modello per la categoria '{self.categoria}' non trovato."
            )

        # Mappatura degli attributi per il ptr
        categoria_attr_map = {
            "FornitorePelli": "fornitore_ptr_pelli",
            "FornitoreProdottiChimici": "fornitore_ptr_prodottichimici",
            "FornitoreManutenzioni": "fornitore_ptr_manutenzioni",
            "FornitoreLavorazioniEsterne": "fornitore_ptr_lavorazioniesterne",
            "FornitoreServizi": "fornitore_ptr_servizi",
            "FornitoreRifiuti": "fornitore_ptr_rifiuti",
            "FornitoreMacello": "fornitore_ptr_macello",
        }

        categoria_attr = categoria_attr_map.get(categoria_model_name)
        if not categoria_attr:
            raise ValidationError(
                f"Attributo per la categoria '{self.categoria}' non trovato."
            )

        try:
            # Verifica se esiste già un'istanza della sottoclasse
            categoria_instance = categoria_model.objects.filter(
                fornitore_ptr=self
            ).first()
            if categoria_instance:
                """print(
                    f"Istanza della categoria '{self.categoria}' già esistente: {categoria_instance}"
                )"""
                setattr(self, categoria_attr, categoria_instance)
            else:
                # Crea una nuova istanza se non esiste
                categoria_instance = categoria_model.objects.create(fornitore_ptr=self)
                setattr(self, categoria_attr, categoria_instance)
                self.save()  # Salva l'istanza del modello generico con la relazione
        except IntegrityError as e:
            raise ValidationError(
                f"Errore durante l'associazione della categoria: {str(e)}"
            )

    def save(self, *args, **kwargs):
        """
        Sovrascrive il metodo save per gestire automaticamente l'associazione della categoria.
        """
        super().save(*args, **kwargs)  # Salva l'istanza principale
        try:
            self.associa_categoria()  # Associa la categoria
        except ValidationError as e:
            raise e'''
        

class Fornitore(models.Model):
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
    country = CountryField(blank_label="(seleziona Paese)")
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


class XrDocumentiGestore(models.Model):
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


class XrDocumentiSmaltitore(models.Model):
    fornitore_rifiuti = models.ForeignKey(
        Fornitore, on_delete=models.CASCADE, related_name="documenti_smaltitore"
    )
    numero = models.CharField(max_length=50, blank=True, null=True)
    data_documento = models.DateField(blank=True, null=True)
    data_scadenza = models.DateField(blank=True, null=True)
    documento = models.FileField(upload_to=smaltitore_documenti_upload_to)

    class Meta:
        verbose_name_plural = "Documenti Smaltitore"


def trasportatore_documenti_upload_to(instance, filename):
    ragione_sociale_normalizzata = (
        instance.fornitore_rifiuti.fornitore_ptr.ragionesociale.replace(
            " ", "_"
        ).lower()
    )
    return os.path.join("rifiuti", "_documenti", ragione_sociale_normalizzata, filename)


class XrDocumentiTrasportatore(models.Model):
    fornitore_rifiuti = models.ForeignKey(
        Fornitore,
        on_delete=models.CASCADE,
        related_name="documenti_trasportatore",
    )
    numero = models.CharField(max_length=50, blank=True, null=True)
    data_documento = models.DateField(blank=True, null=True)
    data_scadenza = models.DateField(blank=True, null=True)
    documento = models.FileField(upload_to=trasportatore_documenti_upload_to)

    class Meta:
        verbose_name_plural = "Documenti Trasportatore"






class LwgFornitore(models.Model):
    lwg_urn = models.CharField(max_length=50)
    lwg_score = models.CharField(max_length=50, blank=True, null=True)
    lwg_range = models.CharField(max_length=100, blank=True, null=True)
    lwg_date = models.DateField(blank=True, null=True)
    lwg_expiry = models.DateField(blank=True, null=True)
    documento = models.FileField(upload_to="lwg_certificates/", null=True, blank=True)
    fk_fornitore = models.ForeignKey(Fornitore, on_delete=models.CASCADE)


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


class XrTransferValueLwgFornitore(models.Model):

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


class Cliente(models.Model):
    ragionesociale = models.CharField(max_length=50, blank=False, null=False)
    indirizzo = models.CharField(max_length=100, blank=True, null=True)
    cap = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    provincia = models.CharField(max_length=50, blank=True, null=True)
    country = CountryField(blank_label="(seleziona Paese)")
    created_by = models.ForeignKey(
        User, related_name="clienti", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["ragionesociale"]

    def __str__(self):
        return self.ragionesociale

    def get_absolute_url(self):
        return reverse("anagrafiche:modifica_cliente", kwargs={"pk": self.pk})


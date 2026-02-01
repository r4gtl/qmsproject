from datetime import date

from acquistopelli.models import TipoAnimale, TipoGrezzo
from anagrafiche.models import Fornitore, Cliente
from django.contrib.auth.models import User
from django.db import models
# Max rimosso: numerazione gestita da services/procedure.py
from django.utils import timezone


class Articolo(models.Model):
    # Industrie fornite
    APPAREL_CLOTHING = "apparel/clothing"
    AUTOMOTIVE = "automotive"
    CONTRACT = "contract"
    FOOTWEAR = "footwear"
    FOOTWEAR_ATHLETIC = "footwear (athletic)"
    LEATHER_GOODS = "leather goods"
    UPHOLSTERY = "upholstery"

    CHOICES_INDUSTRIES_SERVED = (
        (APPAREL_CLOTHING, "Apparel/clothing"),
        (AUTOMOTIVE, "Automotive"),
        (CONTRACT, "Contract"),
        (FOOTWEAR, "Footwear"),
        (FOOTWEAR_ATHLETIC, "Footwear (Athletic)"),
        (LEATHER_GOODS, "Leather goods"),
        (UPHOLSTERY, "Upholstery"),
    )

    descrizione = models.CharField(max_length=100)
    scheda_tecnica = models.FileField(
        upload_to="schede_tecniche_articoli/", null=True, blank=True
    )
    industries_served = models.CharField(
        max_length=50, choices=CHOICES_INDUSTRIES_SERVED, null=True, blank=True
    )
    fk_tipoanimale = models.ForeignKey(
        TipoAnimale,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="articolo",
    )
    fk_tipogrezzo = models.ForeignKey(
        TipoGrezzo,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="articolo",
    )
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        User, related_name="articolo", null=True, blank=True, on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["descrizione"]
        verbose_name_plural = "articoli"

    def __str__(self):
        return self.descrizione


class Colore(models.Model):
    descrizione = models.CharField(max_length=100)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        User, related_name="colore", null=True, blank=True, on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["descrizione"]
        verbose_name_plural = "colori"

    def __str__(self):
        return self.descrizione


class FaseLavoro(models.Model):

    # Interno/Esterno
    INTERNO = "interno"
    ESTERNO = "esterno"

    CHOICES_INT_EST = ((INTERNO, "Interno"), (ESTERNO, "Esterno"))

    # Unità di misura
    MQ = "mq"
    NUMERO = "Nr."
    PESO_KG = "Kg."

    CHOICES_UM = (
        (MQ, "Mq."),
        (NUMERO, "Nr."),
        (PESO_KG, "Kg."),
    )
    descrizione = models.CharField(max_length=100)
    interno_esterno = models.CharField(
        max_length=10, choices=CHOICES_INT_EST, null=True, blank=True
    )
    um = models.CharField(max_length=100, choices=CHOICES_UM, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        User,
        related_name="faselavoro",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["descrizione"]
        verbose_name_plural = "fasi lavoro"

    def __str__(self):
        return self.descrizione


class DettaglioFaseLavoro(models.Model):
    fk_fase_lavoro = models.ForeignKey(FaseLavoro, on_delete=models.CASCADE)
    attributo = models.CharField(max_length=100)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        User,
        related_name="dettagliofaselavoro",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.attributo


class LavorazioneEsterna(models.Model):
    descrizione = models.CharField(max_length=200)
    codice = models.CharField(max_length=9)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        User,
        related_name="lavorazione_esterna",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.descrizione

    class Meta:
        ordering = ["descrizione"]
        verbose_name_plural = "Lavorazioni esterne"


class Procedura(models.Model):
    """
    Procedura di lavorazione per un Articolo.

    Numerazione gestita da services/procedure.py:
    - nr_procedura: generato da sequence DB, unico per "serie" articolo
    - nr_revisione: incrementale per articolo (1, 2, 3...)
    """
    fk_articolo = models.ForeignKey(
        Articolo,
        on_delete=models.CASCADE,
        related_name="procedure"
    )
    nr_procedura = models.IntegerField(blank=True, null=True)
    data_procedura = models.DateField(default=timezone.now)
    nr_revisione = models.IntegerField(blank=True, null=True)
    data_revisione = models.DateField(default=timezone.now)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        User,
        related_name="procedure_create",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-nr_procedura", "-nr_revisione"]
        verbose_name_plural = "procedure"
        constraints = [
            models.UniqueConstraint(
                fields=["fk_articolo", "nr_procedura", "nr_revisione"],
                name="ux_procedura_articolo_nr_rev"
            )
        ]

    def __str__(self):
        return f"{self.fk_articolo} - Proc. {self.nr_procedura} Rev. {self.nr_revisione}"


class DettaglioProcedura(models.Model):
    """
    Riga di dettaglio di una Procedura.

    - is_interna=True: lavorazione interna, caratteristiche usano fk_dettaglio_fase_lavoro
    - is_interna=False: lavorazione esterna (terzista), caratteristiche usano fk_fornitore + fk_lavorazione_esterna

    Nota: fk_fornitore qui è DEPRECATO/LEGACY. La verità su fornitore sta in CaratteristicaProcedura.
    """
    fk_procedura = models.ForeignKey(
        Procedura,
        on_delete=models.CASCADE,
        related_name="dettagli"
    )
    fk_faselavoro = models.ForeignKey(
        FaseLavoro,
        on_delete=models.CASCADE,
        related_name="dettagli_procedura"
    )
    # DEPRECATO: mantenuto per legacy, la verità è su CaratteristicaProcedura
    fk_fornitore = models.ForeignKey(
        Fornitore,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="dettagli_procedura_legacy"
    )
    is_interna = models.BooleanField(default=True)
    numero_riga = models.IntegerField()
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        User,
        related_name="dettaglioprocedura",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["numero_riga"]
        verbose_name_plural = "dettaglio procedure"
        constraints = [
            models.UniqueConstraint(
                fields=["fk_procedura", "numero_riga"],
                name="ux_dettaglio_procedura_riga"
            )
        ]

    def __str__(self):
        tipo = "INT" if self.is_interna else "EST"
        return f"Riga {self.numero_riga} [{tipo}] - {self.fk_faselavoro}"


class CaratteristicaProcedura(models.Model):
    """
    Caratteristica di una riga di dettaglio procedura.

    REGOLE DI VALIDAZIONE (enforced nel serializer):
    - Se DettaglioProcedura.is_interna == True:
        * fk_dettaglio_fase_lavoro OBBLIGATORIO
        * fk_fornitore e fk_lavorazione_esterna DEVONO essere NULL

    - Se DettaglioProcedura.is_interna == False:
        * fk_fornitore e fk_lavorazione_esterna OBBLIGATORI
        * fk_dettaglio_fase_lavoro DEVE essere NULL
    """
    fk_dettaglio_procedura = models.ForeignKey(
        DettaglioProcedura,
        related_name="caratteristiche",
        on_delete=models.CASCADE,
    )
    # Per lavorazione ESTERNA (terzista)
    fk_fornitore = models.ForeignKey(
        Fornitore,
        on_delete=models.CASCADE,
        related_name="caratteristiche_procedura",
        null=True,
        blank=True,
    )
    fk_lavorazione_esterna = models.ForeignKey(
        LavorazioneEsterna,
        on_delete=models.CASCADE,
        related_name="caratteristiche_procedura",
        null=True,
        blank=True,
    )
    # Per lavorazione INTERNA
    fk_dettaglio_fase_lavoro = models.ForeignKey(
        DettaglioFaseLavoro,
        on_delete=models.CASCADE,
        related_name="caratteristiche_procedura",
        null=True,
        blank=True,
    )
    valore = models.CharField(max_length=100, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    numero_riga = models.IntegerField()
    created_by = models.ForeignKey(
        User,
        related_name="caratteristicaprocedura",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["numero_riga"]
        verbose_name_plural = "caratteristiche procedura"
        constraints = [
            models.UniqueConstraint(
                fields=["fk_dettaglio_procedura", "numero_riga"],
                name="ux_caratteristica_procedura_riga"
            )
        ]

    def __str__(self):
        return f"Caratteristica {self.numero_riga} - {self.valore or 'N/A'}"


class ElencoTest(models.Model):
    descrizione = models.CharField(max_length=100)
    norma_riferimento = models.CharField(max_length=100, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        User,
        related_name="elenco_test",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.descrizione

    class Meta:
        ordering = ["descrizione"]
        verbose_name_plural = "elenco test"


class TestArticolo(models.Model):

    # Interno/Esterno
    INTERNO = "interno"
    ESTERNO = "esterno"

    CHOICES_INT_EST = ((INTERNO, "Interno"), (ESTERNO, "Esterno"))

    fk_articolo = models.ForeignKey(
        Articolo, related_name="test_articolo", on_delete=models.CASCADE
    )
    fk_test = models.ForeignKey(
        ElencoTest, related_name="test_articolo", on_delete=models.CASCADE
    )
    valore = models.CharField(max_length=100, blank=True, null=True)
    interno_esterno = models.CharField(
        max_length=10, choices=CHOICES_INT_EST, null=True, blank=True
    )
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        User,
        related_name="test_articolo",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)


class ListinoTerzista(models.Model):
    fk_fornitore = models.ForeignKey(Fornitore, on_delete=models.CASCADE)
    fk_lavorazione_esterna = models.ForeignKey(
        LavorazioneEsterna, on_delete=models.CASCADE
    )
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        User,
        related_name="listino_terzista",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def ultimo_prezzo(self):
        ultimo_prezzo = self.prezzo.order_by("-data_inserimento").first()
        if ultimo_prezzo:
            return ultimo_prezzo.prezzo
        return None


class PrezzoListino(models.Model):
    fk_listino_terzista = models.ForeignKey(
        ListinoTerzista, on_delete=models.CASCADE, related_name="prezzo"
    )
    data_inserimento = models.DateField(default=date.today)
    prezzo = models.DecimalField(max_digits=8, decimal_places=3)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        User,
        related_name="prezzo_listino",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-data_inserimento"]

    def __str__(self):
        return f"Prezzo: {self.prezzo} - Data inserimento: {self.data_inserimento}"


class ListinoCliente(models.Model):
    fk_cliente = models.ForeignKey(
        Cliente, related_name="listino_cliente", on_delete=models.CASCADE
    )
    fk_articolo = models.ForeignKey(
        Articolo, related_name="listino_cliente", on_delete=models.CASCADE
    )
    prezzo = models.DecimalField(max_digits=8, decimal_places=3)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        User,
        related_name="listino_cliente",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fk_articolo.descrizione

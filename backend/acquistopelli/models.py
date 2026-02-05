from anagrafiche.models import Fornitore
from django.conf import settings
from django.db import models
from django.db.models import (ExpressionWrapper, F, IntegerField, OuterRef,
                              Q, Subquery, Sum)
from django.db.models.functions import Coalesce, Lower, Upper
from django_countries.fields import CountryField

from .managers import LottoManager

# =============================================================================
# TABELLE GENERICHE
# =============================================================================

class TipoAnimale(models.Model):
    descrizione = models.CharField(max_length=10)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='animale',
        null=True, blank=True, on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["descrizione"]
        verbose_name_plural = "tipi animale"

    def __str__(self):
        return self.descrizione


class TipoGrezzo(models.Model):
    descrizione = models.CharField(max_length=50)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='grezzo',
        null=True, blank=True, on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["descrizione"]
        verbose_name_plural = "tipi grezzo"

    def __str__(self):
        return self.descrizione


class Scelta(models.Model):
    descrizione = models.CharField(max_length=50)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='scelta',
        null=True, blank=True, on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["descrizione"]
        verbose_name_plural = "scelta"

    def __str__(self):
        return self.descrizione


# =============================================================================
# LWG REGIONI / SUBREGIONI / NAZIONI
# =============================================================================

class LwgRegione(models.Model):
    codice_m49 = models.IntegerField(null=True, blank=True, unique=True)
    nome_regione = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["nome_regione"]
        verbose_name_plural = "regioni LWG"
        db_table = "lwg_regioni"

    def __str__(self):
        return self.nome_regione


class LwgSubregione(models.Model):
    regione = models.ForeignKey(
        LwgRegione, on_delete=models.PROTECT,
        related_name="subregioni",
    )
    codice_m49 = models.IntegerField(null=True, blank=True, unique=True)
    nome_subregione = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["nome_subregione"]
        verbose_name_plural = "subregioni LWG"
        db_table = "lwg_subregioni"
        indexes = [
            models.Index(fields=["regione"], name="idx_subregione_regione"),
        ]

    def __str__(self):
        return f"{self.nome_subregione} ({self.regione.nome_regione})"


class Nazione(models.Model):
    sigla_estesa = models.CharField(max_length=255, null=True, blank=True)  # ISO3
    descrizione = models.CharField(max_length=255, null=True, blank=True)   # Nome nazione
    sigla = models.CharField(max_length=255, null=True, blank=True)         # ISO2
    codice_m49 = models.IntegerField(null=True, blank=True)
    regione = models.ForeignKey(
        LwgRegione, null=True, blank=True,
        on_delete=models.PROTECT, related_name="nazioni",
    )
    subregione = models.ForeignKey(
        LwgSubregione, null=True, blank=True,
        on_delete=models.PROTECT, related_name="nazioni",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='nazione',
        null=True, blank=True, on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["descrizione"]
        verbose_name_plural = "nazioni"
        db_table = "tbl_Nazioni"
        indexes = [
            models.Index(fields=["regione"], name="idx_nazione_regione"),
            models.Index(fields=["subregione"], name="idx_nazione_subregione"),
        ]
        constraints = [
            models.UniqueConstraint(
                Lower("sigla"),
                name="ux_nazione_iso2_lower",
            ),
            models.UniqueConstraint(
                Upper("sigla_estesa"),
                name="ux_nazione_iso3_upper",
            ),
        ]

    def __str__(self):
        return self.descrizione or self.sigla or self.sigla_estesa or f"Nazione #{self.pk}"
    


    

class Lotto(models.Model):
    data_acquisto = models.DateField(null=False, blank=False)
    identificativo = models.CharField(max_length=10, null=False, blank=False)
    fk_tipoanimale = models.ForeignKey(
        TipoAnimale, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='lotto',
    )
    fk_tipogrezzo = models.ForeignKey(
        TipoGrezzo, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='lotto',
    )
    fk_fornitore = models.ForeignKey(
        Fornitore, null=False, blank=False,
        on_delete=models.CASCADE, related_name='lotto',
    )
    origine = CountryField(blank_label='(seleziona Paese)', null=True, blank=True)
    documento = models.CharField(max_length=10, null=True, blank=True)
    is_lwg = models.BooleanField(default=False)
    fk_macello = models.ForeignKey(
        Fornitore, null=True, blank=True,
        on_delete=models.CASCADE, related_name='lotto_macello',
    )
    peso_totale = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    pezzi = models.IntegerField(null=True, blank=True)
    prezzo_unitario = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)
    spese_accessorie = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    kg_km = models.DecimalField(
        max_digits=10, decimal_places=0, null=True, blank=True,
        help_text="Moltiplicare i kg. per i km percorsi per il calcolo della CO2",
    )
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='lotto',
        null=True, blank=True, on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    objects = LottoManager()
    
    def get_scelte_con_rimanenza(self):
        from vendite.models import XRScelteSchede
        used_quantity_subquery = XRScelteSchede.objects.filter(
            fk_sceltalotto=OuterRef('pk')
        ).values('fk_sceltalotto').annotate(
            used=Sum('quantity')
        ).values('used')[:1]

        return self.sceltalotto_set.annotate(
            used_quantity=Coalesce(Subquery(used_quantity_subquery), 0),
            remaining=ExpressionWrapper(
                F('pezzi') - Coalesce(Subquery(used_quantity_subquery), 0),
                output_field=IntegerField()
            )
        ).filter(remaining__gt=0).select_related('fk_scelta')
    

    class Meta:
        ordering = ["-data_acquisto"]
        verbose_name_plural = "Lotti"

    def __str__(self):
        return str(self.data_acquisto) + " " + str(self.identificativo)
    

    
class SceltaLotto(models.Model):
    fk_lotto = models.ForeignKey(Lotto, null=False, blank=False, on_delete=models.CASCADE)
    fk_scelta = models.ForeignKey(Scelta, null=False, blank=False, on_delete=models.CASCADE)
    pezzi = models.IntegerField(null=True, blank=True)
    scelta_terminata = models.BooleanField(default=False)
    data_termine = models.DateField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='sceltalotto',
        null=True, blank=True, on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "scelte lotto"

    def __str__(self):
        scelta = self.fk_scelta.descrizione if self.fk_scelta else "?"
        return f"{scelta} - {self.pezzi or 0} pz"


# =============================================================================
# LOTTO ORIGINE
# =============================================================================

class LottoOrigine(models.Model):
    LIVELLO_PRECISIONE_CHOICES = [
        ("country", "country"),
        ("region", "region"),
        ("subregion", "subregion"),
    ]

    lotto = models.ForeignKey(
        Lotto, on_delete=models.CASCADE, related_name="origini",
    )
    nazione = models.ForeignKey(
        Nazione, null=True, blank=True, on_delete=models.PROTECT,
    )
    regione = models.ForeignKey(
        LwgRegione, null=True, blank=True, on_delete=models.PROTECT,
    )
    subregione = models.ForeignKey(
        LwgSubregione, null=True, blank=True, on_delete=models.PROTECT,
    )
    quota_percentuale = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
    )
    qta_stimata = models.DecimalField(
        max_digits=12, decimal_places=3, null=True, blank=True,
    )
    livello_rischio = models.CharField(max_length=20, null=True, blank=True)
    fonte_dato = models.TextField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    livello_precisione = models.CharField(
        max_length=20, choices=LIVELLO_PRECISIONE_CHOICES, default="country",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='lottoorigine',
        null=True, blank=True, on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "origini lotto"
        db_table = "lot_origini"
        indexes = [
            models.Index(fields=["lotto"], name="idx_lottoorigine_lotto"),
            models.Index(fields=["nazione"], name="idx_lottoorigine_nazione"),
            models.Index(fields=["regione"], name="idx_lottoorigine_regione"),
            models.Index(fields=["subregione"], name="idx_lottoorigine_subreg"),
        ]
        constraints = [
            models.CheckConstraint(
                check=Q(nazione__isnull=False) | Q(regione__isnull=False) | Q(subregione__isnull=False),
                name="chk_lottoorigine_valid",
            ),
        ]

    def __str__(self):
        target = (
            str(self.nazione) if self.nazione
            else str(self.regione) if self.regione
            else str(self.subregione) if self.subregione
            else "—"
        )
        lotto_id = self.lotto.identificativo if self.lotto else "?"
        return f"Origine {self.livello_precisione}: {target} - lotto {lotto_id}"



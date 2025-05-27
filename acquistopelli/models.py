from anagrafiche.models import Fornitore, FornitoreMacello
from django.contrib.auth.models import User
from django.db import models
# prova per le rimanenze delle scelte
from django.db.models import (ExpressionWrapper, F, IntegerField, OuterRef,
                              Subquery, Sum)
from django.db.models.functions import Coalesce
from django_countries.fields import \
    CountryField  # Field from django countries app

from .managers import LottoManager

'''Questi modelli devono essere inseriti in automatico'''
class TipoAnimale(models.Model):
    descrizione = models.CharField(max_length=10)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='animale', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["descrizione"]
        verbose_name_plural = "tipi animale"

    def __str__(self):
        return self.descrizione
    
class TipoGrezzo(models.Model):
    descrizione = models.CharField(max_length=50)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='grezzo', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["descrizione"]
        verbose_name_plural = "tipi grezzo"

    def __str__(self):
        return self.descrizione

'''Fine modelli da inserire in automatico'''
    
class Scelta(models.Model):
    descrizione = models.CharField(max_length=50)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='scelta', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["descrizione"]
        verbose_name_plural = "scelta"

    def __str__(self):
        return self.descrizione
    


    

class Lotto(models.Model):    
    data_acquisto = models.DateField(null=False, blank=False)
    identificativo = models.CharField(max_length=10, null=False, blank=False)
    fk_tipoanimale = models.ForeignKey(TipoAnimale, null=True, blank=True, on_delete=models.SET_NULL, related_name='lotto')
    fk_tipogrezzo = models.ForeignKey(TipoGrezzo, null=True, blank=True, on_delete=models.SET_NULL, related_name='lotto')
    fk_fornitore = models.ForeignKey(Fornitore, null=False, blank=False, on_delete=models.CASCADE, related_name='lotto')
    origine = CountryField(blank_label='(seleziona Paese)', null=True, blank=True)
    documento = models.CharField(max_length=10, null=True, blank=True)
    is_lwg = models.BooleanField(default=False)
    fk_macello = models.ForeignKey(FornitoreMacello, null=True, blank=True, on_delete=models.CASCADE, related_name='lotto_macello')
    peso_totale = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, )
    pezzi = models.IntegerField(null=True, blank=True)
    prezzo_unitario = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True, )
    spese_accessorie = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True, )
    kg_km = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True,
                                help_text="Moltiplicare i kg. per i km percorsi per il calcolo della CO2")
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='lotto', null=True, blank=True, on_delete=models.SET_NULL)
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
    created_by = models.ForeignKey(User, related_name='sceltalotto', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)



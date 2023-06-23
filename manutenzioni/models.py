from django.db import models
from django.urls import reverse
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from anagrafiche.models import Fornitore

class Attrezzatura(models.Model):
    codice_attrezzatura = models.CharField(max_length=10)
    descrizione = models.CharField(max_length=50)
    modello = models.CharField(max_length=100)
    serie_matricola = models.CharField(max_length=50)
    is_dismesso = models.BooleanField(default=False)
    data_dismissione = models.DateField(null=True, blank=True)
    is_taratura = models.BooleanField(default=False)
    periodo_taratura = models.CharField(max_length=50, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='attrezzatura', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__ (self):
        return self.codice_attrezzatura + " " + self.descrizione
    
class ManutenzioneStraordinaria(models.Model):
    fk_attrezzatura = models.ForeignKey(Attrezzatura, on_delete=models.CASCADE)
    data_manutenzione = models.DateField(null=False, blank=False)
    descrizione = models.CharField(max_length=100)
    importo = models.DecimalField(max_digits=8, decimal_places=3)
    ore_fermo = models.DecimalField(max_digits=6, decimal_places=2)
    fk_fornitore = models.ForeignKey(Fornitore, null=True, blank=True, on_delete=models.SET_NULL)
    ft_prot = models.CharField(max_length=20, null=True, blank=True)
    data_fattura = models.DateField(null=False, blank=False)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='manutenzione_straordinaria', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-data_manutenzione"]
        
class Taratura(models.Model):
    fk_attrezzatura = models.ForeignKey(Attrezzatura, on_delete=models.CASCADE)
    data_taratura = models.DateField(null=False, blank=False)
    fk_fornitore = models.ForeignKey(Fornitore, null=True, blank=True, on_delete=models.SET_NULL)
    documento= models.FileField(upload_to='tarature/', null=True, blank=True)
    is_conforme = models.BooleanField(default=True)
    prossima_scadenza = models.DateField(null=False, blank=False)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='taratura', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-data_taratura"]
        
        
class ManutenzioneOrdinaria(models.Model):
    fk_attrezzatura = models.ForeignKey(Attrezzatura, on_delete=models.CASCADE)
    data_manutenzione = models.DateField(null=False, blank=False)
    descrizione = models.CharField(max_length=100)    
    fk_fornitore = models.ForeignKey(Fornitore, null=True, blank=True, on_delete=models.SET_NULL)
    is_eseguita = models.BooleanField(default=False)
    prossima_scadenza = models.DateField(null=False, blank=False)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='manutenzione_ordinaria', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-data_manutenzione"]
        
    
    
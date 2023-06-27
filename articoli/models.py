from django.db import models
from anagrafiche.models import Fornitore
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
from acquistopelli.models import TipoAnimale, TipoGrezzo

class Articolo(models.Model):
    # Industrie fornite
    APPAREL_CLOTHING = 'apparel/clothing'
    AUTOMOTIVE = 'automotive'
    CONTRACT = 'contract'
    FOOTWEAR = 'footwear'
    FOOTWEAR_ATHLETIC = 'footwear (athletic)'
    LEATHER_GOODS = 'leather goods'
    UPHOLSTERY = 'upholstery'
    
    
    CHOICES_INDUSTRIES_SERVED = (
        (APPAREL_CLOTHING, 'Apparel/clothing'),
        (AUTOMOTIVE, 'Automotive'),        
        (CONTRACT, 'Contract'),
        (FOOTWEAR, 'Footwear'),
        (FOOTWEAR_ATHLETIC, 'Footwear (Athletic)'),
        (LEATHER_GOODS, 'Leather goods'),
        (UPHOLSTERY, 'Upholstery')
    )
    
    descrizione = models.CharField(max_length=100)
    scheda_tecnica = models.FileField(upload_to='schede_tecniche_articoli/', null=True, blank=True)
    industries_served = models.CharField(max_length=50, choices=CHOICES_INDUSTRIES_SERVED, null=True, blank=True)
    fk_tipoanimale = models.ForeignKey(TipoAnimale, null=True, blank=True, on_delete=models.SET_NULL, related_name='articolo')
    fk_tipogrezzo = models.ForeignKey(TipoGrezzo, null=True, blank=True, on_delete=models.SET_NULL, related_name='articolo')
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='articolo', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["descrizione"]
        verbose_name_plural = "articoli"

    def __str__(self):
        return self.descrizione
    
class Colore(models.Model):
    descrizione = models.CharField(max_length=100)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='colore', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["descrizione"]
        verbose_name_plural = "colori"

    def __str__(self):
        return self.descrizione
    
class FaseLavoro(models.Model):
    # Unità di misura
    MQ = 'mq'
    NUMERO = 'Nr.'
    PESO_KG = 'Kg.'
    
    
    CHOICES_UM = (
        (MQ, 'Mq.'),
        (NUMERO, 'Nr.'),
        (PESO_KG, 'Kg.'),
        
    )
    descrizione = models.CharField(max_length=100)    
    um =  models.CharField(max_length=100, choices=CHOICES_UM, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='faselavoro', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["descrizione"]
        verbose_name_plural = "fasi lavoro"

    def __str__(self):
        return self.descrizione
    
    
class Procedura(models.Model):
    fk_articolo = models.ForeignKey(Articolo, on_delete=models.CASCADE)
    nr_procedura = models.IntegerField()
    data_procedura = models.DateField(default=timezone.now)
    nr_revisione = models.IntegerField()
    data_revisione = models.DateField(default=timezone.now)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='procedure', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.fk_articolo + " Procedura Nr. " + str(self.nr_procedura) + " del " + str(self.data_procedura) + " Revisione nr. " + str(self.nr_revisione) + " del " + str(self.data_revisione)
    
class DettaglioProcedura(models.Model):
    fk_procedura = models.ForeignKey(Procedura, on_delete=models.CASCADE)
    fk_faselavoro = models.ForeignKey(FaseLavoro, on_delete=models.CASCADE)    
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='dettaglioprocedura', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    
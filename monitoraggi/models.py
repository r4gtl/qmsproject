from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class MonitoraggioAcqua(models.Model):
    data_lettura = models.DateField(null=False, blank=False)
    mc_in = models.IntegerField()
    mc_out = models.IntegerField()
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='MonitoraggioAcqua', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-data_lettura"]

class MonitoraggioGas(models.Model):
    data_lettura = models.DateField(null=False, blank=False)
    mc_in = models.IntegerField()    
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='MonitoraggioGas', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-data_lettura"]

class MonitoraggioEnergiaElettrica(models.Model):
    data_lettura = models.DateField(null=False, blank=False)
    kwh_in = models.IntegerField()    
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='MonitoraggioEnergiaElettrica', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-data_lettura"]

class DatoProduzione(models.Model):
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
    data_inserimento = models.DateField(null=False, blank=False)
    industries_served = models.CharField(max_length=50, choices=CHOICES_INDUSTRIES_SERVED)    
    n_pelli = models.IntegerField()
    mq = models.DecimalField(max_digits=8, decimal_places=3)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='dati_produzione', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-data_inserimento"]



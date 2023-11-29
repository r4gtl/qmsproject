from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.db import models


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
    mc_in = models.DecimalField(max_digits=8, decimal_places=3)   
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='MonitoraggioGas', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-data_lettura"]
    
    @classmethod
    def somma_gas_ultimo_anno(cls):
        # Calcola la data di un anno fa
        data_oggi = datetime.today()
        data_anno_precedente = data_oggi - timedelta(days=365)

        # Esegue la query per ottenere la somma del campo da sommare
        somma = cls.objects.filter(data_lettura__gte=data_anno_precedente).aggregate(total=models.Sum('mc_in'))['total']

        # Verifica se la somma è None (nessun record trovato)
        if somma is None:
            somma = 0

        return somma
    
    @classmethod
    def somma_gas_ultimo_anno_per_mese(cls):
        # Calcola la data di un anno fa
        data_oggi = datetime.today()
        data_anno_precedente = data_oggi - timedelta(days=365)

        # Esegue la query per ottenere la somma dei mc_in raggruppati per mese
        somme_mese_gas = cls.objects.filter(data_lettura__gte=data_anno_precedente) \
            .annotate(mese=models.functions.TruncMonth('data_lettura')) \
            .values('mese') \
            .annotate(somma=models.Sum('mc_in')) \
            .order_by('mese')

        return somme_mese_gas
    
    @classmethod
    def somma_gas_per_intervallo(cls, data_inizio, data_fine):
        somme_mese_intervallo = cls.objects.filter(data_lettura__range=[data_inizio, data_fine]) \
        .values('mese') \
        .annotate(somma=models.Sum('mc_in')) \
        .order_by('mese')

        return somme_mese_intervallo



class MonitoraggioEnergiaElettrica(models.Model):
    data_lettura = models.DateField(null=False, blank=False)
    kwh_in = models.DecimalField(max_digits=9, decimal_places=3)    
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='MonitoraggioEnergiaElettrica', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-data_lettura"]
    
    @classmethod
    def somma_energia_ultimo_anno(cls):
        # Calcola la data di un anno fa
        data_oggi = datetime.today()
        data_anno_precedente = data_oggi - timedelta(days=365)

        # Esegue la query per ottenere la somma del campo da sommare
        somma = cls.objects.filter(data_lettura__gte=data_anno_precedente).aggregate(total=models.Sum('kwh_in'))['total']

        # Verifica se la somma è None (nessun record trovato)
        if somma is None:
            somma = 0

        return somma
    
    @classmethod
    def somma_energia_ultimo_anno_per_mese(cls):
        # Calcola la data di un anno fa
        data_oggi = datetime.today()
        data_anno_precedente = data_oggi - timedelta(days=365)

        # Esegue la query per ottenere la somma dei mc_in raggruppati per mese
        somme_mese_energia = cls.objects.filter(data_lettura__gte=data_anno_precedente) \
            .annotate(mese=models.functions.TruncMonth('data_lettura')) \
            .values('mese') \
            .annotate(somma=models.Sum('kwh_in')) \
            .order_by('mese')

        return somme_mese_energia
    
    @classmethod
    def somma_energia_per_intervallo(cls, data_inizio, data_fine):
        somma_energia_per_intervallo = cls.objects.filter(data_lettura__range=[data_inizio, data_fine]) \
            .values('mese') \
            .annotate(somma=models.Sum('kwh_in')) \
            .order_by('mese')

        return somma_energia_per_intervallo


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
    kg = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='dati_produzione', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-data_inserimento"]

    @classmethod
    def somma_produzione_ultimo_anno(cls, campo_sommabile):
        # Calcola la data di un anno fa
        data_oggi = datetime.today()
        data_anno_precedente = data_oggi - timedelta(days=365)

        # Esegue la query per ottenere la somma del campo da sommare
        somma = cls.objects.filter(data_inserimento__gte=data_anno_precedente).aggregate(total=models.Sum(campo_sommabile))['total']

        # Verifica se la somma è None (nessun record trovato)
        if somma is None:
            somma = 0

        return somma
    
    @classmethod
    def somma_produzione_ultimo_anno_per_mese(cls):
        # Calcola la data di un anno fa
        data_oggi = datetime.today()
        data_anno_precedente = data_oggi - timedelta(days=365)

        somma_produzione_ultimo_anno_per_mese = cls.objects.filter(data_inserimento__gte=data_anno_precedente) \
            .annotate(mese=models.functions.TruncMonth('data_inserimento')) \
            .values('mese') \
            .annotate(somma=models.Sum('mq')) \
            .order_by('mese')
        
        return somma_produzione_ultimo_anno_per_mese
    
    
    @classmethod
    def somma_produzione_per_intervallo(cls, campo_sommabile, data_inizio, data_fine):
        somma_produzione_per_intervallo = cls.objects.filter(data_inserimento__range=[data_inizio, data_fine]) \
            .annotate(mese=models.functions.TruncMonth('data_inserimento')) \
            .values('mese') \
            .annotate(somma=models.Sum(campo_sommabile)) \
            .order_by('mese')
        
        return somma_produzione_per_intervallo


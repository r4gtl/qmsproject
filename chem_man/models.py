from django.db import models
import os
from anagrafiche.models import Fornitore
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

class ProdottoChimico(models.Model):
    # Reparto
    BAGNATO = 'bagnato'
    RIFINIZIONE = 'rifinizione'   
    CHOICES_REPARTO = (
        (BAGNATO, 'Bagnato'),
        (RIFINIZIONE, 'Rifinizione')        
    )
    
    # Classe Infiammabilità
    MOLTO_INFIAMMABILI = 'A - Liquidi molto infiammabili'
    INFIAMMABILI = 'B - Liquidi infiammabili' 
    COMBUSTIBILI = 'C - Liquidi combustibili' 
    NON_INFIAMMABILI = 'Non infiammabili' 
    
    CHOICES_FLAME = (
        (MOLTO_INFIAMMABILI, 'A - Liquidi molto infiammabili'),
        (INFIAMMABILI, 'B - Liquidi infiammabili'),        
        (COMBUSTIBILI, 'C - Liquidi combustibili'),        
        (NON_INFIAMMABILI, 'Non infiammabili')       
    )
    
    # ZDHC Level
    REGISTERED = 'registered'
    LEVEL_1 = 'level 1'
    LEVEL_2 = 'level 2'
    LEVEL_3 = 'level 3'
    
    CHOICES_ZDHC = (
        (REGISTERED, 'Registered'),
        (LEVEL_1, 'Level 1'),
        (LEVEL_2, 'Level 2'),
        (LEVEL_3, 'Level 3')
    )
    
    fk_fornitore = models.ForeignKey(
        Fornitore, related_name='prodotto_chimico',
        limit_choices_to={'categoria': Fornitore.PRODOTTI_CHIMICI},
        on_delete=models.CASCADE
    )
    descrizione = models.CharField(max_length=100)
    solvente = models.DecimalField(max_digits=5, decimal_places=2)
    reparto = models.CharField(max_length=12, choices=CHOICES_REPARTO, null=True, blank=True)
    flame_class = models.CharField(max_length=50, choices=CHOICES_FLAME, null=True, blank=True)
    zdhc_level = models.CharField(max_length=50, choices=CHOICES_ZDHC, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='prodotto_chimico', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-descrizione"]
        
    def __str__(self):
        return self.descrizione
    
    @classmethod
    def get_ultimo_prezzo(cls):
        prezzo_ultimo = None
        prodotto = cls.objects.first()
        if prodotto:
            ultimo_prezzo = prodotto.prezzo.order_by('-data_inserimento').first()
            if ultimo_prezzo:
                prezzo_ultimo = ultimo_prezzo.prezzo
        return prezzo_ultimo
    
class PrezzoProdotto(models.Model):
    fk_prodottochimico = models.ForeignKey(
            ProdottoChimico,
            on_delete=models.CASCADE,
            related_name='prezzo'
            )
    data_inserimento = models.DateField(default=date.today)
    prezzo = models.DecimalField(max_digits=8, decimal_places=3)    
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='prezzi_prodotti_chimici', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-data_inserimento"]
        
    def __str__(self):
        return f"Prezzo: {self.prezzo} - Data inserimento: {self.data_inserimento}"
    
    
def schedatecnica_upload_path(instance, filename):
    forn_ragione_sociale = instance.fk_prodottochimico.fk_fornitore.ragionesociale
    prodotto_descrizione = instance.fk_prodottochimico.descrizione
    base_path = 'SchedeTecniche'
    file_extension = os.path.splitext(filename)[1]
    new_filename = f"{forn_ragione_sociale}_{prodotto_descrizione}_{instance.id}{file_extension}"
    return os.path.join(base_path, new_filename)


class SchedaTecnica(models.Model):
    fk_prodottochimico = models.ForeignKey(
        ProdottoChimico,
        on_delete=models.CASCADE,
        related_name='schede_tecniche'
    )
    data_inserimento = models.DateField(default=date.today)
    documento=models.FileField(upload_to=schedatecnica_upload_path, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
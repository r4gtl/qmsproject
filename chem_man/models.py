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
    
    @property
    def ultimo_prezzo(self):
        ultimo_prezzo = self.prezzo.order_by('-data_inserimento').first()
        if ultimo_prezzo:
            return ultimo_prezzo.prezzo
        return None
    
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
    base_path = 'Prodotti_Chimici'
    file_extension = os.path.splitext(filename)[1]
    new_filename = f"{forn_ragione_sociale}/{prodotto_descrizione}/SchedeTecniche/{filename}{file_extension}"
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



class Sostanza(models.Model):
    descrizione = models.CharField(max_length=500)
    num_cas = models.CharField(max_length=20, blank=True, null=True)
    num_ec = models.CharField(max_length=20, blank=True, null=True)
    num_reach = models.CharField(max_length=20, blank=True, null=True)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='sostanze', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["descrizione"]
        
    def __str__(self):
        return self.descrizione
    

class SostanzaSVHC(models.Model):
    descrizione = models.CharField(max_length=500)
    data_inclusione=models.DateField()
    num_cas = models.CharField(max_length=20, blank=True, null=True)
    num_ec = models.CharField(max_length=20, blank=True, null=True)
    num_reach = models.CharField(max_length=20, blank=True, null=True)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='sostanze_svhc', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["descrizione"]
        
    def __str__(self):
        return self.descrizione
    
class HazardStatement(models.Model):

    # Classe Pericolo
    FISICI = 'Pericoli Fisici'
    SALUTE = 'Pericoli per la Salute' 
    AMBIENTE = 'Pericoli per l\'Ambiente' 
    SUPPLEMENTARI = 'Pericoli Supplementari' 
    
    CHOICES_HAZARD_CAT = (
        (FISICI, 'Pericoli Fisici'),
        (SALUTE, 'Pericoli per la Salute'),        
        (AMBIENTE, 'Pericoli per l\'Ambiente'),        
        (SUPPLEMENTARI, 'Pericoli Supplementari')       
    )
    
    hazard_statement = models.CharField(max_length=20)
    descrizione = models.CharField(max_length=100, null=True, blank=True)
    hazard_category = models.CharField(max_length=50, choices=CHOICES_HAZARD_CAT, null=True, blank=True)
    is_dangerous = models.BooleanField(default=False)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='hazard_statement', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["hazard_statement"]
        
    def __str__(self):
        return self.hazard_statement + " " + self.descrizione
    

class PrecautionaryStatement(models.Model):
    codice = models.CharField(max_length=20)
    descrizione = models.CharField(max_length=200)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='precautionary_statement', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)



class SimboloGHS(models.Model):
    codice = models.CharField(max_length=10)
    descrizione = models.TextField(null=True, blank=True)
    symbol_image = models.ImageField(upload_to='static/ghs_symbols/', null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='simbolo_ghs', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)




def schedasicurezza_upload_path(instance, filename):
    forn_ragione_sociale = instance.fk_prodottochimico.fk_fornitore.ragionesociale
    prodotto_descrizione = instance.fk_prodottochimico.descrizione
    base_path = 'Prodotti_Chimici'
    file_extension = os.path.splitext(filename)[1]
    new_filename = f"{forn_ragione_sociale}/{prodotto_descrizione}/SDS/{filename}{file_extension}"
    return os.path.join(base_path, new_filename)


class SchedaSicurezza(models.Model):
    
    fk_prodottochimico = models.ForeignKey(
            ProdottoChimico,
            on_delete=models.CASCADE,
            related_name='sds'
            )
    data_revisione = models.DateField()
    is_reach = models.BooleanField(default=True)  
    documento=models.FileField(upload_to=schedasicurezza_upload_path, null=True, blank=True)  
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='sds', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-data_revisione"]
        
    def __str__(self):
        return f"Sds revisione del: {self.data_revisione}"
    

class SimboloGHS_SDS(models.Model):
    fk_sds = models.ForeignKey(
            SchedaSicurezza,
            on_delete=models.CASCADE,
            related_name='simbolo_ghs_sds'
            )
    fk_simbolo_ghs = models.ForeignKey(
            SimboloGHS,
            on_delete=models.CASCADE,
            related_name='simbolo_ghs_sds'
            )
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='simbolo_ghs_sds', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)


class PrecautionaryStatement_SDS(models.Model):
    fk_sds = models.ForeignKey(
            SchedaSicurezza,
            on_delete=models.CASCADE,
            related_name='precautionary_statement_sds'
            )
    fk_precautionary_statement = models.ForeignKey(
            PrecautionaryStatement,
            on_delete=models.CASCADE,
            related_name='precautionary_statement_sds'
            )
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='precautionary_statement_sds', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)


class HazardStatement_SDS(models.Model):
    fk_sds = models.ForeignKey(
            SchedaSicurezza,
            on_delete=models.CASCADE,
            related_name='hazard_statement_sds'
            )
    fk_hazard_statement = models.ForeignKey(
            HazardStatement,
            on_delete=models.CASCADE,
            related_name='hazard_statement_sds'
            )
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='hazard_statement_sds', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)



class Sostanza_SDS(models.Model):
    fk_sds = models.ForeignKey(
            SchedaSicurezza,
            on_delete=models.CASCADE,
            related_name='sostanza_sds'
            )
    fk_sostanza = models.ForeignKey(
            Sostanza,
            on_delete=models.CASCADE,
            related_name='sostanza_sds'
            )
    concentrazione = models.CharField(max_length=50)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='sostanza_sds', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    
    


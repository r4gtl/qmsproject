from django.db import models
from django.contrib.auth.models import User


class CodiceCER(models.Model):
    codice = models.CharField(max_length=7, null=False, blank=False)
    descrizione = models.CharField(max_length=100, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='codice_cer', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.codice
    


class CodiceSmaltRec(models.Model):

    # Smaltimento o Recupero
    SMALTIMENTO = 'smaltimento'
    RECUPERO = 'recupero'
    
    
    CHOICES_SMALT_REC = (
        (SMALTIMENTO, 'Smaltimento'),
        (RECUPERO, 'Recupero'),        
    )
    codice = models.CharField(max_length=4, null=False, blank=False)
    descrizione = models.CharField(max_length=100, null=True, blank=True)
    smalt_rec =  models.CharField(max_length=15, choices=CHOICES_SMALT_REC)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='codice_smalt_rec', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.codice
    

class MovimentoRifiuti(models.Model):

    # Carico o Scarico
    CARICO = 'carico'
    SCARICO = 'scarico'
    
    
    CHOICES_CAR_SCAR = (
        (CARICO, 'Carico'),
        (SCARICO, 'Scarico'),        
    )

    data_movimento = models.DateField()
    fk_codicecer = models.ForeignKey(CodiceCER, on_delete=models.CASCADE, related_name='movimento_rifiuti')
    car_scar =  models.CharField(max_length=7, choices=CHOICES_CAR_SCAR)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    fk_smaltrec = models.ForeignKey(CodiceSmaltRec, on_delete=models.CASCADE, related_name='movimento_rifiuti', null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='movimento_rifiuti', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-data_movimento"]
        verbose_name_plural = "Movimenti Rifiuti"

    def __str__(self):
        return str(self.data_movimento)


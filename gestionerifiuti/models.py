from django.db import models
from django.contrib.auth.models import User


class CodiceCER(models.Model):
    codice = models.CharField(max_length=7, null=False, blank=False)
    descrizione = models.CharField(max_length=100, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='codice_cer', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

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
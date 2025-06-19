from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class PuntoEmissione(models.Model):
    camino_numero  = models.CharField(max_length=50, blank=False, null=False)
    origine = models.CharField(max_length=50, blank=False, null=False,
                               help_text="P.E.: cabina rifinizione pelli, depolveratore linea...")
    descrizione_origine = models.TextField(null=True, blank=True,
                                           help_text="Aggiungi una breve descrizione dell'origine.")
    quota = models.CharField(max_length=50, blank=True, null=True)
    
    portata = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True,
                               help_text="Nm3/h")
    parametri = models.CharField(max_length=50, blank=True, null=True,
                               help_text="P.E.: polveri")
    limite_conc = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True,
                               help_text="mg/Nm3")
    limite_flusso = models.DecimalField(max_digits=8, decimal_places=2,  blank=True, null=True,
                               help_text="g/h")
    tipo_abbattimento = models.CharField(max_length=50, blank=True, null=True,
                               help_text="P.E.: Ad umido, filtri a secco...")
    soggetto_controllo = models.BooleanField(default=False)
    autorizzazione = models.CharField(max_length=100, blank=True, null=True)
    is_disabled = models.BooleanField(default=False)

    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='punto_emissione', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["camino_numero"]
        verbose_name_plural = "Punti di Emissione"

    def __str__ (self):
        return self.camino_numero 
    
class RegistroControlloAnalitico(models.Model):
    fk_punto_emissione = models.ForeignKey(PuntoEmissione, related_name='registro_controllo_analitico', null=False, blank=False, on_delete=models.CASCADE)
    data_prelievo = models.DateField(null=False, blank=False)
    prossima_scadenza = models.DateField(null=True, blank=True) 
    portata_risc = models.DecimalField(max_digits=9, decimal_places=2,  blank=True, null=True,
                               help_text="Nm3/h")
    conc_risc = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True,
                               help_text="mg/Nm3")
    flusso_risc = models.DecimalField(max_digits=8, decimal_places=2,  blank=True, null=True,
                               help_text="g/h")
    certificato_numero  = models.CharField(max_length=50, blank=True, null=True)
    certificato = models.FileField(upload_to='analisi_fumi/', null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='registro_controllo_analitico', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["data_prelievo"]
        verbose_name_plural = "Registri controlli analitici"

    def __str__ (self):
        return self.data_prelievo

    
    

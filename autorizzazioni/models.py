from django.db import models
from django.contrib.auth.models import User

class Autorizzazione(models.Model):
    descrizione = models.CharField(max_length=100, null=False, blank=False, help_text="Descrizione")
    rilasciata_da = models.CharField(max_length=100, null=False, blank=False, help_text="Rilasciata da")
    n_autorizzazione = models.CharField(max_length=100, null=True, blank=True, help_text="Identificativo")
    data_autorizzazione = models.DateField(null=True, blank=True)
    frequenza_scadenza = models.CharField(max_length=50, null=True, blank=True, help_text="Frequenza")
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='autorizzazioni', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data_autorizzazione']

    def __str__ (self):
        return self.descrizione + " del " + str(self.data_autorizzazione)
    
    
class DettaglioScadenzaAutorizzazione(models.Model):
    fk_autorizzazione = models.ForeignKey(Autorizzazione, on_delete=models.CASCADE)
    n_rinnovo = models.CharField(max_length=100, null=False, blank=False, help_text="numero autorizzazione")
    data_rinnovo = models.DateField(null=True, blank=True)
    scadenza_rinnovo = models.DateField(null=True, blank=True)
    is_rinnovata = models.BooleanField(default=False)
    documento= models.FileField(upload_to='autorizzazioni/', null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='dettaglio_scadenze_autorizzazioni', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data_rinnovo']
        get_latest_by = ['data_rinnovo']


class ParametroAutorizzazione(models.Model):
    descrizione = models.CharField(max_length=100, null=False, blank=False, help_text="descrizione")
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='parametro_autorizzazione', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['descrizione']

    def __str__ (self):
        return self.descrizione
    

class CampoApplicazione(models.Model):
    fk_autorizzazione = models.ForeignKey(Autorizzazione, null=True, blank=True, on_delete=models.SET_NULL)
    descrizione=models.CharField(max_length=100, null=False, blank=False, help_text="descrizione")
    is_applicabile = models.BooleanField(default=False)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='campo_applicazione', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['descrizione']

    def __str__ (self):
        return self.descrizione
    

class DettaglioCampoApplicazione(models.Model):
    fk_parametro = models.ForeignKey(ParametroAutorizzazione, on_delete=models.CASCADE)
    fk_campoapplicazione = models.ForeignKey(CampoApplicazione, on_delete=models.CASCADE)
    um = models.CharField(max_length=10, null=True, blank=True, help_text="unità_misura")
    limite = models.DecimalField(max_digits=10, decimal_places=3)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='dettaglio_campo_applicazione', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)




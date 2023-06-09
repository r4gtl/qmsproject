from django.db import models
from django_countries.fields import CountryField # Field from django countries app
from anagrafiche.models import Fornitore
from django.contrib.auth.models import User


class TipoAnimale(models.Model):
    descrizione = models.CharField(max_length=10)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='animale', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["descrizione"]
        verbose_name_plural = "tipi animale"

    def __str__(self):
        return self.descrizione
    
class TipoGrezzo(models.Model):
    descrizione = models.CharField(max_length=10)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='grezzo', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["descrizione"]
        verbose_name_plural = "tipi grezzo"

    def __str__(self):
        return self.descrizione
    
class Scelta(models.Model):
    descrizione = models.CharField(max_length=50)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='scelta', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["descrizione"]
        verbose_name_plural = "scelta"

    def __str__(self):
        return self.descrizione
    


class Lotto(models.Model):    
    data_acquisto = models.DateField(null=False, blank=False)
    identificativo = models.CharField(max_length=10, null=False, blank=False)
    fk_tipoanimale = models.ForeignKey(TipoAnimale, null=True, blank=True, on_delete=models.SET_NULL)
    fk_tipogrezzo = models.ForeignKey(TipoGrezzo, null=True, blank=True, on_delete=models.SET_NULL)
    fk_fornitore = models.ForeignKey(Fornitore, null=False, blank=False, on_delete=models.CASCADE)
    origine = CountryField(blank_label='(seleziona Paese)', null=True, blank=True)
    documento = models.CharField(max_length=10, null=True, blank=True)
    is_lwg = models.BooleanField(default=False)
    pezzi = models.IntegerField(null=True, blank=True)
    prezzo_unitario = models.DecimalField(max_digits=8, decimal_places=3)
    spese_accessorie = models.DecimalField(max_digits=10, decimal_places=3)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='lotto', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-data_acquisto"]
        verbose_name_plural = "Lotti"

    def __str__(self):
        return self.data_acquisto + " " + self.identificativo
    

    
class SceltaLotto(models.Model):
    fk_lotto = models.ForeignKey(Lotto, null=False, blank=False, on_delete=models.CASCADE)
    fk_scelta = models.ForeignKey(Scelta, null=False, blank=False, on_delete=models.CASCADE)
    pezzi = models.IntegerField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='sceltalotto', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)



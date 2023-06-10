from django.db import models
from anagrafiche.models import Fornitore
from django.contrib.auth.models import User

class Articolo(models.Model):
    descrizione = models.CharField(max_length=100)
    scheda_tecnica = models.FileField(upload_to='schede_tecniche_articoli/', null=True, blank=True)
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
    descrizione = models.CharField(max_length=100)    
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='faselavoro', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["descrizione"]
        verbose_name_plural = "fasi lavoro"

    def __str__(self):
        return self.descrizione
    


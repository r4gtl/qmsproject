from django.db import models
from django.urls import reverse
import datetime
from django.utils import timezone
from django.contrib.auth.models import User

class SezioneLWG(models.Model):
    lwgsection = models.CharField(max_length=100)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='lwg_sections', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.lwgsection



class Procedura(models.Model):
    identificativo = models.CharField(max_length=50)
    data_procedura = models.DateField(null=False, blank=False)
    descrizione = models.CharField(max_length=100)
    is_eliminata = models.BooleanField(default=False)
    fk_lwgsection = models.ForeignKey(SezioneLWG, null=True, blank=True, on_delete=models.SET_NULL)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='procedura', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.identificativo + " " + str(self.data_procedura)
    

class RevisioneProcedura(models.Model):
    fk_procedura = models.ForeignKey(Procedura, on_delete=models.CASCADE)
    n_revisione = models.IntegerField()
    data_revisione = models.DateField(default=timezone.now)
    documento = models.FileField(upload_to='procedure/', null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='revisione_procedura', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-data_revisione"]
        get_latest_by = ['data_revisione']

    def __str__(self):
        return f"Revisione {self.n_revisione} - Procedura {self.fk_procedura.identificativo}"
    
    


class Modulo(models.Model):
    fk_procedura = models.ForeignKey(Procedura, on_delete=models.CASCADE)
    identificativo = models.CharField(max_length=50)
    data_modulo = models.DateField(null=False, blank=False)
    descrizione = models.CharField(max_length=100)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='modulo', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-data_modulo"]



class RevisioneModulo(models.Model):
    fk_modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)    
    n_revisione = models.IntegerField()
    data_revisione = models.DateField(default=timezone.now)
    documento = models.FileField(upload_to='procedure/moduli/', null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='revisione_modulo', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-data_revisione"]
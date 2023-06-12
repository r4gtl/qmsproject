from django.db import models
from django.urls import reverse
import datetime
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
        return self.identificativo + " " + self.data_procedura


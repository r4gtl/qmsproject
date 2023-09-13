from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Estintore(models.Model):
    tipo_estinguente = models.CharField(max_length=100)
    classe = models.CharField(max_length=100)
    peso = models.CharField(max_length=100)
    matricola = models.CharField(max_length=100)
    anno = models.CharField(max_length=4)
    ubicazione = models.CharField(max_length=200)
    data_dismissione = models.DateField(null=True, blank=True)
    numero_posizione = models.IntegerField()
    scadenza_revisione = models.DateField()
    scadenza_collaudo = models.DateField()


    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='estintore', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["numero_posizione"]

    def __str__(self):
        return f"{self.matricola} - {self.numero_posizione}"
    

class ControlloPeriodicoEstintore(models.Model):
    # Inserire i dati dei controlli periodici sia interni che da ditta esterna e sfrutta il campo scadenza per lo scadenzario    
     # Tipo Controllo
    INTERNO = 'interno'
    PROGRAMMATO = 'programmato'
        
    CHOICES_CONTROL = (
        (INTERNO, 'Interno'),
        (PROGRAMMATO, 'Programmato (Ditta Esterna)')        
    )

    fk_estintore = models.ForeignKey(Estintore, related_name='controllo_periodico_estintore', on_delete=models.CASCADE)
    tipo_controllo = models.CharField(max_length=30, choices=CHOICES_CONTROL)
    scadenza = models.DateField()
    eseguita = models.BooleanField(default=False)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='controllo_periodico_estintore', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-scadenza"]



    

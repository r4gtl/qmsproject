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

class Idrante(models.Model):
    
     # Tipo Idrante
    IP = 'idrante a parete'
    ISS = 'Idrante soprasuolo'
    ICS = 'Idrante a colonna soprasuolo'
    GFS = 'Gruppo fisso schiuma'
    GMS = 'Gruppo mobile schiuma'
    AVVF = 'Attacco autopompa VVF'
    AQ = 'Alimentazione acquedotto'
    AP = 'Alimentazione con pompe'
    EVF = 'Evacuatori di fumo'
    N = 'Naspo'
        
    CHOICES_TYPE = (
        (IP, 'Interno'),
        (ISS, 'Idrante soprasuolo'),     
        (ICS, 'Idrante a colonna soprasuolo'),     
        (GFS, 'Gruppo fisso schiuma'),     
        (GMS, 'Gruppo mobile schiuma'),     
        (AVVF, 'Attacco autopompa VVF'),     
        (AQ, 'Alimentazione acquedotto'),     
        (AP, 'Alimentazione con pompe'),     
        (EVF, 'Evacuatori di fumo'),     
        (N, 'Naspo'),     
    )

    numero_posizione = models.IntegerField()
    tipo_idrante = models.CharField(max_length=35, choices=CHOICES_TYPE)
    uni = models.CharField(max_length=4, blank=True, null=True)
    metri = models.CharField(max_length=4, blank=True, null=True)
    anno = models.CharField(max_length=4)
    data_dismissione = models.DateField(null=True, blank=True)
    scadenza_schiuma = models.DateField(null=True, blank=True)
    scadenza_collaudo = models.DateField()
    ubicazione = models.CharField(max_length=200)


    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='idrante', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["numero_posizione"]

    def __str__(self):
        return f"{self.numero_posizione} - {self.tipo_idrante}"
    

    
class PortaUscita(models.Model):

    # Porte/Uscite
    AS = 'portone scorrevole'
    N = 'normale'
    TF = 'tagliafuoco'
    US = 'uscita di sicurezza'
    
        
    CHOICES_DOOR = (
        (AS, 'Portone scorrevole'),
        (N, 'Normale'),     
        (TF, 'Tagliafuoco'),     
        (US, 'Uscita di sicurezza')  
           
    )

    # Maniglioni
    MAP = 'maniglione antipanico'
    MAN = 'maniglia'  
        
    CHOICES_HANDLE = (
        (MAP, 'Maniglione Antipanico'),
        (MAN, 'Maniglia')
    )

    # Ante
    A = 'anta normale'
    A2 = 'due ante'  
    AS = 'portone scorrevole'  
        
    CHOICES_ANTE = (
        (A, 'Anta normale'),
        (A2, 'Due ante'),
        (AS, 'Portone scorrevole'),
    )

    numero_posizione = models.IntegerField()
    tipo_porta = models.CharField(max_length=35, choices=CHOICES_DOOR)
    marcatura_ce = models.BooleanField(default=False)
    maniglia = models.CharField(max_length=35, choices=CHOICES_HANDLE)
    anta = models.CharField(max_length=35, choices=CHOICES_ANTE)
    matricola = models.CharField(max_length=100, null=True, blank=True)
    ubicazione = models.CharField(max_length=200, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='porta', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["numero_posizione"]

    def __str__(self):
        return f"{self.numero_posizione} - {self.tipo_porta}"
    
    
class ImpiantoSpegnimento(models.Model):
    numero_posizione = models.IntegerField()
    ubicazione = models.CharField(max_length=200, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='impianto', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["numero_posizione"]



class AttrezzaturaAntincendio(models.Model):
    descrizione = models.CharField(max_length=200, null=True, blank=True)
    






    

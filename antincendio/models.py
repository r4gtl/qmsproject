from django.db import models
from django.contrib.auth.models import User
from anagrafiche.models import Fornitore
from human_resources.models import HumanResource


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
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='attrezzatura_antincendio', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    



# Registro Manutenzioni e Controlli
class RegistroControlliAntincendio(models.Model):

    # Controllo Interno/Esterno
    INTERNO = 'interno'
    ESTERNO = 'esterno'  
        
    CHOICES_INT_EST = (
        (INTERNO, 'Interno'),
        (ESTERNO, 'Esterno')
    )

    interno_esterno = models.CharField(max_length=35, choices=CHOICES_INT_EST)
    fk_fornitore = models.ForeignKey(Fornitore, related_name='registro_controlli_antincendio', null=True, blank=True, on_delete=models.CASCADE)
    fk_operatore = models.ForeignKey(HumanResource, related_name='registro_controlli_antincendio', null=True, blank=True, on_delete=models.CASCADE)
    numero_intervento = models.CharField(max_length=10, null=True, blank=True)
    data_intervento = models.DateField()
    prossima_scadenza = models.DateField()
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='registro_controlli_antincendio', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)


# Creo un dettaglio registro per ogni tipologia di attrezzatura
class DettaglioRegistroEstintore(models.Model):
    fk_registro = models.ForeignKey(Fornitore, related_name='dettaglio_registro_estintore', on_delete=models.CASCADE)
    fk_estintore = models.ForeignKey(Estintore, related_name='dettaglio_registro_estintore', on_delete=models.CASCADE)
    manutenzione_effettuata = models.BooleanField(default=False)
    controllo_effettuato = models.BooleanField(default=False)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='dettaglio_registro_estintore', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dettaglio del registro per {self.fk_estintore}"
    

class DettaglioRegistroIdrante(models.Model):
    fk_registro = models.ForeignKey(Fornitore, related_name='dettaglio_registro_idrante', on_delete=models.CASCADE)
    fk_idrante = models.ForeignKey(Idrante, related_name='dettaglio_registro_idrante', on_delete=models.CASCADE)
    manutenzione_effettuata = models.BooleanField(default=False)
    controllo_effettuato = models.BooleanField(default=False)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='dettaglio_registro_idrante', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dettaglio del registro per {self.fk_idrante}"
    

class DettaglioRegistroPortaUscita(models.Model):
    fk_registro = models.ForeignKey(Fornitore, related_name='dettaglio_registro_porta_uscita', on_delete=models.CASCADE)
    fk_porta_uscita = models.ForeignKey(PortaUscita, related_name='dettaglio_registro_porta_uscita', on_delete=models.CASCADE)
    manutenzione_effettuata = models.BooleanField(default=False)
    controllo_effettuato = models.BooleanField(default=False)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='dettaglio_registro_porta_uscita', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dettaglio del registro per {self.fk_porta_uscita}"
    

class DettaglioRegistroImpiangoSpegnimento(models.Model):
    fk_registro = models.ForeignKey(Fornitore, related_name='dettaglio_registro_impianto_spegnimento', on_delete=models.CASCADE)
    fk_impianto = models.ForeignKey(ImpiantoSpegnimento, related_name='dettaglio_registro_impianto_spegnimento', on_delete=models.CASCADE)
    manutenzione_effettuata = models.BooleanField(default=False)
    controllo_effettuato = models.BooleanField(default=False)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='dettaglio_registro_impianto_spegnimento', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dettaglio del registro per {self.fk_impianto}"
    

class DettaglioRegistroAttrezzaturaAntincendio(models.Model):
    fk_registro = models.ForeignKey(Fornitore, related_name='dettaglio_registro_attrezzatura_antincendio', on_delete=models.CASCADE)
    fk_attrezzatura = models.ForeignKey(AttrezzaturaAntincendio, related_name='dettaglio_registro_attrezzatura_antincendio', on_delete=models.CASCADE)
    manutenzione_effettuata = models.BooleanField(default=False)
    controllo_effettuato = models.BooleanField(default=False)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='dettaglio_registro_attrezzatura_antincendio', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dettaglio del registro per {self.fk_attrezzatura}"






from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField # Field from django countries app
from anagrafiche.models import Fornitore
from django.contrib.auth.models import User


class Ward(models.Model):
    
    description = models.CharField(max_length=50, null=False, blank=False, help_text="Nome reparto", db_column="descrizionereparto")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["description"]
        verbose_name_plural = "wards"
        db_table = "reparti"
    
    def __str__(self):
        return self.description
        

class Role(models.Model):
    
    description = models.CharField(max_length=50, null=False, blank=False, help_text="Nome mansione", db_column="descrizionemansione")
    fk_reparto = models.ForeignKey(Ward, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["description"]
        verbose_name_plural = "roles"
        db_table = "mansioni"
        
        
    def __str__(self):
        return self.description

class HumanResource(models.Model):
    GENDER_CHOICES = (
        ('M', 'Maschio'),
        ('F', 'Femmina'),
    )
    
    cognomedipendente = models.CharField(max_length=50, null=False, blank=False)
    nomedipendente = models.CharField(max_length=50, null=False, blank=False)
    country = CountryField(blank_label='(seleziona Paese)', null=True, blank=True)
    immagine = models.ImageField(upload_to='operator_pictures/', default= 'avatar.png',null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    dataassunzione = models.DateField(null=False, blank=False)
    datadimissioni = models.DateField(null=True, blank=True)
    fk_mansione = models.ForeignKey(Role, null=True, blank=True, on_delete=models.SET_NULL)
    fk_reparto = models.ForeignKey(Ward, null=True, blank=True, on_delete=models.SET_NULL)
    qualifica = models.CharField(max_length=50, null=True, blank=True)
    commenti = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.cognomedipendente + " " + self.nomedipendente

    def get_absolute_url(self):
        return reverse("human_resources:update-human-resource", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["-dataassunzione"]
        verbose_name_plural = "dipendenti"
        db_table = "dipendenti"


        
class AreaFormazione(models.Model):
    '''
    Questo modello racchiude le aree di formazione
    per esempio: Sicurezza, Qualità, Amministrazione
    '''
    descrizione = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, related_name='area_formazione', null=True, blank=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return self.descrizione


class CorsoFormazione(models.Model):
    descrizione = models.CharField(max_length=100)
    fk_areaformazione = models.ForeignKey(AreaFormazione, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='corso_formazione', null=True, blank=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return self.descrizione
    
class RegistroFormazione(models.Model):
    data_formazione = models.DateField(null=False, blank=False)
    fk_corso = models.ForeignKey(CorsoFormazione, on_delete=models.CASCADE)
    fk_fornitore = models.ForeignKey(Fornitore, null=True, blank=True, on_delete=models.SET_NULL)
    ore = models.IntegerField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='registro_formazione', null=True, blank=True, on_delete=models.SET_NULL)
    
    class Meta:
        ordering = ["-data_formazione"]



# funzione che crea la directory in base al corso    
def corso_directory_path(instance, filename):
    corso = instance.fk_registro_formazione.fk_corso
    return "{0}/{1}".format(corso, filename)



        
class DettaglioRegistroFormazione(models.Model):
    
    # presenza
    PRESENTE = 'presente'
    ASSENTE = 'assente'
    
    
    CHOICES_PRESENCE = (
        (PRESENTE, 'Presente'),
        (ASSENTE, 'Assente'),        
    )
    fk_registro_formazione = models.ForeignKey(RegistroFormazione, on_delete=models.CASCADE)
    fk_hr = models.ForeignKey(HumanResource, on_delete=models.CASCADE)
    note = models.TextField(null=True, blank=True)  
    certificato = models.FileField(upload_to=corso_directory_path)  
    presenza =  models.CharField(max_length=10, choices=CHOICES_PRESENCE)
    efficace = models.BooleanField(default=True)
    
        
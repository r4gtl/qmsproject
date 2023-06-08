from django.db import models
from django.urls import reverse
import datetime
from django_countries.fields import CountryField # Field from django countries app
from anagrafiche.models import Fornitore
from django.contrib.auth.models import User


class CentrodiLavoro(models.Model):
    '''
    In questa tabella si inseriscono i centri di lavoro.
    Da usare anche nella valutazione degli operatori.
    '''
    description = models.CharField(max_length=50, null=False, blank=False, help_text="Nome centro di lavoro", db_column="descrizionecentrodilavoro")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["description"]
        verbose_name_plural = "centridilavoro"
        db_table = "centrodilavoro"
    
    def __str__(self):
        return self.description


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
    data_nascita = models.DateField(null=True, blank=True)
    country = CountryField(blank_label='(seleziona Paese)', null=True, blank=True)
    immagine = models.ImageField(upload_to='operator_pictures', default= 'avatar.png',null=True, blank=True)        
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
    ore = models.IntegerField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)  
    certificato = models.FileField(upload_to=corso_directory_path)  
    presenza =  models.CharField(max_length=10, choices=CHOICES_PRESENCE)
    efficace = models.BooleanField(default=True)
    prossima_scadenza = models.DateField(null=True, blank=True)
    

class RegistroOreLavoro(models.Model):


    YEAR_CHOICES = [(y,y) for y in range(2000, datetime.date.today().year+1)]
    #MONTH_CHOICE = [(m,m) for m in range(1,13)]
    MONTH_CHOICE = (
        (1, 'Gennaio'),
        (2, 'Febbraio'),
        (3, 'Marzo'),
        (4, 'Aprile'),
        (5, 'Maggio'),
        (6, 'Giugno'),
        (7, 'Luglio'),
        (8, 'Agosto'),
        (9, 'Settembre'),
        (10, 'Ottobre'),
        (11, 'Novembre'),
        (12, 'Dicembre')
    )

    entry_year = models.IntegerField(choices=YEAR_CHOICES,
                 default=datetime.datetime.now().year,)
    entry_month = models.IntegerField(choices=MONTH_CHOICE,
                  default=datetime.datetime.now().month,)
    ore_lavorabili = models.IntegerField(null=True, blank=True)
    ore_lavorate = models.IntegerField(null=True, blank=True)
    straordinari = models.IntegerField(null=True, blank=True)
    ferie_permessi = models.IntegerField(null=True, blank=True)
    permessi_speciali = models.IntegerField(null=True, blank=True)
    maternità = models.IntegerField(null=True, blank=True)
    infortunio = models.IntegerField(null=True, blank=True)
    formazione = models.IntegerField(null=True, blank=True)
    formazione_neoassunti = models.IntegerField(null=True, blank=True)
    malattia = models.IntegerField(null=True, blank=True)
    n_infortuni = models.IntegerField(null=True, blank=True)
    n_infortuni_itinere = models.IntegerField(null=True, blank=True)
    n_malattie_professionali = models.IntegerField(null=True, blank=True)
    ore_malattie_professionali = models.IntegerField(null=True, blank=True)
    permessi_non_retribuiti = models.IntegerField(null=True, blank=True)
    assenze_ingiustificate = models.IntegerField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='registro_ore_lavorazione', null=True, blank=True, on_delete=models.SET_NULL)
    

    def entry_date(self):
        if self.entry_year and self.entry_month:
            return datetime.date(self.entry_year, self.entry_month, 1)
        elif self.entry_year:
            # return Jan 1st
            return datetime.date(self.entry_year, 1, 1)
        else:
            return None

    def month_verbose(self):
        return dict(RegistroOreLavoro.MONTH_CHOICE)[self.entry_month]
    
    class Meta:
        ordering = ["-entry_year", "-entry_month"]

class ValutazioneOperatore(models.Model):
    # Categoria
    NESSUNA = 'nessuna'
    MINIMO = 'minimo'
    MEDIO = 'medio'
    MIGLIORE = 'migliore'
    MASSIMO = 'massimo'
    
    CHOICES_CATEGORY = (
        (NESSUNA, 'Nessuna Valutazione'),
        (MINIMO, 'Minimo. L\'operatore richiede approfondita formazione.'),
        (MEDIO, 'Medio. L\'operatore è competente ma richiede affiancamento a persona di competenza superiore'),
        (MIGLIORE, 'Migliore. L\'operatore è sufficientemente competente.'),
        (MASSIMO, 'Massimo. L\'operatore può fornire formazione ad altri operatori.')
    )
    
    fk_hr = models.ForeignKey(HumanResource, on_delete=models.CASCADE)
    fk_centro_di_lavoro = models.ForeignKey(CentrodiLavoro, on_delete=models.CASCADE)      
    valutazione =  models.CharField(max_length=100, choices=CHOICES_CATEGORY)
    note = models.TextField(null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
import datetime
import os
import uuid
from dateutil.relativedelta import relativedelta

from anagrafiche.models import Fornitore
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum
from django.urls import reverse
from django_countries.fields import \
    CountryField  # Field from django countries app


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
        verbose_name_plural = "Centri di lavoro"
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
    
    # Contratto
    DETERMINATO = 'determinato'
    INDETERMINATO = 'indeterminato'
    
    
    CHOICES_CONTRATTO = (
        (DETERMINATO, 'Determinato'),
        (INDETERMINATO, 'Indeterminato'),        
    )
    
    # Orario
    PART_TIME = 'part_time'
    FULL_TIME = 'full_time'
    
    
    CHOICES_ORARIO = (
        (PART_TIME, 'Part-time'),
        (FULL_TIME, 'Full-time'),        
    )
    
    cognomedipendente = models.CharField(max_length=50, null=False, blank=False)
    nomedipendente = models.CharField(max_length=50, null=False, blank=False)
    data_nascita = models.DateField(null=True, blank=True)
    country = CountryField(blank_label='(seleziona Paese)', null=True, blank=True)
    immagine = models.ImageField(upload_to='operator_pictures', default= 'avatar.png',null=True, blank=True)        
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)    
    contratto = models.CharField(max_length=13, choices=CHOICES_CONTRATTO, null=True, blank=True)    
    orario = models.CharField(max_length=9, choices=CHOICES_ORARIO, null=True, blank=True)    
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

    def clean(self):
        """Validate that datadimissioni >= dataassunzione if both are set."""
        super().clean()
        if self.dataassunzione and self.datadimissioni:
            if self.datadimissioni < self.dataassunzione:
                raise ValidationError({
                    "datadimissioni": "La data di dimissioni non può essere precedente alla data di assunzione."
                })

    def get_absolute_url(self):
        return reverse("human_resources:update_human_resource", kwargs={"pk": self.pk})

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

    class Meta:
        ordering = ["descrizione"]
        verbose_name_plural = "Aree Formazione"        
    
    def __str__(self):
        return self.descrizione


class CorsoFormazione(models.Model):
    descrizione = models.CharField(max_length=100)
    fk_areaformazione = models.ForeignKey(AreaFormazione, on_delete=models.CASCADE)
    # Validità del corso in mesi (default 12). Usato per calcolare scadenza_calcolata.
    validita_mesi = models.PositiveIntegerField(
        default=12,
        help_text="Validità del corso in mesi (es. 12, 24, 36)"
    )
    created_by = models.ForeignKey(
        User,
        related_name='corso_formazione',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        ordering = ["descrizione"]
        verbose_name_plural = "Corsi Formazione"

    def __str__(self):
        return self.descrizione
    
    
class RegistroFormazione(models.Model):
    data_formazione = models.DateField(null=False, blank=False)
    fk_corso = models.ForeignKey(CorsoFormazione, on_delete=models.CASCADE)
    fk_fornitore = models.ForeignKey(Fornitore, null=True, blank=True, on_delete=models.SET_NULL)
    ore = models.DecimalField(max_digits=5, decimal_places=2, default=0, null=True, blank=True)    
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='registro_formazione', null=True, blank=True, on_delete=models.SET_NULL)
    
    class Meta:
        ordering = ["-data_formazione"]
        verbose_name_plural = "Registri Formazione"



# Funzione che crea la directory in base al corso
def corso_directory_path(instance, filename):
    """
    Upload certificati in cartella organizzata per corso.

    HARDENING:
    - os.path.basename: rimuove path traversal (../../../etc/passwd)
    - UUID: evita collisioni e caratteri problematici nel filename
    - Slug limitato a 30 char per evitare path troppo lunghi

    Path finale: certificati_formazione/corso_{id}_{slug}/{uuid}.{ext}
    """
    from django.utils.text import slugify

    # SICUREZZA: rimuovi qualsiasi path dal filename (previene path traversal)
    safe_filename = os.path.basename(filename)

    # Estrai e normalizza estensione
    _, ext = os.path.splitext(safe_filename)
    ext = ext.lower()

    # Genera nome univoco con UUID (evita collisioni e caratteri strani)
    new_filename = f"{uuid.uuid4().hex}{ext}"

    corso = instance.fk_registro_formazione.fk_corso
    # Slug limitato a 30 char per evitare path troppo lunghi
    corso_slug = slugify(corso.descrizione)[:30] if corso.descrizione else "corso"

    return f"certificati_formazione/corso_{corso.id}_{corso_slug}/{new_filename}"


class DettaglioRegistroFormazioneManager(models.Manager):
    """
    Manager custom per DettaglioRegistroFormazione.
    Fornisce query per ottenere il record corrente per coppia (hr, corso).
    """

    def get_current_per_hr_corso(self):
        """
        Ritorna il record corrente per ogni coppia (fk_hr, corso).

        Il "record corrente" è quello con scadenza_effettiva più lontana nel futuro.
        Se scadenza_override è valorizzata, usa quella; altrimenti scadenza_calcolata.

        Implementato con PostgreSQL DISTINCT ON per robustezza e performance.
        NOTA: DISTINCT ON è specifico PostgreSQL. Per altri DB usare subquery.
        """
        from django.db.models.functions import Coalesce

        # DISTINCT ON (PostgreSQL): seleziona il primo record per ogni gruppo
        # ordinato per scadenza_effettiva decrescente (più lontana nel futuro)
        return (
            self.get_queryset()
            .annotate(
                scadenza_effettiva_calc=Coalesce('scadenza_override', 'scadenza_calcolata')
            )
            .order_by(
                'fk_hr_id',
                'fk_registro_formazione__fk_corso_id',
                '-scadenza_effettiva_calc'
            )
            .distinct('fk_hr_id', 'fk_registro_formazione__fk_corso_id')
            .select_related(
                'fk_hr',
                'fk_registro_formazione',
                'fk_registro_formazione__fk_corso'
            )
        )


class DettaglioRegistroFormazione(models.Model):
    """
    Dettaglio partecipazione di un dipendente a un registro formazione.

    Gestione scadenze:
    - scadenza_calcolata: calcolata automaticamente da data_formazione + validita_mesi
    - scadenza_override: valore manuale che sovrascrive il calcolo automatico
    - scadenza_effettiva: property che ritorna override se presente, altrimenti calcolata

    DEPRECATO: prossima_scadenza - mantenuto per compatibilità, migrato in scadenza_override
    """

    PRESENTE = 'presente'
    ASSENTE = 'assente'

    CHOICES_PRESENCE = (
        (PRESENTE, 'Presente'),
        (ASSENTE, 'Assente'),
    )

    fk_registro_formazione = models.ForeignKey(
        RegistroFormazione,
        on_delete=models.CASCADE,
        related_name='dettagli'
    )
    fk_hr = models.ForeignKey(
        HumanResource,
        on_delete=models.CASCADE,
        related_name='dettagli_formazione'
    )
    ore = models.DecimalField(
        max_digits=5, decimal_places=2, default=0, null=True, blank=True
    )
    note = models.TextField(null=True, blank=True)
    certificato = models.FileField(
        upload_to=corso_directory_path, null=True, blank=True
    )
    presenza = models.CharField(max_length=10, choices=CHOICES_PRESENCE)
    efficace = models.BooleanField(default=True)

    # DEPRECATO: mantenuto per compatibilità DB, non usare in nuovo codice
    prossima_scadenza = models.DateField(null=True, blank=True)

    # Nuovi campi scadenza
    scadenza_calcolata = models.DateField(
        null=True,
        blank=True,
        help_text="Calcolata automaticamente: data_formazione + validita_mesi del corso"
    )
    scadenza_override = models.DateField(
        null=True,
        blank=True,
        help_text="Scadenza manuale che sovrascrive il calcolo automatico"
    )

    created_by = models.ForeignKey(
        User,
        related_name='dettaglio_registro_formazione',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    objects = DettaglioRegistroFormazioneManager()

    class Meta:
        ordering = ['-fk_registro_formazione__data_formazione']
        verbose_name_plural = "Dettagli Registro Formazione"
        indexes = [
            models.Index(
                fields=['fk_hr', 'fk_registro_formazione'],
                name='idx_dettaglio_hr_registro'
            ),
        ]

    def __str__(self):
        return f"{self.fk_hr} - {self.fk_registro_formazione.fk_corso}"

    @property
    def scadenza_effettiva(self):
        """
        Ritorna la scadenza effettiva: override se presente, altrimenti calcolata.
        """
        return self.scadenza_override or self.scadenza_calcolata

    def calcola_scadenza(self):
        """
        Calcola la scadenza basandosi su data_formazione + validita_mesi del corso.
        Ritorna la data calcolata (non salva).
        """
        if not self.fk_registro_formazione_id:
            return None

        registro = self.fk_registro_formazione
        if not registro.data_formazione or not registro.fk_corso:
            return None

        validita_mesi = registro.fk_corso.validita_mesi or 12
        return registro.data_formazione + relativedelta(months=validita_mesi)

    def save(self, *args, **kwargs):
        """Override save per calcolare automaticamente scadenza_calcolata."""
        # Calcola scadenza_calcolata se non già impostata o se i dati sono cambiati
        if self.fk_registro_formazione_id:
            self.scadenza_calcolata = self.calcola_scadenza()
        super().save(*args, **kwargs)
    

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
    
    
    @staticmethod
    def sum_field_per_year_last_triennium(field_name):
        # Calcola l'anno corrente
        current_year = datetime.date.today().year

        # Calcola l'anno di inizio dell'ultimo triennio
        last_triennium_start_year = current_year - 3

        # Filtra i record per l'ultimo triennio (escludendo l'anno in corso)
        records_last_triennium = RegistroOreLavoro.objects.filter(
            entry_year__gte=last_triennium_start_year,
            entry_year__lt=current_year
        )

        # Calcola la somma del campo specificato per ogni anno dell'ultimo triennio
        sum_per_year = {}
        for year in range(last_triennium_start_year, current_year):
            sum_per_year[year] = records_last_triennium.filter(
                entry_year=year
            ).aggregate(total_field=Sum(field_name))['total_field'] or 0

        return sum_per_year
    
    
    class Meta:
        ordering = ["-entry_year", "-entry_month"]
        verbose_name_plural = "Registri Ore Lavoro"

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
    fk_centro_di_lavoro = models.ForeignKey(CentrodiLavoro, on_delete=models.PROTECT)
    valutazione =  models.CharField(max_length=100, choices=CHOICES_CATEGORY)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='valutazione_operatore', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["fk_hr"]
        verbose_name_plural = "Valutazioni Operatori"
        constraints = [
            models.UniqueConstraint(
                fields=["fk_hr", "fk_centro_di_lavoro"],
                name="ux_valutazione_hr_centro"
            )
        ]


##############################################################################
# SAFETY
##############################################################################

class Safety_Role(models.Model):
    descrizione = models.CharField(max_length=100)    
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='safety_role', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["descrizione"]

    def __str__(self):
        return self.descrizione
    
class HR_Safety(models.Model):
    fk_hr = models.ForeignKey(HumanResource, related_name='hr_safety', on_delete=models.CASCADE)
    fk_safety_role = models.ForeignKey(Safety_Role, related_name='hr_safety', on_delete=models.CASCADE)
    data_inizio_incarico = models.DateField()
    data_fine_incarico = models.DateField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='hr_safety', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["fk_hr", "-data_inizio_incarico"]
        indexes = [
            models.Index(fields=["fk_hr", "fk_safety_role"], name="idx_hr_safety_lookup"),
        ]

    def __str__(self):
        return f"Operatore: {self.fk_hr} - Incarico: {self.fk_safety_role}"






    
    
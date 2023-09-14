from django.db import models
from datetime import date
from django.db.models import Max
from django.contrib.auth.models import User
from articoli.models import Articolo, Colore
from acquistopelli.models import TipoAnimale, TipoGrezzo
from chem_man.models import ProdottoChimico




####################################################
# RICETTE
####################################################

# Tabelle Generiche

class OperazioneRicette(models.Model):
    # Reparto riferimento
    BAGNATO = 'Bagnato'
    RIFINIZIONE = 'Rifinizione' 
    
    CHOICES_WARD = (
        (BAGNATO, 'Bagnato'),
        (RIFINIZIONE, 'Rifinizione')
    )
    descrizione = models.CharField(max_length=100)
    ward_ref = models.CharField(max_length=11, choices=CHOICES_WARD, null=False, blank=False)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='operazione_ricette', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

# Ricette bagnato    
class RicettaBagnato(models.Model):
    numero_ricetta = models.IntegerField(default=None)
    data_ricetta = models.DateField(default=date.today)
    fk_articolo = models.ForeignKey(Articolo, related_name='ricette_bagnato', on_delete=models.CASCADE)
    fk_tipoanimale = models.ForeignKey(TipoAnimale, null=True, blank=True, on_delete=models.SET_NULL, related_name='ricette_bagnato')
    fk_tipogrezzo = models.ForeignKey(TipoGrezzo, null=True, blank=True, on_delete=models.SET_NULL, related_name='ricette_bagnato')
    kg_ricetta = models.DecimalField(max_digits=4, decimal_places=0)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='ricette_bagnato', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if self.numero_ricetta is None:
            # Trova il valore massimo esistente in numero_ricetta
            max_numero_ricetta = RicettaBagnato.objects.aggregate(Max('numero_ricetta'))['numero_ricetta__max']
            
            if max_numero_ricetta is not None:
                self.numero_ricetta = max_numero_ricetta + 1
            else:
                # Se non ci sono ancora elementi, imposta il default a 1
                self.numero_ricetta = 1
        
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ["-data_ricetta"]
        
    def __str__(self):
        formatted_data_ricetta = self.data_ricetta.strftime('%d/%m/%Y')
        return f"Ricetta n.: {self.numero_ricetta} - Data Ricetta: {formatted_data_ricetta}"
        
class RevisioneRicettaBagnato(models.Model):
    fk_ricetta_bagnato = models.ForeignKey(RicettaBagnato, related_name='revisione_ricette_bagnato', on_delete=models.CASCADE)
    numero_revisione = models.IntegerField(default=None)
    data_revisione = models.DateField(default=date.today)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='revisione_ricette_bagnato', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-data_revisione"]
        
    def __str__(self):
        formatted_data_revisione = self.data_revisione.strftime('%d/%m/%Y')
        return f"Revisione n.: {self.numero_revisione} - Data Revisione: {formatted_data_revisione}"

    def save(self, *args, **kwargs):
        if self.numero_revisione is None:
            # Trova il valore massimo esistente in numero_revisione per la stessa fk_ricetta_bagnato
            max_numero_revisione = RevisioneRicettaBagnato.objects.filter(fk_ricetta_bagnato=self.fk_ricetta_bagnato).aggregate(Max('numero_revisione'))['numero_revisione__max']
            
            if max_numero_revisione is not None:
                self.numero_revisione = max_numero_revisione + 1
            else:
                # Se non ci sono ancora elementi per la stessa fk_ricetta_bagnato, imposta il default a 1
                self.numero_revisione = 1
        
        super().save(*args, **kwargs)

class DettaglioRevisioneRicettaBagnato(models.Model):
    # Questo modello serve per le righe effettive della ricetta
    fk_revisione = models.ForeignKey(RevisioneRicettaBagnato, related_name='dettaglio_revisione_ricette_bagnato', on_delete=models.CASCADE)
    numero_riga = models.IntegerField()
    
    def get_choices(self):
        return OperazioneRicette.objects.filter(ward_ref="Bagnato")
    
    fk_operazione_ricette = models.ForeignKey(OperazioneRicette, 
                                            related_name='dettaglio_revisione_ricette_bagnato', 
                                            on_delete=models.CASCADE,                                            
                                            limit_choices_to=get_choices,
                                            )
    
    temperatura = models.CharField(max_length=50)
    quantity = models.DecimalField(max_digits=8, decimal_places=2)
    fk_prodotto_chimico = models.ForeignKey(ProdottoChimico, related_name='dettaglio_revisione_ricette_bagnato', on_delete=models.CASCADE)
    tempo = models.CharField(max_length=50)
    procedura = models.CharField(max_length=100)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='dettaglio_revisione_ricette_bagnato', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # Controllo se il campo numero_riga è già stato assegnato, altrimenti lo calcolo
        if not self.numero_riga:
            # Trova il numero più alto in base alla fk_revisione
            max_numero_riga = DettaglioRevisioneRicettaBagnato.objects.filter(fk_revisione=self.fk_revisione).aggregate(models.Max('numero_riga'))['numero_riga__max']
            # Se non ci sono righe esistenti per questa revisione, inizia da 1, altrimenti incrementa di 1
            self.numero_riga = 1 if max_numero_riga is None else max_numero_riga + 1

        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ["numero_riga"]
        
    
    
        
class RicettaFondo(models.Model):
    numero_ricetta = models.IntegerField(default=None)
    data_ricetta = models.DateField(default=date.today)
    fk_colore = models.ForeignKey(Colore, related_name='ricette_fondo', on_delete=models.CASCADE)
    fk_ricetta_bagnato = models.ForeignKey(RicettaBagnato, related_name='ricette_fondo', on_delete=models.CASCADE)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='ricette_fondo', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    
        
    def save(self, *args, **kwargs):
        if self.numero_ricetta is None:
            # Trova il valore massimo esistente in numero_ricetta
            max_numero_ricetta = RicettaFondo.objects.aggregate(Max('numero_ricetta'))['numero_ricetta__max']
            
            if max_numero_ricetta is not None:
                self.numero_ricetta = max_numero_ricetta + 1
            else:
                # Se non ci sono ancora elementi, imposta il default a 1
                self.numero_ricetta = 1
        
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ["-data_ricetta"]
        
    def __str__(self):
        formatted_data_ricetta = self.data_ricetta.strftime('%d/%m/%Y')
        return f"Ricetta Fondo n.: {self.numero_ricetta} - Data Ricetta: {formatted_data_ricetta}"

class RevisioneRicettaFondo(models.Model):
    fk_ricetta_fondo = models.ForeignKey(RicettaFondo, related_name='revisione_ricette_fondo', on_delete=models.CASCADE)
    numero_revisione = models.IntegerField(default=None)
    data_revisione = models.DateField(default=date.today)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='revisione_ricette_fondo', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-data_revisione"]
        
    def __str__(self):
        formatted_data_revisione = self.data_revisione.strftime('%d/%m/%Y')
        return f"Revisione Fondo n.: {self.numero_revisione} - Data Revisione: {formatted_data_revisione}"

    def save(self, *args, **kwargs):
        if self.numero_revisione is None:
            # Trova il valore massimo esistente in numero_revisione per la stessa fk_ricetta_bagnato
            max_numero_revisione = RevisioneRicettaFondo.objects.filter(fk_ricetta_fondo=self.fk_ricetta_fondo).aggregate(Max('numero_revisione'))['numero_revisione__max']
            
            if max_numero_revisione is not None:
                self.numero_revisione = max_numero_revisione + 1
            else:
                # Se non ci sono ancora elementi per la stessa fk_ricetta_bagnato, imposta il default a 1
                self.numero_revisione = 1
        
        super().save(*args, **kwargs)
        
        
class DettaglioRevisioneRicettaFondo(models.Model):
    # Questo modello serve per le righe effettive della ricetta
    fk_revisione = models.ForeignKey(RevisioneRicettaFondo, related_name='dettaglio_revisione_ricette_fondo', on_delete=models.CASCADE)
    numero_riga = models.IntegerField()
    
    def get_choices(self):
        return OperazioneRicette.objects.filter(ward_ref="Bagnato")
    
    fk_operazione_ricette = models.ForeignKey(OperazioneRicette, 
                                            related_name='dettaglio_revisione_ricette_fondo', 
                                            on_delete=models.CASCADE,                                            
                                            limit_choices_to=get_choices,
                                            )
    quantity = models.DecimalField(max_digits=8, decimal_places=2)
    fk_prodotto_chimico = models.ForeignKey(ProdottoChimico, related_name='dettaglio_revisione_ricette_fondo', on_delete=models.CASCADE)
    temperatura = models.CharField(max_length=50)
    tempo = models.CharField(max_length=50)
    procedura = models.CharField(max_length=100)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='dettaglio_revisione_ricette_fondo', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # Controllo se il campo numero_riga è già stato assegnato, altrimenti lo calcolo
        if not self.numero_riga:
            # Trova il numero più alto in base alla fk_revisione
            max_numero_riga = DettaglioRevisioneRicettaFondo.objects.filter(fk_revisione=self.fk_revisione).aggregate(models.Max('numero_riga'))['numero_riga__max']
            # Se non ci sono righe esistenti per questa revisione, inizia da 1, altrimenti incrementa di 1
            self.numero_riga = 1 if max_numero_riga is None else max_numero_riga + 1

        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ["numero_riga"]
        
# Ricette Rifinizione    
class RicettaRifinizione(models.Model):
    pass
    


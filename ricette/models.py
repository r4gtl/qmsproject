import locale
from datetime import date
from decimal import Decimal

from acquistopelli.models import TipoAnimale, TipoGrezzo
from articoli.models import Articolo, Colore
from chem_man.models import PrezzoProdotto, ProdottoChimico
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Max, Q

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

    class Meta:
        ordering = ["descrizione"]

    def __str__(self):        
        return self.descrizione

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
# Faccio una prova per vedere di gestire numero ricetta e revisione in un'unico modello
class RicettaRifinizione(models.Model):
    numero_ricetta = models.IntegerField(blank=True, null=True)
    data_ricetta = models.DateField(default=date.today)
    numero_revisione = models.IntegerField(blank=True, null=True)
    data_revisione = models.DateField(default=date.today)
    fk_articolo = models.ForeignKey(Articolo, related_name='ricette_rifinizione', on_delete=models.CASCADE)    
    ricetta_per_pelli = models.DecimalField(max_digits=4, decimal_places=0)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='ricette_rifinizione', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def calcola_totale_prezzi(self):
        # Ottieni tutti i dettagli delle ricette associati a questa RicettaRifinizione
        dettagli_ricette = self.dettaglio_ricette_rifinizione.all()

        # Inizializza il totale a zero
        totale_prezzi = 0.0

        for dettaglio_ricetta in dettagli_ricette:
            recent_prezzi = PrezzoProdotto.objects.filter(
                fk_prodottochimico=dettaglio_ricetta.fk_prodotto_chimico
            ).order_by('-data_inserimento').values('prezzo')[:1]

            # Verifica se ci sono prezzi disponibili
            if recent_prezzi:
                # Converti il prezzo da Decimal a float
                prezzo_float = float(recent_prezzi[0]['prezzo'])

                # Converte quantity in float e moltiplica
                totale_prezzi += float(dettaglio_ricetta.quantity) * prezzo_float

        locale.setlocale(locale.LC_ALL, 'it_IT.UTF-8')  # Imposta la localizzazione italiana
        totale_prezzi = locale.currency(totale_prezzi, grouping=True, symbol=True)

        
        return totale_prezzi
    
    def calcola_solvente_totale(self):
        # Ottieni tutti i dettagli delle ricette associati a questa RicettaRifinizione
        dettagli_ricette = self.dettaglio_ricette_rifinizione.all()

        # Inizializza il totale del solvente a zero
        totale_solvente = 0.0

        for dettaglio_ricetta in dettagli_ricette:
            if dettaglio_ricetta.fk_prodotto_chimico and dettaglio_ricetta.fk_prodotto_chimico.solvente:
                # Calcola il solvente per il dettaglio della ricetta
                solvente_dettaglio = float(dettaglio_ricetta.quantity) * float((dettaglio_ricetta.fk_prodotto_chimico.solvente / 100))
                totale_solvente += solvente_dettaglio

        return totale_solvente
    
    def save(self, *args, **kwargs):
        # Se il numero ricetta è vuoto
        if self.numero_ricetta is None:
            max_numero_ricetta = RicettaRifinizione.objects.aggregate(Max('numero_ricetta'))['numero_ricetta__max']
            if self.pk:
                # Stai modificando una ricetta esistente
                previous_instance = RicettaRifinizione.objects.get(pk=self.pk)
                print("Previous instance: " + str(previous_instance))
                if self.fk_articolo != previous_instance.fk_articolo:
                    # L'articolo è stato cambiato, controlla se esiste già una ricetta per il nuovo articolo
                    #existing_ricetta = RicettaRifinizione.objects.filter(
                    #    fk_articolo=self.fk_articolo
                    #).exclude(pk=self.pk).order_by('-numero_revisione').first()

                    existing_ricetta = RicettaRifinizione.objects.filter(
                    fk_articolo=self.fk_articolo
                    ).order_by('-numero_revisione').first()
                    print("Articolo: " + str(self.fk_articolo))
                    print("Ricetta: " + str(existing_ricetta))

                    if existing_ricetta:
                        print("Modifica: la ricetta esiste. Existing ricetta numero ricetta: " + str(existing_ricetta.numero_ricetta) + "existing_ricetta.numero_revisione: " + str(existing_ricetta.numero_revisione))
                        # Esiste già una ricetta per il nuovo articolo, quindi usa il suo numero di ricetta
                        self.numero_ricetta = existing_ricetta.numero_ricetta                        
                        self.numero_revisione = existing_ricetta.numero_revisione + 1
                    else:
                        print("Modifica: la ricetta NON esiste. Existing ricetta numero ricetta: " + str(existing_ricetta.numero_ricetta) + "existing_ricetta.numero_revisione: " + str(existing_ricetta.numero_revisione))
                        # Non esiste ancora una ricetta per il nuovo articolo, quindi incrementa solo il numero_revisione
                        self.numero_ricetta = max_numero_ricetta + 1 if max_numero_ricetta else 1
                        self.numero_revisione = previous_instance.numero_revisione + 1
            else:
                # Stai creando una nuova ricetta

                # Stai creando una nuova ricetta
                existing_ricetta = RicettaRifinizione.objects.filter(
                    fk_articolo=self.fk_articolo
                ).order_by('-numero_revisione').first()
                print("Articolo: " + str(self.fk_articolo))
                print("Ricetta: " + str(existing_ricetta))
                #existing_ricetta = RicettaRifinizione.objects.order_by('-numero_revisione').first()

                if existing_ricetta:
                    print("Creazione: la ricetta esiste. Existing ricetta numero ricetta: " + str(existing_ricetta.numero_ricetta) + "existing_ricetta.numero_revisione: " + str(existing_ricetta.numero_revisione))
                    # Esiste già una ricetta, quindi usa il suo numero di ricetta e incrementa solo il numero_revisione
                    self.numero_ricetta = existing_ricetta.numero_ricetta
                    self.numero_revisione = existing_ricetta.numero_revisione + 1
                else:
                    # Non esiste ancora una ricetta, quindi inizia con il numero 1 per entrambi
                    self.numero_ricetta = max_numero_ricetta + 1 if max_numero_ricetta else 1
                    #self.numero_ricetta = 1
                    self.numero_revisione = 1
                    print("Creazione: la ricetta NON esiste. Existing ricetta numero ricetta: " + str(self.numero_ricetta) + "existing_ricetta.numero_revisione: " + str(self.numero_revisione))
        else:
            # Se il numero ricetta non è vuoto
            max_numero_ricetta = RicettaRifinizione.objects.aggregate(Max('numero_ricetta'))['numero_ricetta__max']
            if self.pk:
                # Stai modificando una ricetta esistente
                previous_instance = RicettaRifinizione.objects.get(pk=self.pk)
                print("Previous instance: " + str(previous_instance))
                if self.fk_articolo != previous_instance.fk_articolo:
                    existing_ricetta = RicettaRifinizione.objects.filter(
                    fk_articolo=self.fk_articolo
                    ).order_by('-numero_revisione').first()                    

                    if existing_ricetta:                        
                        # Esiste già una ricetta per il nuovo articolo, quindi usa il suo numero di ricetta
                        self.numero_ricetta = existing_ricetta.numero_ricetta                        
                        self.numero_revisione = existing_ricetta.numero_revisione + 1
                    else:
                        
                        # Non esiste ancora una ricetta per il nuovo articolo, quindi incrementa solo il numero_revisione
                        self.numero_ricetta = max_numero_ricetta + 1 if max_numero_ricetta else 1
                        self.numero_revisione = previous_instance.numero_revisione + 1
            else:
                # Stai creando una nuova ricetta
                existing_ricetta = RicettaRifinizione.objects.filter(
                    fk_articolo=self.fk_articolo
                ).order_by('-numero_revisione').first()               

                if existing_ricetta:                    
                    # Esiste già una ricetta, quindi usa il suo numero di ricetta e incrementa solo il numero_revisione
                    self.numero_ricetta = existing_ricetta.numero_ricetta
                    self.numero_revisione = existing_ricetta.numero_revisione + 1
                else:
                    # Non esiste ancora una ricetta, quindi inizia con il numero 1 per entrambi
                    self.numero_ricetta = max_numero_ricetta + 1 if max_numero_ricetta else 1                    
                    self.numero_revisione = 1
                    
        super().save(*args, **kwargs)


    
    class Meta:
        ordering = ["-data_ricetta"]
        
    def __str__(self):
        formatted_data_ricetta = self.data_ricetta.strftime('%d/%m/%Y')
        return f"Ricetta Rifinizione n.: {self.numero_ricetta} - Data Ricetta: {formatted_data_ricetta}"
    

class DettaglioRicettaRifinizione(models.Model):
    fk_ricetta_rifinizione = models.ForeignKey(RicettaRifinizione, related_name='dettaglio_ricette_rifinizione', on_delete=models.CASCADE)

    
    
    def get_choices_operations():
        #return OperazioneRicette.objects.filter(ward_ref="Rifinizione")
        return {'ward_ref': "Rifinizione"}
    
    fk_operazione_ricette = models.ForeignKey(OperazioneRicette, 
                                            related_name='dettaglio_ricette_rifinizione', 
                                            on_delete=models.CASCADE,                                            
                                            limit_choices_to=get_choices_operations,
                                            )
    numero_riga = models.IntegerField()
    quantity = models.DecimalField(max_digits=8, decimal_places=2)

    
    #def get_choices_chemical():
    #    return {'reparto': ProdottoChimico.RIFINIZIONE}  # Filtra i prodotti con reparto "Rifinizione"
    
    @staticmethod
    def get_choices_chemical():
        reparto_rifinizione = ProdottoChimico.objects.filter(reparto=ProdottoChimico.RIFINIZIONE)
        reparto_null = ProdottoChimico.objects.filter(Q(reparto__isnull=True) | Q(reparto=''))
        
        reparto_choices = list(reparto_rifinizione) + list(reparto_null)
    
        reparto_choices_dict = [{'id': choice.id, 'descrizione': choice.descrizione} for choice in reparto_choices]
        return Q(id__in=[choice['id'] for choice in reparto_choices_dict])


    fk_prodotto_chimico = models.ForeignKey(
        ProdottoChimico,
        related_name='dettaglio_ricette_rifinizione',
        on_delete=models.CASCADE,
        limit_choices_to=get_choices_chemical,
    )
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='dettaglio_ricette_rifinizione', null=True, blank=True, on_delete=models.SET_NULL)
    

    def calcola_totale(self):
        if self.fk_prodotto_chimico:
            # Ottieni l'ultimo prezzo dal modello ProdottoChimico
            ultimo_prezzo = self.fk_prodotto_chimico.ultimo_prezzo
            if ultimo_prezzo is not None:
                return self.quantity * ultimo_prezzo
        return 0  # Restituisci 0 se non c'è un prezzo disponibile o un prodotto chimico associato
    
    class Meta:
        ordering = ["numero_riga"]


    


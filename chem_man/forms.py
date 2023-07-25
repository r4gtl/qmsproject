from django import forms
from datetime import date
from django.db.models import Max
from django.contrib.admin.widgets import ForeignKeyRawIdWidget

from .models import (
                    ProdottoChimico, PrezzoProdotto, SchedaTecnica,
                    Sostanza, SostanzaSVHC, HazardStatement, PrecautionaryStatement,
                    SimboloGHS, SchedaSicurezza, SimboloGHS_SDS, PrecautionaryStatement_SDS, HazardStatement_SDS, Sostanza_SDS,
                    ImballaggioPC, OrdineProdottoChimico, DettaglioOrdineProdottoChimico,
                    AcquistoProdottoChimico, DettaglioAcquistoProdottoChimico
)
from anagrafiche.models import Fornitore


class ProdottoChimicoModelForm(forms.ModelForm):
    fk_fornitore = forms.ModelChoiceField(
        queryset=Fornitore.objects.filter(categoria=Fornitore.PRODOTTI_CHIMICI),
        label='Fornitore'
    )
    fk_imballaggio = forms.ModelChoiceField(
        queryset=ImballaggioPC.objects.all(),
        label='Imballaggio di default'
    )
    class Meta:
        model = ProdottoChimico
        fields= '__all__'
        widgets = {
            'descrizione': forms.TextInput(attrs={'placeholder': 'Inserisci il nome del prodotto chimico'}),
            'solvente': forms.NumberInput(attrs={'class': 'form-control text-end'}),
            
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),
            'created_by': forms.HiddenInput()
        }
        labels = {
            'descrizione': 'Nome Prodotto',
            'solvente': 'Percentuale Solvente',
            'reparto': 'Reparto',
            'flame_class': 'classe di Infiammabilità',
            'zdhc_level': 'ZDHC Level',
            'note': 'Note'

        }
        

class PrezzoProdottoModelForm(forms.ModelForm):
    
    
    class Meta:
        model = PrezzoProdotto
        fields= '__all__'
        widgets = {
            'data_inserimento': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),            
            'prezzo': forms.NumberInput(attrs={'class': 'form-control'}),            
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),
            'created_by': forms.HiddenInput(),
            'fk_prodottochimico': forms.HiddenInput()
        }
        labels = {
            'data_inserimento': 'Data Inserimento',
            'prezzo': 'Prezzo',            
            'note': 'Note'

        }
        

class SchedaTecnicaModelForm(forms.ModelForm):
    
    
    class Meta:
        model = SchedaTecnica
        fields= '__all__'
        widgets = {
            'data_inserimento': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),            
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),            
            'fk_prodottochimico': forms.HiddenInput()
        }
        labels = {
            'data_inserimento': 'Data Inserimento',
            'documento': 'Documento',
            'note': 'Note'

        }
        

class SostanzaModelForm(forms.ModelForm):
    
    
    class Meta:
        model = Sostanza
        fields= '__all__'
        widgets = {
            'descrizione': forms.TextInput(attrs={'placeholder': 'Inserisci il nome della sostanza'}),
            'num_cas': forms.TextInput(attrs={'placeholder': 'Inserisci il numero CAS'}),
            'num_ec': forms.TextInput(attrs={'placeholder': 'Inserisci il numero EC'}),
            'num_reach': forms.TextInput(attrs={'placeholder': 'Inserisci il numero ReaCh'}),
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),            
            'created_by': forms.HiddenInput()
        }
        labels = {
            'descrizione': 'Descrizione',
            'num_cas': 'Numero CAS',
            'num_ec': 'Numero EC',
            'num_reach': 'Numero ReaCh',            
            'note': 'Note'

        }
        

class SostanzaSVHCModelForm(forms.ModelForm):    
    
    class Meta:
        model = SostanzaSVHC
        fields= '__all__'
        widgets = {
            'descrizione': forms.TextInput(attrs={'placeholder': 'Inserisci il nome della sostanza'}),
            'data_inclusione': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),            
            'num_cas': forms.TextInput(attrs={'placeholder': 'Inserisci il numero CAS'}),
            'num_ec': forms.TextInput(attrs={'placeholder': 'Inserisci il numero EC'}),
            'num_reach': forms.TextInput(attrs={'placeholder': 'Inserisci il numero ReaCh'}),
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),            
            'created_by': forms.HiddenInput()
        }
        labels = {
            'descrizione': 'Descrizione',
            'data_inclusione': 'Data Inclusione',
            'num_cas': 'Numero CAS',
            'num_ec': 'Numero EC',
            'num_reach': 'Numero ReaCh',            
            'note': 'Note'

        }
        

class HazardStatementModelForm(forms.ModelForm):    
    
    class Meta:
        model = HazardStatement
        fields= '__all__'
        widgets = {
            'hazard_statement': forms.TextInput(attrs={'placeholder': 'Inserisci codice dell\'Indicazione di Pericolo '}),
            'descrizione': forms.TextInput(attrs={'placeholder': 'Inserisci la descrizione dell\'Indicazione di Pericolo'}),              
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),            
            'created_by': forms.HiddenInput()
        }
        labels = {
            'hazard_statement': 'Codice Indicazione di Pericolo',
            'descrizione': 'Descrizione',
            'hazard_category': 'Categoria di Pericolo',
            'is_dangerous': 'Segnalata nel DVR',           
            'note': 'Note'

        }
        

class PrecautionaryStatementModelForm(forms.ModelForm):    
    
    class Meta:
        model = PrecautionaryStatement
        fields= '__all__'
        widgets = {
            'codice': forms.TextInput(attrs={'placeholder': 'Inserisci codice del Consiglio Di Pridenza'}),
            'descrizione': forms.TextInput(attrs={'placeholder': 'Inserisci la descrizione del Consiglio di Prudenza'}),              
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),            
            'created_by': forms.HiddenInput()
        }
        labels = {
            'codice': 'Codice',
            'descrizione': 'Descrizione',            
            'is_dangerous': 'Segnalata nel DVR',           
            'note': 'Note'

        }

class SimboloGHSModelForm(forms.ModelForm):    
    
    class Meta:
        model = SimboloGHS
        fields= '__all__'
        widgets = {
            'codice': forms.TextInput(attrs={'placeholder': 'Inserisci codice del simbolo di pericolo'}),
            'descrizione': forms.Textarea(attrs={'placeholder': 'Inserisci descrizione', 'rows':'5'}),            
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),            
            'created_by': forms.HiddenInput()
        }
        labels = {
            'codice': 'Codice',
            'descrizione': 'Descrizione',   
            'symbol_image': 'Simbolo',
            
            'note': 'Note'

        }


class SchedaSicurezzaModelForm(forms.ModelForm):
    
    
    class Meta:
        model = SchedaSicurezza
        fields= '__all__'
        widgets = {
            'data_revisione': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),            
            
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),
            'created_by': forms.HiddenInput(),
            'fk_prodottochimico': forms.HiddenInput()
        }
        labels = {
            'data_revisione': 'Data Revisione',
            'documento': 'Documento',            
            'is_reach': 'Conforme Reach',
            'note': 'Note'

        }
        

class SimboloGHS_SDSModelForm(forms.ModelForm):    
    
    class Meta:
        model = SimboloGHS_SDS
        fields= '__all__'

      
        widgets = {
            
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),            
            'created_by': forms.HiddenInput(),
            'fk_sds': forms.HiddenInput(),
            'fk_simbolo_ghs': forms.Select()
        }
        labels = {
            'fk_simbolo_ghs': 'Simbolo GHS',      
            
            'note': 'Note'

        }


class PrecautionaryStatement_SDSModelForm(forms.ModelForm):    
    
    class Meta:
        model = PrecautionaryStatement_SDS
        fields= '__all__'

        fk_precautionary_statement = forms.ModelChoiceField(queryset=PrecautionaryStatement.objects.all())
        widgets = {
            
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),            
            'created_by': forms.HiddenInput(),
            'fk_sds': forms.HiddenInput()
        }
        labels = {
            'fk_precautionary_statement': 'Consiglio di Prudenza',      
            
            'note': 'Note'

        }

class HazardStatement_SDSModelForm(forms.ModelForm):    
    
    class Meta:
        model = HazardStatement_SDS
        fields= '__all__'

        fk_hazard_statement = forms.ModelChoiceField(queryset=HazardStatement.objects.all())
        widgets = {
            
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),            
            'created_by': forms.HiddenInput(),
            'fk_sds': forms.HiddenInput()
        }
        labels = {
            'fk_hazard_statement': 'Indicazione di Pericolo',      
            
            'note': 'Note'

        }


class Sostanza_SDSModelForm(forms.ModelForm):    
    
    class Meta:
        model = Sostanza_SDS
        fields= '__all__'
    
    

        
        widgets = {
            #'fk_sostanza': forms.ChoiceField(),
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),            
            'created_by': forms.HiddenInput(),
            'fk_sds': forms.HiddenInput()
        }
        labels = {
        #    'fk_sostanza': 'Sostanza',      
            
            'note': 'Note'

        }

    

     
class ImballaggioPCModelForm(forms.ModelForm):    
    
    class Meta:
        model = ImballaggioPC
        fields= '__all__'
        widgets = {
            'descrizione': forms.TextInput(attrs={'placeholder': 'Inserisci descrizione (Fusto da kg. 30, Cisterna...) '}),
            'peso_unitario': forms.NumberInput(attrs={'class': 'form-control text-end'}),            
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),            
            'created_by': forms.HiddenInput()
        }
        labels = {
            
            'descrizione': 'Descrizione',
            'peso_unitario': 'Peso Unitario',
            
            'note': 'Note'

        }
        

     
class OrdineProdottoChimicoModelForm(forms.ModelForm):    
    fk_fornitore = forms.ModelChoiceField(
        queryset=Fornitore.objects.filter(categoria=Fornitore.PRODOTTI_CHIMICI),
        label='Fornitore'
    )
    
    class Meta:
        model = OrdineProdottoChimico
        fields= '__all__'
        widgets = {
            #'numero_ordine': forms.NumberInput(attrs={'class': 'form-control'}),            
            'numero_ordine': forms.TextInput(attrs={'readonly': 'readonly', 'class':'text-end'}),
            'data_ordine': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control text-end', 'type': 'date'}),
            'data_consegna': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),
            'note_nc': forms.Textarea(attrs={'placeholder': 'Inserisci NC Riscontrate', 'rows':'3'}),            
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),            
            'created_by': forms.HiddenInput()
        }
        labels = {
            
            'numero_ordine': 'Numero Ordine',
            'data_ordine': 'Data Ordine',
            'data_consegna': 'Data Consegna',
            'is_conforme': 'Ordine conforme',
            'note_nc': 'NC Riscontrate',
            'note': 'Note'

        }

        
        

   
class DettaglioOrdineProdottoChimicoModelForm(forms.ModelForm):   

    fk_imballaggio = forms.ModelChoiceField(
        queryset=ImballaggioPC.objects.all(),
        label='Imballaggio',
        widget=forms.Select
    )

   
    class Meta:
        model = DettaglioOrdineProdottoChimico
        fields= '__all__'
        widgets = {
            
            'u_misura': forms.TextInput(),            
            'quantity': forms.NumberInput(attrs={'class': 'form-control text-end'}),            
            
            
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),            
            'created_by': forms.HiddenInput(),
            'fk_ordine': forms.HiddenInput()
        }
        labels = {
            
            'u_misura': 'Unità di Misura',
            'quantity': 'Quantità',
            'fk_prodotto_chimico': 'Prodotto Chimico',
            
            'note': 'Note'

        }
        # La prossima funzione serve per caricare il valore di imballaggio
        # quando creo una nuova istanza.
        # Attenzione: ChatGPT dice di caricare il form con
        # form = DettaglioOrdineProdottoChimicoModelForm(initial={'fk_prodotto_chimico': prodotto_chimico_instance})
        # quindi valutare nel caso di uso di CBV
        '''
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if not self.instance.pk:  # Controlla se è una nuova istanza
                fk_prodotto_chimico = self.initial.get('fk_prodotto_chimico')
                if fk_prodotto_chimico:
                    self.fields['fk_imballaggio'].initial = fk_prodotto_chimico.fk_imballaggio
        '''

  
class AcquistoProdottoChimicoModelForm(forms.ModelForm):    
    fk_fornitore = forms.ModelChoiceField(
        queryset=Fornitore.objects.filter(categoria=Fornitore.PRODOTTI_CHIMICI),
        label='Fornitore'
    )
    
    class Meta:
        model = AcquistoProdottoChimico
        fields= '__all__'
        widgets = {
            #'numero_ordine': forms.NumberInput(attrs={'class': 'form-control'}),            
            'numero_documento': forms.TextInput(attrs={'class':'text-end'}),
            'data_documento': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control text-end', 'type': 'date'}),
            
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),            
            'created_by': forms.HiddenInput()
        }
        labels = {
            
            'numero_documento': 'Numero Documento',
            'data_documento': 'Data Documento',
            
            'note': 'Note'

        }

        
        

   
class DettaglioAcquistoProdottoChimicoModelForm(forms.ModelForm):   

    

   
    class Meta:
        model = DettaglioAcquistoProdottoChimico
        fields= '__all__'
        widgets = {
            
            'u_misura': forms.TextInput(),            
            'quantity': forms.NumberInput(attrs={'class': 'form-control text-end'}),            
            
            
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),            
            'created_by': forms.HiddenInput(),
            'fk_acquisto': forms.HiddenInput()
        }
        labels = {
            
            'u_misura': 'Unità di Misura',
            'quantity': 'Quantità',
            'fk_prodotto_chimico': 'Prodotto Chimico',
            
            'note': 'Note'

        }
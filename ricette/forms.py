from datetime import date

from articoli.models import Articolo
from django import forms
from django.db.models import Max

from .models import *


class OperazioneRicetteModelForm(forms.ModelForm):
    
    
    class Meta:
        model = OperazioneRicette
        fields= '__all__'
        
        widgets = {
            'descrizione': forms.TextInput(attrs={'placeholder': 'Inserisci descrizione operazione'}),
            'ward_ref': forms.Select(),
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),
            'created_by': forms.HiddenInput(),
        }
        labels = {
            'descrizione': 'Descrizione',
            'ward_ref': 'Reparto',
            'note': 'Note'

        }


class RicettaRifinizioneModelForm(forms.ModelForm):
    
    
    class Meta:
        model = RicettaRifinizione
        fields= '__all__'
        fk_articolo = forms.ModelChoiceField(
            queryset=Articolo.objects.all(),            
            widget=forms.Select
            )
        
        
        widgets = {
            'numero_ricetta': forms.NumberInput(attrs={'class': 'form-control text-end', 'readonly': 'True'}),
            'data_ricetta': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control text-end', 'type': 'date'}),            
            'numero_revisione': forms.NumberInput(attrs={'class': 'form-control text-end', 'readonly': 'True'}),
            'data_revisione': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control text-end', 'type': 'date'}),            
            'ricetta_per_pelli': forms.NumberInput(attrs={'class': 'form-control text-end'}),
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),
            'created_by': forms.HiddenInput(),
        }
        labels = {
            'fk_articolo': 'Articolo',
            'numero_ricetta': 'Numero Ricetta',
            'data_ricetta': 'Data Ricetta',
            'numero_revisione': 'Numero Revisione',
            'data_revisione': 'Data Revisione',
            'ricetta_per_pelli': 'Ricetta per n. pelli',
            'note': 'Note'

        }

class DettaglioRicettaRifinizioneModelForm(forms.ModelForm):    
    
    class Meta:
        model = DettaglioRicettaRifinizione
        fields= '__all__'
        
        widgets = {
            'numero_riga': forms.NumberInput(attrs={'class': 'form-control text-end', 'readonly': 'True'}),
            'fk_operazione_ricette': forms.Select(),
            'fk_prodotto_chimico': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control text-end'}),            
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),
            'created_by': forms.HiddenInput(),
            'fk_ricetta_rifinizione': forms.HiddenInput()
        }
        labels = {
            'numero_riga': 'Ordinale',
            'fk_operazione_ricette': 'Operazione',
            'fk_prodotto_chimico': 'Prodotto Chimico',
            'quantity': 'Quantità',
            'note': 'Note'

        }


from django import forms
from datetime import date
from django.db.models import Max


from .models import *
from articoli.models import Articolo




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
            label='Articolo',
            widget=forms.Select
            )
        
        widgets = {
            'numero_ricetta': forms.NumberInput(attrs={'class': 'form-control text-end'}),
            'data_ricetta': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),            
            'numero_revisione': forms.NumberInput(attrs={'class': 'form-control text-end'}),
            'data_revisione': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),            
            'ricetta_per_pelli': forms.NumberInput(attrs={'class': 'form-control text-end'}),
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),
            'created_by': forms.HiddenInput(),
        }
        labels = {
            'numero_ricetta': 'Numero Ricetta',
            'data_ricetta': 'Data Ricetta',
            'numero_revisione': 'Numero Revisione',
            'data_revisione': 'Data Revisione',
            'ricetta_per_pelli': 'Ricetta per n. pelli',
            'note': 'Note'

        }
        
        
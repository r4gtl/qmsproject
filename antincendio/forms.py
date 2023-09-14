from django import forms
from datetime import date
from django.db.models import Max


from .models import *


class EstintoreModelForm(forms.ModelForm):
    
    
    class Meta:
        model = Estintore
        fields= '__all__'
        widgets = {
            'tipo_estinguente': forms.TextInput(attrs={'placeholder': 'Inserisci il tipo estinguente (polvere, idrico, ...)'}),
            'classe': forms.TextInput(attrs={'placeholder': 'Inserisci la classe (113B, 34A233BC, ...)'}),
            'peso': forms.TextInput(attrs={'placeholder': 'Inserisci il peso'}),
            'matricola': forms.TextInput(attrs={'placeholder': 'Inserisci il numero di matricola'}),
            'anno': forms.TextInput(attrs={'placeholder': 'Inserisci l\'anno di fabbricazione'}),
            'ubicazione': forms.TextInput(attrs={'placeholder': 'Inserisci la posizione o il reparto'}),
            'data_dismissione': forms.TextInput(attrs={'placeholder': 'Inserisci eventuale data di dismissione'}),
            'numero_posizione': forms.TextInput(attrs={'placeholder': 'Inserisci il numero assegnato'}),
            'scadenza_revisione': forms.TextInput(attrs={'placeholder': 'Inserisci/modifica la scadenza di revisione'}),
            'scadenza_collaudo': forms.TextInput(attrs={'placeholder': 'Inserisci/modifica la scadenza di collaudo'}),
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),            
            'created_by': forms.HiddenInput()
        }
        labels = {
            'tipo_estinguente': 'Tipo estinguente',
            'classe': 'Classe',
            'peso': 'Peso',
            'matricola': 'Matricola',            
            'anno': 'Anno di fabbricazione',            
            'ubicazione': 'Ubicazione',            
            'data_dismissione': 'Data Dismissione',            
            'numero_posizione': 'Numero/Posizione',            
            'scadenza_revisione': 'Scadenza Revisione',            
            'scadenza_collaudo': 'Scadenza Collaudo',            
            'note': 'Note'

        }
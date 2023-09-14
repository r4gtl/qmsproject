from django import forms
from datetime import date
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
        
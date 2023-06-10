from django import forms

from .models import (Articolo, 
                    Colore,
                )


class ArticoloModelForm(forms.ModelForm):
    class Meta:
        model = Articolo
        fields = '__all__'
        widgets = {
            'descrizione': forms.TextInput(attrs={'placeholder': 'Inserisci Nome Articolo'}),            
            'created_by': forms.HiddenInput(),
            'created_at': forms.HiddenInput()
        }
        labels = {
            'descrizione': 'Articolo',
            
        }
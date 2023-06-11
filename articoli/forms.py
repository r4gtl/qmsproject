from django import forms

from .models import (Articolo, 
                    Colore, FaseLavoro
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
        
class ColoreModelForm(forms.ModelForm):
    class Meta:
        model = Colore
        fields = '__all__'
        widgets = {
            'descrizione': forms.TextInput(attrs={'placeholder': 'Inserisci Nome colore'}),            
            'created_by': forms.HiddenInput(),
            'created_at': forms.HiddenInput()
        }
        labels = {
            'descrizione': 'Colore',
            
        }
        
class FaseLavoroModelForm(forms.ModelForm):
    class Meta:
        model = FaseLavoro
        fields = '__all__'
        widgets = {
            'descrizione': forms.TextInput(attrs={'placeholder': 'Inserisci Nome Fase'}),            
            'created_by': forms.HiddenInput(),
            'created_at': forms.HiddenInput()
        }
        labels = {
            'descrizione': 'Fase di Lavoro',
            
        }
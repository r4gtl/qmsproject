from django import forms

from .models import (Articolo, 
                    Colore, FaseLavoro, ElencoTest
                )
from acquistopelli.models import TipoAnimale, TipoGrezzo


class ArticoloModelForm(forms.ModelForm):
    class Meta:
        model = Articolo
        fields = '__all__'
        fk_tipoanimale = forms.ModelChoiceField(queryset=TipoAnimale.objects.all())
        fk_tipogrezzo = forms.ModelChoiceField(queryset=TipoGrezzo.objects.all())
        widgets = {
            'descrizione': forms.TextInput(attrs={'placeholder': 'Inserisci Nome Articolo'}),            
            'created_by': forms.HiddenInput(),
            'created_at': forms.HiddenInput()
        }
        labels = {
            'descrizione': 'Articolo',
            'fk_tipoanimale': 'Tipo Animale',
            'fk_tipogrezzo': 'Tipo Grezzo'
            
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

class ElencoTestModelForm(forms.ModelForm):
    class Meta:
        model = ElencoTest
        fields = '__all__'
        widgets = {
            'descrizione': forms.TextInput(attrs={'placeholder': 'Inserisci Nome Test'}),   
            'norma_riferimento': forms.TextInput(attrs={'placeholder': 'Inserisci norma di riferimento'}),
            'created_by': forms.HiddenInput(),
            'created_at': forms.HiddenInput()
        }
        labels = {
            'descrizione': 'Test',
            'norma_riferimento': 'Norma di Riferimento',
            
        }
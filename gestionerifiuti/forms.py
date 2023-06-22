from django import forms

from .models import (MovimentoRifiuti, 
                    CodiceCER,
                    CodiceSmaltRec
                )


class MovimentoRifiutiModelForm(forms.ModelForm):

    fk_codicecer = forms.ModelChoiceField(queryset=CodiceCER.objects.all(), label='Codice Cer')
    fk_smaltrec = forms.ModelChoiceField(queryset=CodiceSmaltRec.objects.all(), label='Codice Smalt/Rec')

    class Meta:
        model = MovimentoRifiuti
        fields = '__all__'
        widgets = {
            'data_movimento': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'style': 'text-align: right;'}),            
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),
            'created_by': forms.HiddenInput(),
            'created_at': forms.HiddenInput()
        }
        labels = {
            'data_movimento': 'Data Movimento',
            'fk_codicecer': 'Codice Cer',
            'car_scar': 'Carico/Scarico',
            'quantity': 'Quantità',
            'fk_smaltrec': 'Codice Smalt/Rec',
            'note': 'Annotazioni'

            
        }
        

class CodiceCERModelForm(forms.ModelForm):

    

    class Meta:
        model = CodiceCER
        fields = '__all__'
        widgets = {
            'codice': forms.TextInput(attrs={'class': 'form-control'}),
            'descrizione': forms.TextInput(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),
            'created_by': forms.HiddenInput(),
            'created_at': forms.HiddenInput()
        }
        labels = {
            'codice': 'Codice Cer',
            'descrizione': 'Descrizione',            
            'note': 'Annotazioni'

            
        }
        

class CodiceSmaltRecModelForm(forms.ModelForm):

    

    class Meta:
        model = CodiceSmaltRec
        fields = '__all__'
        widgets = {
            'codice': forms.TextInput(attrs={'class': 'form-control'}),
            'descrizione': forms.TextInput(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),
            'created_by': forms.HiddenInput(),
            'created_at': forms.HiddenInput()
        }
        labels = {
            'codice': 'Codice Cer',
            'descrizione': 'Descrizione',   
            'smalt_rec': 'Smaltimento/Recupero',
            'note': 'Annotazioni'

            
        }
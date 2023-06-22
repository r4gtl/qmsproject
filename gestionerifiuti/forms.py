from django import forms

from .models import (MovimentoRifiuti, 
                    CodiceCER,
                    CodiceSmaltRec
                )


class MovimentoRifiutiModelForm(forms.ModelForm):

    fk_codicecer = forms.ModelChoiceField(queryset=CodiceCER.objects.all())
    fk_smaltrec = forms.ModelChoiceField(queryset=CodiceSmaltRec.objects.all())

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
from django import forms
from .models import (MonitoraggioAcqua, MonitoraggioGas, MonitoraggioEnergiaElettrica,
                     DatoProduzione
                     )


class MonitoraggioAcquaModelForm(forms.ModelForm):
    class Meta:
        model = MonitoraggioAcqua
        fields = '__all__'

        widget = {
            'data_lettura': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),
            'mc_in': forms.NumberInput(attrs={'class': 'form-control'}),
            'mc_out': forms.NumberInput(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),
            'created_by': forms.HiddenInput()
        }
        labels = {
            'data_lettura': 'Data Lettura',
            'mc_in': 'Mc in ingresso',
            'mc_out': 'Mc in uscita',
            'note': 'Annotazioni'
        }

class MonitoraggioGasModelForm(forms.ModelForm):
    class Meta:
        model = MonitoraggioGas
        fields = '__all__'

        widget = {
            'data_lettura': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),
            'mc_in': forms.NumberInput(attrs={'class': 'form-control'}),            
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),
            'created_by': forms.HiddenInput()
        }
        labels = {
            'data_lettura': 'Data Lettura',
            'mc_in': 'Mc in ingresso',            
            'note': 'Annotazioni'
        }

class MonitoraggioEnergiaElettricaModelForm(forms.ModelForm):
    class Meta:
        model = MonitoraggioEnergiaElettrica
        fields = '__all__'

        widget = {
            'data_lettura': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),
            'kwh_in': forms.NumberInput(attrs={'class': 'form-control'}),            
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),
            'created_by': forms.HiddenInput()
        }
        labels = {
            'data_lettura': 'Data Lettura',
            'kwh_in': 'Kwh in ingresso',            
            'note': 'Annotazioni'
        }

class DatoProduzioneModelForm(forms.ModelForm):
    class Meta:
        model = DatoProduzione
        fields = '__all__'

        widget = {
            'data_inserimento': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),
            'industries_served': forms.ChoiceField(),
            'n_pelli': forms.NumberInput(attrs={'class': 'form-control'}),
            'mq': forms.NumberInput(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),
            'created_by': forms.HiddenInput()
        }
        labels = {
            'data_inserimento': 'Data inserimento',
            'industries_served': 'Destinazione d\'Uso',
            'mc_in': 'Mc in ingresso',
            'mc_out': 'Mc in uscita',
            'note': 'Annotazioni'
        }
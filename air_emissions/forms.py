from django import forms
from .models import *



class FormPuntoEmissione(forms.ModelForm):
    class Meta:
        model = PuntoEmissione
        exclude=()
        #fields='__all__'
        camino_numero = forms.CharField(max_length=50)
        origine = forms.CharField(max_length=50)
        quota = forms.CharField(max_length=50)
        portata = forms.CharField(max_length=50)
        parametri = forms.CharField(max_length=50)
        limite_conc = forms.CharField(max_length=50)
        limite_flusso = forms.CharField(max_length=50)
        tipo_abbattimento = forms.CharField(max_length=50)
        tipo_abbattimento = forms.CharField(max_length=50)
        autorizzazione = forms.CharField(max_length=50)
        widgets = {
                'created_at': forms.HiddenInput(),
                'created_by': forms.HiddenInput()
                }
        labels = {
            'camino_numero': 'Camino Numero',
            'origine': 'Origine',
            'quota': 'Quota (m)',
            'portata': 'portata (Nm3/h)',
            'parametri': 'Parametri',
            'limite_conc': 'Limite Concentrazione (mg/Nm3)',
            'limite_flusso': 'Limite Flusso (g/h)',
            'tipo_abbattimento': 'Tipo di Abbattimento',
            'soggetto_controllo': 'Soggetto a controllo',
            'autorizzazione': 'Autorizzazione',
            'is_disabled': 'Non Attivo',
            'note': 'Note',
            
            
        }
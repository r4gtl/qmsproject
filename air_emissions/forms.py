from django import forms
from .models import *



class PuntoEmissioneModelForm(forms.ModelForm):
    class Meta:
        model = PuntoEmissione
        exclude=()
        #fields='__all__'
        
        widgets = {
                'camino_numero': forms.TextInput(attrs={'placeholder': 'Inserisci il nome del punto di emissione'}),
                'origine': forms.TextInput(attrs={'placeholder': 'Inserisci l\'origine del punto di emissione'}),
                'quota': forms.TextInput(attrs={'placeholder': 'Inserisci la quota del punto di emissione'}),
                'portata': forms.NumberInput(attrs={'class': 'form-control'}),
                'parametri': forms.TextInput(attrs={'placeholder': 'Inserisci il parametro del punto di emissione'}),
                'limite_conc': forms.NumberInput(attrs={'class': 'form-control'}),
                'limite_flusso': forms.NumberInput(attrs={'class': 'form-control'}),       
                'tipo_abbattimento': forms.TextInput(attrs={'placeholder': 'Inserisci il tipo di abbattimento del punto di emissione'}),
                'autorizzazione': forms.TextInput(attrs={'placeholder': 'Inserisci l\'autorizzazione di riferimento del punto di emissione'}),
                'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),
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




class RegistroControlloAnaliticoModelForm(forms.ModelForm):
    class Meta:
        model = RegistroControlloAnalitico
        exclude=()
        fields='__all__'
        
        widgets = {
                'fk_punto_emissione': forms.HiddenInput(),
                'data_prelievo': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),
                'prossima_scadenza': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),                
                'portata_risc': forms.NumberInput(attrs={'class': 'form-control', 'style': 'text-align: right;'}),
                'conc_risc': forms.NumberInput(attrs={'class': 'form-control', 'style': 'text-align: right;'}),
                'flusso_risc': forms.NumberInput(attrs={'class': 'form-control', 'style': 'text-align: right;'}),
                'certificato_numero': forms.TextInput(attrs={'placeholder': 'Inserisci il tipo di abbattimento del punto di emissione'}),                
                'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),
                'created_at': forms.HiddenInput(),
                'created_by': forms.HiddenInput()
                }
        labels = {
            'data_prelievo': 'Data Prelievo',
            'prossima_scadenza': 'Prossima Scadenza',
            'portata_risc': 'Portata Riscontrata (Nm3/h)',
            'conc_risc': 'Concentrazione riscontrata (mg/Nm3)',
            'flusso_risc': 'Flusso di massa riscontrato (g/h)',
            'certificato_numero': 'Numero certificato',
            'certificato': 'Link al certificato',
            'note': 'Note',
            
            
        }
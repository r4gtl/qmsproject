from django import forms
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField
from .models import (Attrezzatura, ManutenzioneStraordinaria, Taratura,
                    ManutenzioneOrdinaria,
                    )
from human_resources.models import Ward

from anagrafiche.models import Fornitore

class AttrezzaturaModelForm(forms.ModelForm):
    class Meta:
        model = Attrezzatura
        fields = '__all__'
        fk_ward = forms.ModelChoiceField(queryset=Ward.objects.all())
        widgets = {
            
            'codice_attrezzatura': forms.TextInput(attrs={'placeholder': 'Inserisci codice attrezzatura'}),
            'descrizione': forms.TextInput(attrs={'placeholder': 'Inserisci descrizione'}),
            'modello': forms.TextInput(attrs={'placeholder': 'Inserisci modello'}),
            'serie_matricola': forms.TextInput(attrs={'placeholder': 'Inserisci serie/matricola'}),
            'is_dismesso': forms.CheckboxInput(),
            'data_dismissione': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),
            'is_taratura': forms.CheckboxInput(),
            'periodo_taratura': forms.TextInput(attrs={'placeholder': 'Inserisci periodo taratura'}),            
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows': 3}),
            

            'created_by': forms.HiddenInput(),
            'created_at': forms.HiddenInput()
        }
        labels = {
            
            'codice_attrezzatura': 'Codice Attrezzatura',
            'descrizione': 'Descrizione',
            'modello': 'Modello',
            'serie_matricola': 'N. serie/N. Matricola',
            'fk_ward': 'Reparto',
            'is_dismesso': 'Dismesso',
            'data_dismissione': 'Data Dismissione',
            'is_taratura': 'Soggetto a taratura',
            'periodo_taratura': 'Periodi di taratura',
            'note': 'Annotazioni'
        }
        
class ManutenzioneStraordinariaModelForm(forms.ModelForm):
    fk_fornitore = forms.ModelChoiceField(queryset=Fornitore.objects.all(), label='Fornitore')
    

    class Meta:
        model = ManutenzioneStraordinaria
        fields = '__all__'
        
        widgets = {
            'data_manutenzione': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),
            'descrizione': forms.TextInput(attrs={'placeholder': 'Inserisci descrizione'}),            
            'fk_fornitore': forms.Select(attrs={'style': 'background-color: #F5F8EC'}),
            'ft_prot': forms.TextInput(attrs={'placeholder': 'Inserisci codice attrezzatura'}),
            'importo': forms.NumberInput(attrs={'class': 'form-control', 'style': 'text-align: right;'}), 
            'ore_fermo': forms.NumberInput(attrs={'class': 'form-control', 'style': 'text-align: right;'}), 
            'data_fattura': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),            
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),
            'fk_attrezzatura': forms.HiddenInput(),
            'created_by': forms.HiddenInput(),
            'created_at': forms.HiddenInput()
        }

        labels = {
            
            'data_manutenzione': 'Data Manutenzione',
            'descrizione': 'Descrizione',
            'importo': 'Importo',
            'ore_fermo': 'Ore Fermo',
            'fk_fornitore': 'Fornitore',
            'ft_prot': 'Fattura Protocollo',
            'data_fattura': 'Data Fattura',
            'note': 'Annotazioni'
        }
        
class TaraturaModelForm(forms.ModelForm):
    class Meta:
        model = Taratura
        fields = '__all__'
        fk_fornitore = forms.ModelChoiceField(queryset=Fornitore.objects.all(), label='Fornitore')
        widgets = {
            'data_taratura': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),
            'fk_fornitore': forms.Select(attrs={'style':'background_color:#F5F8EC'}),            
            #'documento': forms.FileField(),
            'is_conforme': forms.CheckboxInput(),
            'prossima_scadenza': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),
            'fk_attrezzatura': forms.HiddenInput(),
            'created_by': forms.HiddenInput(),
            'created_at': forms.HiddenInput()
        }
        labels = {
            
            'data_taratura': 'Data Taratura',
            'fk_fornitore': 'Fornitore',
            'documento': 'Documento',
            'is_conforme': 'Conforme',
            'prossima_scadenza': 'Prossima Scadenza',
            'note': 'Annotazioni'
        }
        
class ManutenzioneOrdinariaModelForm(forms.ModelForm):
    class Meta:
        model = ManutenzioneOrdinaria
        fields = '__all__'
        fk_fornitore = forms.ModelChoiceField(queryset=Fornitore.objects.all(),  label='Fornitore')
        widgets = {
            'data_manutenzione': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),
            'descrizione': forms.TextInput(attrs={'placeholder': 'Inserisci descrizione'}),
            'fk_fornitore': forms.Select(attrs={'style':'background_color:#F5F8EC'}),                        
            'is_eseguita': forms.CheckboxInput(),
            'prossima_scadenza': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),
            'fk_attrezzatura': forms.HiddenInput(),
            'created_by': forms.HiddenInput(),
            'created_at': forms.HiddenInput()
        }
        labels = {
            
            'data_manutenzione': 'Data Manutenzione',
            #'fk_fornitore': 'Fornitore',
            'descrizione': 'Descrizione',
            'is_eseguita': 'Eseguita',
            'prossima_scadenza': 'Prossima Scadenza',
            'note': 'Annotazioni'
        }
        
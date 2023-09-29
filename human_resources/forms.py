from cProfile import label
from django import forms
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField



from .models import *
from anagrafiche.models import Fornitore


class HumanResourceModelForm(forms.ModelForm):
    class Meta:
        model = HumanResource
        fields = '__all__'
        exclude = ['created_at', 'updated_at']
        country = CountryField().formfield()
        
        widgets = {            
            'cognomedipendente': forms.TextInput(attrs={'class': 'form-control'}),
            'nomedipendente': forms.TextInput(attrs={'class': 'form-control'}),
            'country': CountrySelectWidget(),
            'data_nascita': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),            
            #'immagine': forms.ImageField(),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'contratto': forms.Select(attrs={'class': 'form-control'}),
            'orario': forms.Select(attrs={'class': 'form-control'}),
            'dataassunzione': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),
            'datadimissioni': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),
            'fk_mansione': forms.Select(attrs={'class': 'form-control'}),
            'fk_reparto': forms.Select(attrs={'class': 'form-control'}),
            'qualifica': forms.TextInput(attrs={'class': 'form-control'}),
            'commenti': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),
            
        }
        
        labels = {
            'cognomedipendente': 'Cognome',
            'nomedipendente': 'Nome',
            'country': 'Nazionalità',
            'data_nascita': 'Data di Nascita',
            'immagine': 'Foto',
            'gender': 'Genere',
            'dataassunzione': 'Data Assunzione',
            'datadimissioni': 'Data Dimissioni',
            'fk_mansione': 'Mansione',
            'fk_reparto': 'Reparto',
            'qualifica': 'Qualifica',
            'commenti': 'Commenti',

        }

class CentrodiLavoroModelForm(forms.ModelForm):
    class Meta:
        model = CentrodiLavoro
        fields = '__all__'
        labels = {
            'description': 'Descrizione',    
        }

class WardModelForm(forms.ModelForm):
    class Meta:
        model = Ward
        fields = '__all__'
        labels = {
            'description': 'Descrizione',    
        }


class RoleModelForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = '__all__'
        labels = {
            'description': 'Descrizione',    
        }



class Safety_RoleModelForm(forms.ModelForm):
    class Meta:
        model = Safety_Role
        fields= '__all__'
        widgets = {
            'descrizione': forms.TextInput(attrs={'placeholder': 'Inserisci il nome dell\'incarico sicurezza'}), 
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),
            'created_by': forms.HiddenInput(),
        }
        labels = {
            'descrizione': 'Descrizione',                       
            'note': 'Note'

        }



'''SEZIONE FORMAZIONE'''        
# Area formazione
class AreaFormazioneModelForm(forms.ModelForm):
    class Meta:
        model = AreaFormazione
        fields = '__all__'
        widgets = {
            'descrizione': forms.TextInput(attrs={'placeholder': 'Inserisci Area Formazione'}),            
            'created_by': forms.HiddenInput()
        }
        
        
# Corso Formazione        
class CorsoFormazioneModelForm(forms.ModelForm):
    class Meta:
        model = CorsoFormazione
        fields = '__all__'
        fk_areaformazione = forms.ModelChoiceField(queryset=AreaFormazione.objects.all())
        widgets = {
            'descrizione': forms.TextInput(attrs={'placeholder': 'Inserisci Corso Formazione'}),
            'fk_areaformazione': forms.Select(attrs={'style':'background_color:#F5F8EC'}),
            'created_by': forms.HiddenInput()
        }
        labels = {
            'descrizione': 'Corso di Formazione',
            'fk_areaformazione': 'Area Formazione',
            

        }

# Registro Formazione
class RegistroFormazioneModelForm(forms.ModelForm):
    class Meta:
        model = RegistroFormazione
        fields = '__all__'
        fk_corso = forms.ModelChoiceField(queryset=CorsoFormazione.objects.all())
        fk_fornitore = forms.ModelChoiceField(queryset=Fornitore.objects.all())
        
        widgets = {
            'data_formazione': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),         
            'fk_corso': forms.Select(attrs={'style':'background_color:#F5F8EC'}),
            'fk_fornitore': forms.Select(attrs={'style':'background_color:#F5F8EC'}),
            'ore': forms.NumberInput(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),
            'created_by': forms.HiddenInput()
        }
        labels = {
            'data_formazione': 'Data Formazione',
            'fk_corso': 'Corso/Attività',
            'fk_fornitore': 'Ente che ha fornito il servizio',
            'ore': 'Ore totali di formazione',
            'note': 'Annotazioni'
        }
        
# Dettaglio Registro Formazione
class DettaglioRegistroFormazioneModelForm(forms.ModelForm):
    class Meta:
        model = DettaglioRegistroFormazione
        fields = '__all__'
        fk_hr = forms.ModelChoiceField(queryset=HumanResource.objects.all())
        widgets = {
            'fk_registro_formazione': forms.HiddenInput(),            
            'fk_hr': forms.Select(attrs={'style':'background_color:#F5F8EC'}),
            'prossima_scadenza': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),
            'efficace': forms.CheckboxInput(),
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),
            
        }
        labels = {
            'fk_hr': 'Operatore',
            'certificato': 'Certificato',
            'presenza': 'Presenza',
            'efficace': 'Efficace',
            'prossima_scadenza': 'Prossima Scadenza',
            'note': 'Annotazioni'
        }
        
# Registro Ore Lavoro
class RegistroOreLavoroModelForm(forms.ModelForm):
    class Meta:
        model = RegistroOreLavoro
        fields = '__all__'
        
        
        widgets = {
            'entry_year': forms.Select(attrs={'style':'background_color:#F5F8EC'}),
            'entry_month': forms.Select(attrs={'style':'background_color:#F5F8EC'}),
            'ore_lavorabili': forms.NumberInput(attrs={'class': 'form-control', 'style': 'text-align:right; '}),
            'ore_lavorate': forms.NumberInput(attrs={'class': 'form-control', 'style': 'text-align:right; '}),
            'straordinari': forms.NumberInput(attrs={'class': 'form-control', 'style': 'text-align:right; '}),
            'ferie_permessi': forms.NumberInput(attrs={'class': 'form-control', 'style': 'text-align:right; '}),
            'permessi_speciali': forms.NumberInput(attrs={'class': 'form-control', 'style': 'text-align:right; '}),
            'maternità': forms.NumberInput(attrs={'class': 'form-control', 'style': 'text-align:right; '}),
            'infortunio': forms.NumberInput(attrs={'class': 'form-control', 'style': 'text-align:right; '}),
            'formazione': forms.NumberInput(attrs={'class': 'form-control', 'style': 'text-align:right; '}),
            'formazione_neoassunti': forms.NumberInput(attrs={'class': 'form-control', 'style': 'text-align:right; '}),
            'malattia': forms.NumberInput(attrs={'class': 'form-control', 'style': 'text-align:right; '}),
            'n_infortuni': forms.NumberInput(attrs={'class': 'form-control', 'style': 'text-align:right; '}),
            'n_infortuni_itinere': forms.NumberInput(attrs={'class': 'form-control', 'style': 'text-align:right; '}),
            'n_malattie_professionali': forms.NumberInput(attrs={'class': 'form-control', 'style': 'text-align:right; '}),
            'ore_malattie_professionali': forms.NumberInput(attrs={'class': 'form-control', 'style': 'text-align:right; '}),
            'permessi_non_retribuiti': forms.NumberInput(attrs={'class': 'form-control', 'style': 'text-align:right; '}),
            'assenze_ingiustificate': forms.NumberInput(attrs={'class': 'form-control', 'style': 'text-align:right; '}),
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),
            'created_by': forms.HiddenInput()
        }
        labels = {
            'entry_year': 'Anno',
            'entry_month': 'Mese',
            'ore_lavorabili': 'Ore Lavorabili',
            'ore_lavorate': 'Ore Lavorate',
            'straordinari': 'Straordinari',
            'ferie_permessi': 'Ferie/Permessi',
            'permessi_speciali': 'Permessi Speciali',
            'maternità': 'Maternità',
            'infortunio': 'Infortunio',
            'formazione': 'Formazione',
            'formazione_neoassunti': 'Formazione Neo-assunti',
            'malattia': 'Malattia',
            'n_infortuni': 'N. Infortuni',
            'n_infortuni_itinere': 'N. Infortuni in Itinere',
            'n_malattie_professionali': 'N. Malattie Professionali',
            'ore_malattie_professionali': 'Ore Malattie Professionali',
            'permessi_non_retribuiti': 'Permessi non Retribuiti',
            'assenze_ingiustificate': 'Assenze Ingiustificate',
            'note': 'Annotazioni',
            
        }

# XR Valutazione-Operatore
class ValutazioneOperatoreModelForm(forms.ModelForm):
    class Meta:
        model = ValutazioneOperatore
        fields = '__all__' 
        fk_centro_di_lavoro = forms.ModelChoiceField(queryset=CentrodiLavoro.objects.all())     
        widgets = {
            'fk_hr': forms.HiddenInput(),
            'fk_centro_di_lavoro': forms.Select(attrs={'style':'background_color:#F5F8EC'}), 
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),                     
            'created_by': forms.HiddenInput(),
            'created_at': forms.HiddenInput()
        }
        labels = {
            'fk_centro_di_lavoro': 'Centro di Lavoro',
            'valutazione': 'Valutazione',
            'note': 'Annotazioni'
            
        }

# XR Safety_Role-Operatore
class HR_SafetyModelForm(forms.ModelForm):
    class Meta:
        model = HR_Safety
        fields = '__all__' 
        fk_safety_role = forms.ModelChoiceField(queryset=Safety_Role.objects.all())     
        widgets = {
            'fk_hr': forms.HiddenInput(),            
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}), 
            'data_inizio_incarico': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),
            'data_fine_incarico': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),

            'created_by': forms.HiddenInput(),
            
        }
        labels = {
            'fk_safety_role': 'Incarico Sicurezza',            
            'data_inizio_incarico': 'Data Inizio Incarico',
            'data_fine_incarico': 'Data Fine Incarico',
            'note': 'Annotazioni'
            
        }
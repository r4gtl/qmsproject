from django import forms
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField
from .models import Fornitore, Facility, FacilityContact

class FormFornitore(forms.ModelForm):
    class Meta:
        model = Fornitore
        exclude=()
        #fields='__all__'
        ragionesociale = forms.CharField(max_length=100, label="Facility Name")
        indirizzo = forms.CharField()
        cap = forms.CharField()
        city = forms.CharField()
        provincia = forms.CharField()
        country = CountryField().formfield()
        categoria = forms.CharField()
        is_lwg = forms.BooleanField(widget=forms.CheckboxInput(attrs={'onClick': 'myFunction();'}))
        created_by = forms.CharField()
        created_at = forms.DateTimeField()
        widgets = {'country': CountrySelectWidget(),
                # 'created_at': forms.HiddenInput(),
                # 'created_by': forms.HiddenInput()
                }
        labels = {
            'ragionesociale': 'Ragione Sociale',
            'country': 'Paese',
            'city': 'Città',
            'is_lwg': 'LWG'
            
        }


class FormFacility(forms.ModelForm):
    class Meta:
        model = Facility
        exclude=()
        #fields='__all__'
        nome_sito = forms.CharField(max_length=100, label="Facility Name")
        urn = forms.CharField(max_length=50, label="URN Number")
        piva = forms.CharField(max_length=11)
        indirizzo = forms.CharField(max_length=100)
        cap = forms.CharField(max_length=5)
        city = forms.CharField(max_length=100)
        provincia = forms.CharField(max_length=2)
        country = CountryField().formfield()
        phone = forms.CharField(max_length=50)
        primary_cat = forms.CharField(label="Categoria primaria")
        secondary_cat = forms.CharField(label="Categoria secondaria")
        tertiary_cat = forms.CharField(label="Categoria terziaria")
        latitude = forms.FloatField()
        longitude = forms.FloatField()
        site_area = forms.FloatField()
        facility_description= forms.Textarea()
        created_at = forms.DateTimeField()
        widgets = {'country': CountrySelectWidget(),
                   'created_at': forms.HiddenInput(),
                   'nome_sito': forms.TextInput(attrs={'placeholder': 'Inserisci nome azienda'}),
                   'urn': forms.TextInput(attrs={'placeholder': 'Inserisci URN'}),
                   'facility_description': forms.Textarea(attrs={'placeholder': 'Inserisci una descrizione per l\'azienda'}),
                   }
        labels = {
            'nome_sito': 'Facility Name',
            'country': 'Paese',
            'primary_cat': 'Categoria Primaria',
            'secondary_cat': 'Categoria Secondaria',
            'tertiary_cat': 'Categoria Terziaria',
            'site_area': 'Superficie del Sito',
            'latitude': 'Latitudine',
            'longitude': 'Longitudine',
            'facility_description': 'Descrizione Azienda'
        }
        
class FormFacilityContact(forms.ModelForm):
    class Meta:
        model = FacilityContact
        exclude=()
        fk_facility = forms.IntegerField()
        contact_type = forms.CharField(max_length=100)
        name = forms.CharField(max_length=100)
        position = forms.CharField(max_length=100)
        email = forms.EmailField()
        widgets = {'fk_facility': forms.HiddenInput(),
                   'name': forms.TextInput(attrs={'placeholder': 'Nome e cognome'}),
                   'position': forms.TextInput(attrs={'placeholder': 'posizione'}),
                   
                   }

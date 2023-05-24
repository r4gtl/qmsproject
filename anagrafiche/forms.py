from django import forms
from django_countries.widgets import CountrySelectWidget
from .models import Fornitore, Facility

class FormFornitore(forms.ModelForm):
    class Meta:
        model = Fornitore
        fields='__all__'
        widgets = {'country': CountrySelectWidget()}
        
class FormFacility(forms.ModelForm):
    class Meta:
        model = Facility
        fields='__all__'
        widgets = {'country': CountrySelectWidget()}
import django_filters
from django import forms
from .models import Autorizzazione, DettaglioScadenzaAutorizzazione

class AutorizzazioneFilter(django_filters.FilterSet):   
   
    descrizione=django_filters.CharFilter(field_name='descrizione', lookup_expr='icontains', label='', widget=forms.TextInput(attrs={'style': 'width: 60%; margin-left: 5%'}))
    rilasciata_da=django_filters.CharFilter(field_name='rilasciata_da', lookup_expr='icontains', label='', widget=forms.TextInput(attrs={'style': 'width: 60%; margin-left: 5%'}))
    
    class Meta:
        model = Autorizzazione
        fields = ['descrizione', 'rilasciata_da']
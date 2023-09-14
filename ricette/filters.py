import django_filters
from django_filters.widgets import BooleanWidget
from django import forms
from .models import *


class OperazioneFilter(django_filters.FilterSet):
    
    descrizione=django_filters.CharFilter(field_name='descrizione', lookup_expr='icontains', widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'}))
    ward_ref=django_filters.CharFilter(field_name='ward_ref', lookup_expr='icontains', widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'}))
    
    class Meta:
        model = OperazioneRicette
        fields = ['descrizione', 'ward_ref']
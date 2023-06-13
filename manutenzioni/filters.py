import django_filters
from django import forms
from .models import Attrezzatura


class AttrezzaturaFilter(django_filters.FilterSet):
    codice_attrezzatura=django_filters.CharFilter(lookup_expr='icontains', label='Codice Attrezzatura')
    descrizione=django_filters.CharFilter(lookup_expr='icontains', label='Descrizione')
    
    class Meta:
        model = Attrezzatura
        fields = ['codice_attrezzatura',
                'descrizione'
                ] 
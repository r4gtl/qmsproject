import django_filters
from django import forms
from .models import Articolo, Colore


class ArticoloFilter(django_filters.FilterSet):
    descrizione=django_filters.CharFilter(lookup_expr='icontains', label='Descrizione')
    
    
    class Meta:
        model = Articolo
        fields = ['descrizione'
                ] 
        

class ColoreFilter(django_filters.FilterSet):
    descrizione=django_filters.CharFilter(lookup_expr='icontains', label='Descrizione')
    
    
    class Meta:
        model = Colore
        fields = ['descrizione'
                ] 
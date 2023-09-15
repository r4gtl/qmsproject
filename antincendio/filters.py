import django_filters
from django_filters.widgets import BooleanWidget
from django import forms
from .models import *



class EstintoreFilter(django_filters.FilterSet):
    
    classe=django_filters.CharFilter(field_name='classe', lookup_expr='icontains', widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'}))
    matricola=django_filters.CharFilter(field_name='matricola', lookup_expr='icontains', widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'}))
    
    class Meta:
        model = Estintore
        fields = ['classe', 'matricola']


class IdranteFilter(django_filters.FilterSet):
    
    numero_posizione=django_filters.CharFilter(field_name='numero_posizione', lookup_expr='icontains', widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'}))
    tipo_idrante=django_filters.CharFilter(field_name='tipo_idrante', lookup_expr='icontains', widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'}))
    
    class Meta:
        model = Idrante
        fields = ['numero_posizione', 'tipo_idrante']


class PortaUscitaFilter(django_filters.FilterSet):
    
    numero_posizione=django_filters.CharFilter(field_name='numero_posizione', lookup_expr='icontains', widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'}))
    tipo_porta = django_filters.ChoiceFilter(
        field_name='tipo_porta',
        lookup_expr='icontains',
        widget=forms.Select(attrs={'style': 'width: 90%; margin-left: 5%'}),
        choices=PortaUscita.CHOICES_DOOR  # Usa le scelte definite nel modello
    )
    
    
    class Meta:
        model = PortaUscita
        fields = ['numero_posizione', 'tipo_porta']
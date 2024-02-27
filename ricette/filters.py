import django_filters
from django import forms
from django_filters.widgets import BooleanWidget

from .models import *


class OperazioneFilter(django_filters.FilterSet):
    
    descrizione=django_filters.CharFilter(field_name='descrizione', lookup_expr='icontains', widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'}))
    ward_ref=django_filters.CharFilter(field_name='ward_ref', lookup_expr='icontains', widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'}))
    
    class Meta:
        model = OperazioneRicette
        fields = ['descrizione', 'ward_ref']


class RicettaRifinizioneFilter(django_filters.FilterSet):
    
    numero_ricetta=django_filters.CharFilter(
        field_name='numero_ricetta', 
        lookup_expr='icontains', 
        label='Numero ricetta',
        widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'}))
    
    numero_revisione=django_filters.CharFilter(
        field_name='numero_revisione', 
        lookup_expr='icontains', 
        label='Numero Revisione',
        widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'}))
    
    descrizione_articolo = django_filters.CharFilter(
        field_name='fk_articolo__descrizione',  # Utilizza il campo descrizione di fk_articolo
        lookup_expr='icontains',
        label='Descrizione Articolo',  # Etichetta per il campo
        widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'})
    )
    
    class Meta:
        model = RicettaRifinizione
        fields = ['numero_ricetta', 'numero_revisione', 'descrizione_articolo']


class RicettaColoreRifinizioneFilter(django_filters.FilterSet):
    
    numero_ricetta=django_filters.CharFilter(
        field_name='numero_ricetta', 
        lookup_expr='icontains', 
        label='Numero ricetta',
        widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'}))
    
    numero_revisione=django_filters.CharFilter(
        field_name='numero_revisione', 
        lookup_expr='icontains', 
        label='Numero Revisione',
        widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'}))
    
    descrizione_articolo = django_filters.CharFilter(
        field_name='fk_articolo__descrizione',  # Utilizza il campo descrizione di fk_articolo
        lookup_expr='icontains',
        label='Descrizione Articolo',  # Etichetta per il campo
        widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'})
    )

    descrizione_colore = django_filters.CharFilter(
        field_name='fk_colore__descrizione',  # Utilizza il campo descrizione di fk_articolo
        lookup_expr='icontains',
        label='Descrizione Colore',  # Etichetta per il campo
        widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'})
    )
    
    class Meta:
        model = RicettaColoreRifinizione
        fields = ['numero_ricetta', 'numero_revisione', 'descrizione_articolo', 'descrizione_colore']




class RicettaBagnatoFilter(django_filters.FilterSet):
    
    numero_ricetta=django_filters.CharFilter(
        field_name='numero_ricetta', 
        lookup_expr='icontains', 
        label='Numero ricetta',
        widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'}))
    
    numero_revisione=django_filters.CharFilter(
        field_name='numero_revisione', 
        lookup_expr='icontains', 
        label='Numero Revisione',
        widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'}))
    
    descrizione_articolo = django_filters.CharFilter(
        field_name='fk_articolo__descrizione',  # Utilizza il campo descrizione di fk_articolo
        lookup_expr='icontains',
        label='Descrizione Articolo',  # Etichetta per il campo
        widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'})
    )

    descrizione_tipo_pelli = django_filters.CharFilter(
        field_name='fk_tipogrezzo__descrizione',  # Utilizza il campo descrizione di fk_articolo
        lookup_expr='icontains',
        label='Tipo Grezzo',  # Etichetta per il campo
        widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'})
    )

    descrizione_tipo_animale = django_filters.CharFilter(
        field_name='fk_tipoanimale__descrizione',  # Utilizza il campo descrizione di fk_articolo
        lookup_expr='icontains',
        label='Tipo Animale',  # Etichetta per il campo
        widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'})
    )
    
    class Meta:
        model = RicettaBagnato
        fields = ['numero_ricetta', 'numero_revisione', 'descrizione_articolo', 'descrizione_tipo_pelli', 'descrizione_tipo_animale']
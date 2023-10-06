import django_filters
from django_filters.widgets import BooleanWidget
from django import forms
from .models import *
from anagrafiche.models import Fornitore
from human_resources.models import HumanResource




class EstintoreFilter(django_filters.FilterSet):
    
    classe=django_filters.CharFilter(field_name='classe', lookup_expr='icontains', widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'}))
    matricola=django_filters.CharFilter(field_name='matricola', lookup_expr='icontains', widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'}))
    
    class Meta:
        model = Estintore
        fields = ['classe', 'matricola']


class IdranteFilter(django_filters.FilterSet):
    
    numero_posizione=django_filters.CharFilter(field_name='numero_posizione', lookup_expr='icontains', widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'}))
    tipo_idrante=django_filters.ChoiceFilter(
        field_name='tipo_idrante', 
        lookup_expr='icontains', 
        widget=forms.Select(attrs={'style': 'width: 90%; margin-left: 5%'}),
        choices=Idrante.CHOICES_TYPE  # Usa le scelte definite nel modello
        )
    
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

class AttrezzaturaAntincendioFilter(django_filters.FilterSet):
    
    descrizione = django_filters.CharFilter(field_name='descrizione', lookup_expr='icontains', widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'}))
    class Meta:
        model = AttrezzaturaAntincendio
        fields = ['descrizione']

class ImpiantoSpegnimentoFilter(django_filters.FilterSet):
    
    numero_posizione = django_filters.CharFilter(field_name='numero_posizione', lookup_expr='icontains', widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'}))
    ubicazione = django_filters.CharFilter(field_name='ubicazione', lookup_expr='icontains', widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'}))
    class Meta:
        model = ImpiantoSpegnimento
        fields = ['numero_posizione', 'ubicazione']



class RegistroControlliAntincendioFilter(django_filters.FilterSet):
    
    interno_esterno = django_filters.ChoiceFilter(
        field_name='interno_esterno',
        lookup_expr='icontains',
        widget=forms.Select(attrs={'style': 'width: 90%; margin-left: 5%'}),
        choices=RegistroControlliAntincendio.CHOICES_INT_EST  # Usa le scelte definite nel modello
    )
    fk_fornitore = django_filters.ModelChoiceFilter(
        field_name='fk_fornitore',
        queryset=Fornitore.objects.all(),
        label='Fornitore'
    )
    fk_operatore= django_filters.ModelChoiceFilter(
        field_name='fk_operatore',
        queryset=HumanResource.objects.all(),
        label='Operatore'
    )
    data_intervento=django_filters.DateFromToRangeFilter()
    
    
    class Meta:
        model = RegistroControlliAntincendio
        fields = ['interno_esterno', 'fk_fornitore', 'fk_operatore', 'data_intervento']
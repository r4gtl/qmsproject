import django_filters
from django_filters.widgets import BooleanWidget
from django import forms
from .models import (ProdottoChimico, Sostanza, 
                    SostanzaSVHC, HazardStatement,
                    PrecautionaryStatement, SimboloGHS,
                    ImballaggioPC, OrdineProdottoChimico,
                    AcquistoProdottoChimico,
)
from anagrafiche.models import Fornitore




class ProdottoChimicoFilter(django_filters.FilterSet):
    
    descrizione=django_filters.CharFilter(field_name='descrizione', lookup_expr='icontains', widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'}))
    fk_fornitore = django_filters.ModelChoiceFilter(
        field_name='fk_fornitore',
        queryset=Fornitore.objects.filter(categoria=Fornitore.PRODOTTI_CHIMICI),
        label='Fornitore'
    )
    
    class Meta:
        model = ProdottoChimico
        fields = ['descrizione', 'fk_fornitore']



class SostanzaFilter(django_filters.FilterSet):
    
    num_cas=django_filters.CharFilter(field_name='num_cas', lookup_expr='icontains', widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'}))
    num_ec=django_filters.CharFilter(field_name='num_cas', lookup_expr='icontains', widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'}))
    
    class Meta:
        model = Sostanza
        fields = ['num_cas', 'num_ec']



class SostanzaSVHCFilter(django_filters.FilterSet):
    
    num_cas_svhc=django_filters.CharFilter(field_name='num_cas', lookup_expr='icontains', widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'}))
    num_ec_svhc=django_filters.CharFilter(field_name='num_cas', lookup_expr='icontains', widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'}))
    
    class Meta:
        model = SostanzaSVHC
        fields = ['num_cas', 'num_ec']



class HazardStatementFilter(django_filters.FilterSet):
    
    hazard_statement=django_filters.CharFilter(field_name='hazard_statement', lookup_expr='icontains', widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'}))    
    hazard_category = django_filters.ChoiceFilter(choices=HazardStatement.CHOICES_HAZARD_CAT)

    class Meta:
        model = HazardStatement
        fields = ['hazard_statement', 'hazard_category']


class PrecautionaryStatementFilter(django_filters.FilterSet):
    
    codice=django_filters.CharFilter(field_name='codice', lookup_expr='icontains', widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'}))    
    descrizione = django_filters.CharFilter(field_name='descrizione', lookup_expr='icontains', widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'}))    
    
    class Meta:
        model = PrecautionaryStatement
        fields = ['codice', 'descrizione']



class SimboloGHSFilter(django_filters.FilterSet):
    
    codice=django_filters.CharFilter(field_name='codice', lookup_expr='icontains', widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'}))    
    
    
    class Meta:
        model = SimboloGHS
        fields = ['codice']

class ImballaggioPCFilter(django_filters.FilterSet):
    
    descrizione=django_filters.CharFilter(field_name='codice', lookup_expr='icontains', widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'}))    
    
    
    class Meta:
        model = ImballaggioPC
        fields = ['descrizione']
        


class OrdineProdottoChimicoFilter(django_filters.FilterSet):
    
    fk_fornitore = django_filters.ModelChoiceFilter(
        field_name='fk_fornitore',
        queryset=Fornitore.objects.filter(categoria=Fornitore.PRODOTTI_CHIMICI),
        label='Fornitore'
    )
    numero_ordine=django_filters.NumberFilter(field_name='numero_ordine', lookup_expr='icontains', widget=forms.NumberInput(attrs={'style': 'width: 90%; margin-left: 5%'}))
    data_ordine = django_filters.DateFromToRangeFilter()
    data_consegna = django_filters.DateFromToRangeFilter()
    is_conforme = django_filters.BooleanFilter(field_name='is_conforme', widget=BooleanWidget())
    class Meta:
        model = OrdineProdottoChimico
        fields = ['fk_fornitore', 'numero_ordine', 
                'data_ordine', 'data_consegna',
                'is_conforme'
                ]
        
class AcquistoProdottoChimicoFilter(django_filters.FilterSet):
    
    fk_fornitore = django_filters.ModelChoiceFilter(
        field_name='fk_fornitore',
        queryset=Fornitore.objects.filter(categoria=Fornitore.PRODOTTI_CHIMICI),
        label='Fornitore'
    )
    numero_documento=django_filters.NumberFilter(field_name='numero_documento', lookup_expr='icontains', widget=forms.NumberInput(attrs={'style': 'width: 90%; margin-left: 5%'}))
    data_documento = django_filters.DateFromToRangeFilter()
    
    class Meta:
        model = AcquistoProdottoChimico
        fields = ['fk_fornitore', 'numero_documento', 
                'data_documento'
                ]
import django_filters
from anagrafiche.models import Cliente
from django import forms
from django_filters.widgets import BooleanWidget

from .models import OrdineCliente, SchedaLavorazione


class OrdineClienteFilter(django_filters.FilterSet):
    
    numero_ordine=django_filters.CharFilter(field_name='numero_ordine', lookup_expr='icontains', widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'}))
    fk_cliente = django_filters.ModelChoiceFilter(
        field_name='fk_cliente',
        queryset=Cliente.objects.all(),
        label='Cliente'
    )
    
    class Meta:
        model = OrdineCliente
        fields = ['numero_ordine', 'fk_cliente']


class SchedaLavorazioneFilter(django_filters.FilterSet):
    numero_scheda = django_filters.NumberFilter(field_name='pk', label='Numero Scheda')

    articolo_descrizione = django_filters.CharFilter(
        field_name='fk_articolo__descrizione',
        lookup_expr='icontains',
        label='Descrizione Articolo'
    )

    colore_descrizione = django_filters.CharFilter(
        field_name='fk_colore__descrizione',
        lookup_expr='icontains',
        label='Descrizione Colore'
    )

    numero_ordine = django_filters.CharFilter(
        field_name='fk_dettaglio_ordine_cliente__fk_ordine__numero_ordine',
        lookup_expr='icontains',
        label='Numero Ordine'
    )

    data_scheda_da = django_filters.DateFilter(
        field_name='data_scheda',
        lookup_expr='gte',
        label='Data Scheda Da'
    )

    data_scheda_a = django_filters.DateFilter(
        field_name='data_scheda',
        lookup_expr='lte',
        label='Data Scheda A'
    )

    scheda_chiusa = django_filters.BooleanFilter(
        field_name='scheda_chiusa',
        label='Scheda Chiusa'
    )

    class Meta:
        model = SchedaLavorazione
        fields = []
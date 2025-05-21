import django_filters
from anagrafiche.models import Cliente
from django import forms
from django_filters.widgets import BooleanWidget

from .models import OrdineCliente


class OrdineClienteFilter(django_filters.FilterSet):
    
    numero_ordine=django_filters.CharFilter(field_name='numero_ordine', lookup_expr='icontains', widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'}))
    fk_cliente = django_filters.ModelChoiceFilter(
        field_name='fk_cliente',
        queryset=Cliente.objects.all(),
        label='Cliente'
    )
    
    class Meta:
        model = OrdineCliente
        fields = ['numero_ordine', 'cliente']
        
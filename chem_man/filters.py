import django_filters
from django import forms
from .models import ProdottoChimico
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
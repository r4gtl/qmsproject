import django_filters
from django import forms
from .models import Fornitore, Cliente




class FornitoreFilter(django_filters.FilterSet):
    
    #
    # Categoria
    NESSUNA = 'nessuna'
    PELLI = 'pelli'
    PRODOTTI_CHIMICI = 'prodotti chimici'
    LAVORAZIONI_ESTERNE = 'lavorazioni esterne'
    SERVIZI = 'servizi'
    
    CHOICES_CATEGORY = (
        (NESSUNA, 'Manca categoria'),
        (PELLI, 'Pelli'),
        (PRODOTTI_CHIMICI, 'Prodotti Chimici'),
        (LAVORAZIONI_ESTERNE, 'Lavorazioni Esterne'),
        (SERVIZI, 'Servizi')
    )
    ragionesociale=django_filters.CharFilter(field_name='ragionesociale', lookup_expr='icontains', widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'}))
    categoria=django_filters.ChoiceFilter(choices=CHOICES_CATEGORY)
    
    class Meta:
        model = Fornitore
        fields = ['ragionesociale', 'categoria']



class ClienteFilter(django_filters.FilterSet):   
   
    ragionesociale=django_filters.CharFilter(field_name='ragionesociale', lookup_expr='icontains', widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'}))
    
    class Meta:
        model = Cliente
        fields = ['ragionesociale']
import django_filters
from django import forms
from .models import MovimentoRifiuti, CodiceCER, CodiceSmaltRec

class MovimentoRifiutiFilter(django_filters.FilterSet):   
    # Carico o Scarico
    CARICO = 'carico'
    SCARICO = 'scarico'
    
    
    CHOICES_CAR_SCAR = (
        (CARICO, 'Carico'),
        (SCARICO, 'Scarico'),        
    )

    data_movimento = django_filters.DateFromToRangeFilter()
    fk_codicecer = django_filters.ModelChoiceFilter(queryset=CodiceCER.objects.all(),
                                                empty_label="Tutti i Codici",
                                                label='Codice CER',
                                                widget=forms.Select(attrs={'class': 'form-control'})
                                                )
    car_scar= django_filters.ChoiceFilter(choices=CHOICES_CAR_SCAR)
    fk_smaltrec = django_filters.ModelChoiceFilter(queryset=CodiceSmaltRec.objects.all(),
                                                empty_label="Tutti i Codici",
                                                label='Codice Smaltimento/Recupero',
                                                widget=forms.Select(attrs={'class': 'form-control'})
                                                )

    class Meta:
        model = MovimentoRifiuti
        fields = ['data_movimento', 'fk_codicecer','car_scar', 'fk_smaltrec']


     
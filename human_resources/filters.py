import django_filters
from django import forms
from .models import HumanResource, Ward, Role



        
class HRFilter(django_filters.FilterSet):
    cognomedipendente=django_filters.CharFilter(lookup_expr='icontains', label='Cognome')
    nomedipendente=django_filters.CharFilter(lookup_expr='icontains', label='Nome')
    fk_reparto=django_filters.ModelChoiceFilter(queryset=Ward.objects.all(),
                                                empty_label="Tutti i reparti",
                                                label='Reparto',
                                                widget=forms.Select(attrs={'class': 'form-control'})
                                                )
    fk_mansione=django_filters.ModelChoiceFilter(queryset=Role.objects.all(),
                                                empty_label="Tutte le mansioni",
                                                label='Mansione',
                                                widget=forms.Select(attrs={'class': 'form-control'})
                                                )
    
    class Meta:
        model = HumanResource
        fields = ['cognomedipendente', 'nomedipendente',
                'fk_reparto', 'fk_mansione', 
                ] 
import django_filters
from .models import HumanResource


        
class HRFilter(django_filters.FilterSet):
    cognomedipendente=django_filters.CharFilter(lookup_expr='icontains', label='Cognome')
    nomedipendente=django_filters.CharFilter(lookup_expr='icontains', label='Nome')
    class Meta:
        model = HumanResource
        fields = ['cognomedipendente', 'nomedipendente',] 
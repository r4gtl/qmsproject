import django_filters
from django import forms
from .models import Procedura, SezioneLWG


class ProceduraFilter(django_filters.FilterSet):
    descrizione=django_filters.CharFilter(lookup_expr='icontains', label='Descrizione')
    fk_lwgsection=django_filters.ModelChoiceFilter(queryset=SezioneLWG.objects.all(),
                                                empty_label="Tutte le sezioni LWG",
                                                label='Sezione LWG',
                                                widget=forms.Select(attrs={'class': 'form-control'})
                                                )
    
    class Meta:
        model = Procedura
        fields = ['descrizione',
                  'fk_lwgsection'
                ] 
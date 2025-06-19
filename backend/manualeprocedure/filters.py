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
    
    def __init__(self, *args, **kwargs):
        fk_lwgsection_value = kwargs.pop('fk_lwgsection', None)
        super(ProceduraFilter, self).__init__(*args, **kwargs)
        
        if fk_lwgsection_value:
            self.filters['fk_lwgsection'].extra.update(
                {'initial': fk_lwgsection_value}
            )
    
    class Meta:
        model = Procedura
        fields = ['descrizione',
                  'fk_lwgsection'
                ] 
import django_filters
from django_filters.filters import BooleanFilter
from django.db.models.fields import BooleanField
from .models import *
from django import forms
from .models import Attrezzatura



class MyBooleanFilter(django_filters.ChoiceFilter):
    '''Filtro per visualizzare tutti i valori indipendentemente se vero o falso
        realizzato con ChatGpt.
    '''
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('choices', (            
            (True, 'Sì'),
            (False, 'No'),
        ))
        super().__init__(*args, **kwargs)

    def filter(self, qs, value):
        if value is None:
            return qs
        elif value:
            return qs.filter(**{self.field_name: True})
        else:
            return qs


class AttrezzaturaFilter(django_filters.FilterSet):
    codice_attrezzatura=django_filters.CharFilter(lookup_expr='icontains', widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'}), label='Codice Attrezzatura')
    descrizione=django_filters.CharFilter(lookup_expr='icontains', widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'}), label='Descrizione')
    #is_taratura=django_filters.BooleanFilter(method='unchecked_means_any_value')
    is_taratura=MyBooleanFilter(field_name='is_taratura')
    
    class Meta:
        model = Attrezzatura
        fields = ['codice_attrezzatura',
                'descrizione',
                'is_taratura',
                'is_dismesso'
                ] 
        filter_overrides = {
                
                models.BooleanField: {
                    'filter_class': django_filters.BooleanFilter,
                    'extra': lambda f: {
                        
                        'widget' : forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'align-center'})
                    },
                }
            }
        widgets = {
        'is_dismesso': BooleanFilter(attrs={'class': 'form-control'})
    }
        

    def unchecked_means_any_value(self, queryset, name, value):
        if value is None:
            return queryset
        elif value is False:
            return queryset.all()
        else:
            return queryset.filter(**{name: value})
    
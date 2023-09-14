import django_filters
from django_filters.widgets import BooleanWidget
from django import forms
from .models import *



class EstintoreFilter(django_filters.FilterSet):
    
    classe=django_filters.CharFilter(field_name='classe', lookup_expr='icontains', widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'}))
    matricola=django_filters.CharFilter(field_name='matricola', lookup_expr='icontains', widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'}))
    
    class Meta:
        model = Estintore
        fields = ['classe', 'matricola']

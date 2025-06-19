from django.contrib import admin

from .models import *


class EstintoreModelAdmin(admin.ModelAdmin):
    model = Estintore
    list_display = ['tipo_estinguente', 'classe', 'matricola', 'numero_posizione']
    search_fields = ['matricola'] 
    ordering = ['numero_posizione']

class IdranteModelAdmin(admin.ModelAdmin):
    model = Idrante
    list_display = ['numero_posizione', 'tipo_idrante']
    search_fields = ['numero_posizione'] 
    ordering = ['numero_posizione']

class ImpiantoSpegnimentoModelAdmin(admin.ModelAdmin):
    model = ImpiantoSpegnimento
    list_display = ['numero_posizione', 'ubicazione']
    search_fields = ['numero_posizione'] 
    ordering = ['numero_posizione']



admin.site.register(Estintore, EstintoreModelAdmin)
admin.site.register(Idrante, IdranteModelAdmin)
admin.site.register(ImpiantoSpegnimento, ImpiantoSpegnimentoModelAdmin)
from django.contrib import admin

from .models import *


class PuntoEmissioneModelAdmin(admin.ModelAdmin):
    model = PuntoEmissione
    list_display = ['camino_numero', 'origine', 'quota', 'portata', 'soggetto_controllo']
    search_fields = ['camino_numero'] 
    ordering = ['camino_numero']


class RegistroControlloAnaliticoModelAdmin(admin.ModelAdmin):
    model = RegistroControlloAnalitico
    list_display = ['fk_punto_emissione', 'data_prelievo', 'certificato_numero']
    search_fields = ['data_prelievo'] 
    ordering = ['-data_prelievo']



admin.site.register(PuntoEmissione, PuntoEmissioneModelAdmin)
admin.site.register(RegistroControlloAnalitico, RegistroControlloAnaliticoModelAdmin)


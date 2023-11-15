from django.contrib import admin

from .models import (AreaFormazione, CentrodiLavoro, CorsoFormazione,
                     HumanResource, RegistroFormazione, RegistroOreLavoro,
                     ValutazioneOperatore)


class HumanResourceModelAdmin(admin.ModelAdmin):
    model = HumanResource
    list_display = [         
        "cognomedipendente", 
        "nomedipendente", 
        "dataassunzione",         
        "datadimissioni",
        ]
    search_fields = ["cognomedipendente", "nomedipendente"]
    ordering = ['cognomedipendente']

class AreaFormazioneModelAdmin(admin.ModelAdmin):
    model = AreaFormazione
    list_display = [         
        "descrizione",         
        ]
    search_fields = ["descrizione"]
    ordering = ['descrizione']

class CorsoFormazioneModelAdmin(admin.ModelAdmin):
    model = CorsoFormazione
    list_display = [         
        "descrizione", 
        "fk_areaformazione"        
        ]
    search_fields = ["descrizione"]
    ordering = ['descrizione']

class RegistroFormazioneModelAdmin(admin.ModelAdmin):
    model = RegistroFormazione
    list_display = [         
        "data_formazione", 
        "fk_corso",
        "fk_fornitore",
        "ore"
        ]
    search_fields = ["data_formazione"]
    ordering = ['-data_formazione']


class RegistroOreLavoroModelAdmin(admin.ModelAdmin):
    model = RegistroOreLavoro
    list_display = [         
        "entry_year", 
        "entry_month",        
        ]
    search_fields = ["entry_year", "entry_month"]
    ordering = ['-entry_year']


class ValutazioneOperatoreModelAdmin(admin.ModelAdmin):
    model = ValutazioneOperatore
    list_display = [         
        "fk_hr", 
        "fk_centro_di_lavoro",  
        "valutazione"      
        ]
    search_fields = ["fk_hr"]
    ordering = ['fk_hr']

class CentrodiLavoroModelAdmin(admin.ModelAdmin):
    model = CentrodiLavoro
    list_display = [         
        "description"
        ]
    search_fields = ["description"]
    ordering = ['description']



admin.site.register(HumanResource, HumanResourceModelAdmin)
admin.site.register(AreaFormazione, AreaFormazioneModelAdmin)
admin.site.register(CorsoFormazione, CorsoFormazioneModelAdmin)
admin.site.register(RegistroFormazione, RegistroFormazioneModelAdmin)
admin.site.register(RegistroOreLavoro, RegistroOreLavoroModelAdmin)
admin.site.register(CentrodiLavoro, CentrodiLavoroModelAdmin)
admin.site.register(ValutazioneOperatore, ValutazioneOperatoreModelAdmin)

from django.contrib import admin

# Register your models here.

from .models import (Attrezzatura,
                    ManutenzioneStraordinaria, ManutenzioneOrdinaria,
                    Taratura
                    )

admin.site.register(Attrezzatura)
admin.site.register(ManutenzioneStraordinaria)
admin.site.register(ManutenzioneOrdinaria)
admin.site.register(Taratura)

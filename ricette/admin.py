from django.contrib import admin

from .models import *

admin.site.register(OperazioneRicette)
admin.site.register(RicettaBagnato)
admin.site.register(RevisioneRicettaBagnato)
admin.site.register(RicettaFondo)
admin.site.register(RevisioneRicettaFondo)
admin.site.register(RicettaRifinizione)

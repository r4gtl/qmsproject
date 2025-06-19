from django.contrib import admin

from .models import (  # FornitoreServizi, FornitoreLavorazioniEsterne, FornitorePelli, FornitoreProdottiChimici
    Cliente, Facility, FacilityContact, Fornitore, LwgFornitore, TransferValue)

# Register your models here.


admin.site.register(Fornitore)
admin.site.register(Facility)
admin.site.register(FacilityContact)
admin.site.register(Cliente)
admin.site.register(LwgFornitore)
admin.site.register(TransferValue)
#admin.site.register(FornitoreServizi)
#admin.site.register(FornitoreLavorazioniEsterne)
#admin.site.register(FornitorePelli)
#admin.site.register(FornitoreProdottiChimici)

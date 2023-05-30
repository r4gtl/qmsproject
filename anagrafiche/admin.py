from django.contrib import admin

# Register your models here.

from .models import (Fornitore, Facility,
                      FacilityContact, Cliente,
                        LwgFornitore, TransferValue
                        )

admin.site.register(Fornitore)
admin.site.register(Facility)
admin.site.register(FacilityContact)
admin.site.register(Cliente)
admin.site.register(LwgFornitore)
admin.site.register(TransferValue)

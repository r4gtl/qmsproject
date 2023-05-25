from django.contrib import admin

# Register your models here.

from .models import Fornitore, Facility, FacilityContact

admin.site.register(Fornitore)
admin.site.register(Facility)
admin.site.register(FacilityContact)

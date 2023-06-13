from django.contrib import admin

# Register your models here.

from .models import (MonitoraggioAcqua,
                     MonitoraggioGas, MonitoraggioEnergiaElettrica,                     
                    )

admin.site.register(MonitoraggioAcqua)
admin.site.register(MonitoraggioGas)
admin.site.register(MonitoraggioEnergiaElettrica)


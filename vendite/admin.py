from django.contrib import admin

from .models import DettaglioOrdineCliente, OrdineCliente

admin.site.register(OrdineCliente)
admin.site.register(DettaglioOrdineCliente)



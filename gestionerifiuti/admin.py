from django.contrib import admin

# Register your models here.

from .models import (CodiceCER, CodiceSmaltRec,
                      MovimentoRifiuti
                        )

admin.site.register(CodiceCER)
admin.site.register(CodiceSmaltRec)
admin.site.register(MovimentoRifiuti)

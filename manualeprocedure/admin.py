from django.contrib import admin

# Register your models here.

from .models import (SezioneLWG,
                     Procedura, RevisioneProcedura,
                     Modulo, RevisioneModulo
                    )

admin.site.register(SezioneLWG)
admin.site.register(Procedura)
admin.site.register(RevisioneProcedura)
admin.site.register(Modulo)
admin.site.register(RevisioneModulo)

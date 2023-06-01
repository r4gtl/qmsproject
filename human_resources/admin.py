from django.contrib import admin
from .models import (
    HumanResource, AreaFormazione, CorsoFormazione
    )


class HumanResourceModelAdmin(admin.ModelAdmin):
    model = HumanResource
    list_display = [         
        "cognomedipendente", 
        "nomedipendente", 
        "dataassunzione",         
        "datadimissioni",
        ]
    search_fields = ["cognomedipendente", "nomedipendente"]


admin.site.register(HumanResource, HumanResourceModelAdmin)
admin.site.register(AreaFormazione)
admin.site.register(CorsoFormazione)

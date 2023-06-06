from django.http import JsonResponse
from django.db.models import Sum, Count

from .models import (HumanResource, 
                    RegistroFormazione, 
                    )


# Charts
def ore_formazione(request):
    labels = []
    data = []

    queryset = RegistroFormazione.objects.values('fk_corso__fk_areaformazione__descrizione').annotate(ore_formazione=Sum('ore'))
    for entry in queryset:
        labels.append(entry['fk_corso__fk_areaformazione__descrizione'])
        data.append(entry['ore_formazione'])
        
    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

def operatori_per_reparto(request):
    labels = []
    data = []

    queryset = HumanResource.objects.values('fk_reparto__description').annotate(hr_count=Count('pk'))
    for entry in queryset:
        labels.append(entry['fk_reparto__description'])
        data.append(entry['hr_count'])
        print("label: " + str(labels))
        print("dati: " +str(data))
    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })
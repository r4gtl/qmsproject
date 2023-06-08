from django.http import JsonResponse
from django.db.models import Sum, Count
from datetime import datetime

from .models import (HumanResource, 
                    RegistroFormazione, 

                    )


def get_years_from_delta(d):
    days_in_year = 365
    return int(d.days / days_in_year)


def get_average_age():
    hrs = HumanResource.objects.filter(datadimissioni__isnull=True).filter(data_nascita__isnull=False)
    days_in_year = 365
    ages = []

    for hr in hrs:
        data_nascita=str(hr.data_nascita)
        dt = datetime.strptime(data_nascita, '%Y-%m-%d')         
        in_days = datetime.now() - dt
        in_years = int(in_days.days / days_in_year)
        ages.append(in_years)

        print("Anni:" + str(in_years))
    avg_age = sum(ages) / len(ages)
    print("Media:" + str(avg_age))
    return avg_age


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
from django.http import JsonResponse
from django.db.models import Sum, Count
from datetime import datetime

from .models import (HumanResource, 
                    RegistroFormazione, 

                    )



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

        
    avg_age = sum(ages) / len(ages)    
    return avg_age

def get_gender_perc(gender):
    hrs = HumanResource.objects.filter(datadimissioni__isnull=True)
    hrs_count = hrs.count()
    print("Conto: " + str(hrs_count))
    my_gender = 0

    for hr in hrs:
        gender_choice = hr.gender
        print("Nome: " + str(hr.cognomedipendente) + " " + str(hr.nomedipendente))
        print("Genere: " + str(gender_choice))
        if gender_choice==gender:
            my_gender+=1

    if my_gender==0:
        return 0
    else:
        return (my_gender /hrs_count )*100


def get_ita_perc():
    hrs = HumanResource.objects.filter(datadimissioni__isnull=True)
    hrs_count = hrs.count()
    
    it = 0
    not_it = 0

    for hr in hrs:
        country_choice = hr.country
        
        if country_choice=="IT":
            it+=1
        else:
            not_it+=1

    if it==0:
        return 0
    else:
        return (it / hrs_count )*100


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

def age_groups(request):

    hrs = HumanResource.objects.filter(datadimissioni__isnull=True).filter(data_nascita__isnull=False)
    days_in_year = 365
    
    labels = ['18-30', '31-40', '41-50', '51-60', '>60']
    data = [0,0,0,0,0]
    backgroundColor = [
      'rgba(255, 99, 132)',
      'rgba(255, 159, 64)',
      'rgba(255, 205, 86)',
      'rgba(75, 192, 192)',
      'rgba(54, 162, 235)'
    ]

    borderColor = [
      'rgb(255, 99, 132)',
      'rgb(255, 159, 64)',
      'rgb(255, 205, 86)',
      'rgb(75, 192, 192)',
      'rgb(54, 162, 235)'
    ]

    for hr in hrs:
        data_nascita=str(hr.data_nascita)
        dt = datetime.strptime(data_nascita, '%Y-%m-%d')         
        in_days = datetime.now() - dt
        in_years = int(in_days.days / days_in_year)
        if in_years>=18 and in_years<=30:
            data[0]+=1
        elif in_years>=31 and in_years<=40:
            data[1]+=1
        elif in_years>=41 and in_years<=50:
            data[2]+=1
        elif in_years>=51 and in_years<=60:
            data[3]+=1
        elif in_years>60:
            data[4]+=1
   
    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
        'backgroundColor': backgroundColor,
        'borderColor': borderColor
    })
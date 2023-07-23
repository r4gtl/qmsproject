from django.http import JsonResponse
from django.db.models import Sum, Count, Q
from django.utils import timezone
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

    if ages:       
        avg_age = sum(ages) / len(ages)
    else:
        avg_age = 0    
    return avg_age

def get_gender_perc(gender):
    hrs = HumanResource.objects.filter(datadimissioni__isnull=True)
    hrs_count = hrs.count()
    print("Conto: " + str(hrs_count))
    my_gender = 0

    for hr in hrs:
        gender_choice = hr.gender        
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
    
    

# def num_tot_dipendenti(request):
#     # Ottieni l'anno attuale
#     current_date = timezone.now()
#     current_year = current_date.year

#     # Calcola gli ultimi tre anni escluso l'anno attuale
#     years = list(range(current_year - 3, current_year))

#     # Organizza i dati per il grafico
#     labels = []
#     male_data = []
#     female_data = []
    
#     male_female_data = []

#     for year in years:
#         labels.append(str(year))

#         # Conta il numero di dipendenti maschi e femmine per l'anno in ciclo
#         male_count = HumanResource.objects.filter(
#             dataassunzione__year__lte=year
#         ).filter(
#             Q(datadimissioni__year__gt=year) | Q(datadimissioni__isnull=True),
#             gender='M'
#         ).count()
#         female_count = HumanResource.objects.filter(
#             dataassunzione__year__lte=year
#         ).filter(
#             Q(datadimissioni__year__gt=year) | Q(datadimissioni__isnull=True),
#             gender='F'
#         ).count()

#         total_count = male_count + female_count
#         male_data.append(male_count)
#         female_data.append(total_count)
#         male_female_data.append([male_count, female_count])

#     chart_data = {
#         'labels': labels,
#         'male_female_data': male_female_data,
        
#     }
#     print("Chart_data:" + str(chart_data))
#     return JsonResponse(chart_data)

def num_tot_dipendenti(request):
    contratto = request.GET.get('contratto', None)
    print("Contratto inizio: " + str(contratto))
    # Ottieni l'anno attuale
    current_date = datetime.now()
    current_year = current_date.year

    # Calcola gli ultimi tre anni escluso l'anno attuale
    years = list(range(current_year - 3, current_year))

     # Organizza i dati per il grafico
    labels = [str(year) for year in years]
    male_data = []
    female_data = []

    for year in years:
        male_count = HumanResource.objects.filter(
            dataassunzione__year__lte=year
        ).filter(
            Q(datadimissioni__year__gt=year) | Q(datadimissioni__isnull=True),
            gender='M'
        ).count()
        female_count = HumanResource.objects.filter(
            dataassunzione__year__lte=year
        ).filter(
            Q(datadimissioni__year__gt=year) | Q(datadimissioni__isnull=True),
            gender='F'
        ).count()
        if contratto:
            male_count = HumanResource.objects.filter(
                dataassunzione__year__lte=year
            ).filter(
                Q(datadimissioni__year__gt=year) | Q(datadimissioni__isnull=True),
                gender='M', contratto=contratto
            ).count()
            female_count = HumanResource.objects.filter(
                dataassunzione__year__lte=year
            ).filter(
                Q(datadimissioni__year__gt=year) | Q(datadimissioni__isnull=True),
                gender='F', contratto=contratto
            ).count()
    
            
        
        
        
        
        
        male_data.append(male_count)
        female_data.append(female_count)

    # Aggiungi gli anni senza dati nel caso in cui ci siano lacune nei dati
    for year in years:
        if year not in [int(label) for label in labels]:
            labels.append(str(year))
            male_data.append(0)
            female_data.append(0)

    chart_data = {
        'labels': labels,
        'male_data': male_data,
        'female_data': female_data,
    }
    print("Chart_data:" + str(chart_data))
    print("Contratto_finale:" + str(contratto))
    return JsonResponse(chart_data)





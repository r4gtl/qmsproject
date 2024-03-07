import datetime

from django.shortcuts import render

from .charts import num_tot_dipendenti
from .models import *


def stampa_risorse_umane(request):
    
    context = {
    }
    
    return render(request, "human_resources/reports/stampa_risorse_umane.html", context)



def performance_triennio(request):
    fields = {
        'maternità': {
            'nome': 'maternità',
            'alias': 'Maternità',
            'icon_class': 'bi bi-balloon'  # Replace this with the correct icon class
        },
        'malattia': {
            'nome': 'malattia',
            'alias': 'Malattia',
            'icon_class': 'bi bi-prescription2'  # Replace this with the correct icon class
        },
        'infortunio': {
            'nome': 'infortunio',
            'alias': 'Infortunio',
            'icon_class': 'bi bi-bandaid'  # Replace this with the correct icon class
        },
        # Add other fields with their respective alias and icon
    }

    data_per_field = {}
    for field, field_data in fields.items():
        alias = field_data['alias']
        data_per_field[field] = RegistroOreLavoro.sum_field_per_year_last_triennium(field)
    print("data_per_field: " + str(data_per_field))
    
    context = {
        'num_tot_dipendenti': num_tot_dipendenti, 
        'data_per_field': data_per_field,
        'fields': fields,
    }

    return render(request, 'human_resources/reports/performance_triennio.html', context)


def scadenze_formazione(request):
    today = datetime.date.today()
    year_today = datetime.date.today().year
    elenco_formazione = DettaglioRegistroFormazione.objects.filter(prossima_scadenza__gte=today,
        fk_hr__datadimissioni__isnull=True).order_by('-prossima_scadenza')


    context = {
        'elenco_formazione': elenco_formazione,
        'year_today': year_today
    }

    return render(request, 'human_resources/reports/scadenze_formazione.html', context)

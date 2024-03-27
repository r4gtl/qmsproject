from datetime import datetime

from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count, Sum, functions
from django_countries.fields import CountryField
from monitoraggi.models import DatoProduzione, MonitoraggioEnergiaElettrica



def produzione_intervallo_date(request):
    # Ottieni le variabili from_date e to_date dalla richiesta, se presenti
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    # Calcola le date di inizio e fine per la ricerca dei dati
    if from_date and to_date:
        from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
        to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
    else:
        today = datetime.now().date()
        from_date = today - timedelta(days=365)
        to_date = today

    # Filtra i dati in base alle date fornite
    data = DatoProduzione.objects.filter(
        data_inserimento__gte=from_date,
        data_inserimento__lte=to_date
    ).values('industries_served').annotate(total_quantity=Sum('n_pelli'))

    data_json = list(data)

    return JsonResponse(data_json, safe=False)


def report_dati_produzione(request):
    if request.method == 'GET':
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        
        
        from_date_formatted = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
        to_date_formatted = datetime.datetime.strptime(to_date, '%Y-%m-%d').date()

        produzione_filtrata = filtro_dati_produzione(from_date, to_date)
        context = {
                'produzione_filtrata': produzione_filtrata,
                'from_date_formatted': from_date_formatted,
                'to_date_formatted': to_date_formatted,
                'from_date': from_date,
                'to_date': to_date
                
            }

        return render(request, 'monitoraggi/reports/report_produzione.html', context)
    else:
        # Gestisci eventuali altri metodi HTTP
        pass
    

def filtro_dati_produzione(data_inizio, data_fine):    
    dati_produzione_filtrati = DatoProduzione.objects.filter(
            data_inserimento__gte=data_inizio,
            data_inserimento__lte=data_fine
        ).values('industries_served').annotate(total_quantity=Sum('n_pelli'))
   

    return dati_produzione_filtrati


def fetch_chart_data(from_date, to_date):
    # Esegui la logica per recuperare i dati necessari utilizzando from_date e to_date
    # Questa logica potrebbe essere simile a quella nella tua funzione produzione_intervallo_date
    # Ad esempio:
    data = DatoProduzione.objects.filter(
        data_inserimento__gte=from_date,
        data_inserimento__lte=to_date
    ).values('data_inserimento').annotate(
        total_quantity=Sum('n_pelli'),
        total_mq=Sum('mq'),  
        total_kg=Sum('kg')
    )
    
    # Formatta i dati come richiesto dal tuo grafico
    chart_data = {
        'labels': [entry['data_inserimento'] for entry in data],
        'datasets': [
            {
                'label': 'Total Quantity',
                'data': [entry['total_quantity'] for entry in data],
            },
            {
                'label': 'Total MQ',
                'data': [entry['total_mq'] for entry in data],
            },
            {
                'label': 'Total KG',
                'data': [entry['total_kg'] for entry in data],
            }
        ]
    }

    return chart_data
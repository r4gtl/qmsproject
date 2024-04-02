from datetime import datetime, timedelta

from django.shortcuts import render
from django.utils.dateparse import parse_date
from django.http import JsonResponse
from django.db.models import Count, Sum, functions
from django_countries.fields import CountryField
from monitoraggi.models import DatoProduzione, MonitoraggioEnergiaElettrica
from monitoraggi.utils import filtro_dati_produzione, somma_dato_per_intervallo_per_mese



def produzione(request, from_date=None, to_date=None):
    if request.method == 'GET':
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        if from_date and to_date:
            # Converti le date nel formato "YYYY-MM-DD" utilizzato nel modello
            from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
            to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
        else:
            today = datetime.now().date()
            from_date = today - timedelta(days=365)
            to_date = today
        #print(f"from_date: {from_date}, to_date: {to_date}")    
        data = DatoProduzione.objects.filter(
            data_inserimento__gte=from_date,
            data_inserimento__lte=to_date
        ).values('data_inserimento', 'industries_served').annotate(
            total_quantity=Sum('n_pelli'),
            total_mq=Sum('mq'),  
            total_kg=Sum('kg')
        ).order_by('-data_inserimento')  # Ordina per data_inserimento in modo decrescente
        
        data_json = list(data)
        
        return JsonResponse(data_json, safe=False)
    else:
        pass




def energia(request, from_date=None, to_date=None):
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    
    # Effettua il parsing delle date
    #from_date = parse_date(from_date)
    #to_date = parse_date(to_date)
    if from_date and to_date:
        # Converti le date nel formato "YYYY-MM-DD" utilizzato nel modello
        from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
        to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
    else:
        today = datetime.now().date()
        from_date = today - timedelta(days=365)
        to_date = today
    print(f"from_date_energia: {from_date}")    
    print(f"to_date_energia: {to_date}")    
    
    produzione_per_mese = somma_dato_per_intervallo_per_mese(DatoProduzione, 'mq', 'data_inserimento', from_date, to_date)
    
    somma_energia_per_mese = somma_dato_per_intervallo_per_mese(MonitoraggioEnergiaElettrica, 'kwh_in', 'data_lettura', from_date, to_date)

    print(f"produzione_per_mese: {produzione_per_mese}")
    print(f"somma_energia_per_mese: {somma_energia_per_mese}")

    rapporto_per_mese_energia = []
    for prod_mese, energia_mese in zip(produzione_per_mese, somma_energia_per_mese):
        mese = prod_mese['mese']
        produzione = prod_mese['somma']
        somma_energia = energia_mese['somma']
        
        if from_date and to_date and from_date <= mese <= to_date:
            if somma_energia != 0:
                rapporto = (float(produzione) / float(somma_energia)) * 3.6
            else:
                rapporto = 0
            rapporto_per_mese_energia.append({'mese': mese, 'rapporto': rapporto})


    rapporto_energia= rapporto_per_mese_energia
    # Crea un dizionario con i dati JSON
    dati_json = list(rapporto_energia)
    print(f"dati_json_energia: {dati_json}")
    

    return JsonResponse(dati_json, safe=False)
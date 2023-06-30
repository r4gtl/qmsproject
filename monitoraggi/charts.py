from django.http import JsonResponse
from django.utils.dateparse import parse_date
from django.shortcuts import render
import json
from django.db.models import Sum, Count
from datetime import datetime, timedelta
from django_countries.fields import Country

from .models import (DatoProduzione, 
                    MonitoraggioGas, MonitoraggioEnergiaElettrica

                    )

from .utils import filtro_dati_produzione, somma_dato_per_intervallo_per_mese

def produzione_ultimo_anno(request):
    today = datetime.now().date()
    twelve_months_ago = today - timedelta(days=365)

    data = DatoProduzione.objects.filter(
        data_inserimento__gte=twelve_months_ago, 
        data_inserimento__lte=today
    ).values('industries_served').annotate(total_quantity=Sum('n_pelli'))

    data_json = list(data)

    return JsonResponse(data_json, safe=False)



def consumi_mj_mq_ultimo_anno(request):
    produzione_per_mese = DatoProduzione.somma_produzione_ultimo_anno_per_mese()
    
    somma_gas_per_mese = MonitoraggioGas.somma_gas_ultimo_anno_per_mese()
    
    somma_energia_per_mese = MonitoraggioEnergiaElettrica.somma_energia_ultimo_anno_per_mese()

    rapporto_per_mese_gas = []
    for prod_mese, gas_mese in zip(produzione_per_mese, somma_gas_per_mese):
        mese = prod_mese['mese']
        produzione = prod_mese['somma']        
        somma_gas = gas_mese['somma']
        
        if somma_gas != 0:
            rapporto = (float(produzione) / float(somma_gas))*38.4
            
        else:
            rapporto = 0

        rapporto_per_mese_gas.append({'mese': mese, 'rapporto': rapporto})

    rapporto_per_mese_energia = []
    for prod_mese, energia_mese in zip(produzione_per_mese, somma_energia_per_mese):
        mese = prod_mese['mese']
        produzione = prod_mese['somma']
        somma_energia = energia_mese['somma']
        
        if somma_energia != 0:
            rapporto = (float(produzione) / float(somma_energia))*3.6
            
        else:
            rapporto = 0

        rapporto_per_mese_energia.append({'mese': mese, 'rapporto': rapporto})

    # Crea un dizionario con i dati JSON
    dati_json = {
        'rapporto_gas': rapporto_per_mese_gas,
        'rapporto_energia': rapporto_per_mese_energia
    }
    
    return JsonResponse(dati_json)


def produzione_intervallo_date(request):
    if request.method == 'GET':
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')

        data = DatoProduzione.objects.filter(
            data_inserimento__gte=from_date,
            data_inserimento__lte=to_date
        ).values('industries_served').annotate(total_quantity=Sum('n_pelli'))
        
        data_json = list(data)
        
        return JsonResponse(data_json, safe=False)
    else:
        
        pass
    
def energia_intervallo_date(request):
    if request.method == 'GET':
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')

        data = MonitoraggioEnergiaElettrica.somma_energia_per_intervallo(from_date, to_date)
        
        data_json = list(data)
        
        return JsonResponse(data_json, safe=False)
    else:
        
        pass




def consumi_mj_mq_intervallo_date(request):
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    
    # Effettua il parsing delle date
    from_date = parse_date(from_date)
    to_date = parse_date(to_date)

    produzione_per_mese = somma_dato_per_intervallo_per_mese(DatoProduzione, 'mq', 'data_inserimento', from_date, to_date)
    #somma_gas_per_mese = MonitoraggioGas.somma_gas_ultimo_anno_per_mese()
    somma_energia_per_mese = somma_dato_per_intervallo_per_mese(MonitoraggioEnergiaElettrica, 'kwh_in', 'data_lettura', from_date, to_date)

    #rapporto_per_mese_gas = []
    #for prod_mese, gas_mese in zip(produzione_per_mese, somma_gas_per_mese):
    #    mese = prod_mese['mese']
    #    produzione = prod_mese['somma']
    #    somma_gas = gas_mese['somma']
        
    #    if from_date and to_date and from_date <= mese <= to_date:
    #        if somma_gas != 0:
    #            rapporto = (float(produzione) / float(somma_gas)) * 38.4
    #        else:
    #            rapporto = 0
    #        rapporto_per_mese_gas.append({'mese': mese, 'rapporto': rapporto})

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

    # Crea un dizionario con i dati JSON
    dati_json = {
        #'rapporto_gas': rapporto_per_mese_gas,
        'rapporto_energia': rapporto_per_mese_energia
    }

    return JsonResponse(dati_json)

def consumi_mj_mq_intervallo_date_energia(request):
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    
    # Effettua il parsing delle date
    from_date = parse_date(from_date)
    to_date = parse_date(to_date)
    
    produzione_per_mese = somma_dato_per_intervallo_per_mese(DatoProduzione, 'mq', 'data_inserimento', from_date, to_date)
    
    somma_energia_per_mese = somma_dato_per_intervallo_per_mese(MonitoraggioEnergiaElettrica, 'kwh_in', 'data_lettura', from_date, to_date)

    

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
        
    

    return JsonResponse(dati_json, safe=False)


def consumi_mj_mq_intervallo_date_gas(request):
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    
    # Effettua il parsing delle date
    from_date = parse_date(from_date)
    to_date = parse_date(to_date)
    
    produzione_per_mese = somma_dato_per_intervallo_per_mese(DatoProduzione, 'mq', 'data_inserimento', from_date, to_date)
    
    somma_gas_per_mese = somma_dato_per_intervallo_per_mese(MonitoraggioGas, 'mc_in', 'data_lettura', from_date, to_date)

    

    rapporto_per_mese_gas = []
    for prod_mese, gas_mese in zip(produzione_per_mese, somma_gas_per_mese):
        mese = prod_mese['mese']
        produzione = prod_mese['somma']
        somma_gas = gas_mese['somma']
        
        if from_date and to_date and from_date <= mese <= to_date:
            if somma_gas != 0:
                rapporto = (float(produzione) / float(somma_gas)) * 38.4
            else:
                rapporto = 0
            rapporto_per_mese_gas.append({'mese': mese, 'rapporto': rapporto})


    rapporto_gas= rapporto_per_mese_gas
    # Crea un dizionario con i dati JSON
    dati_json = list(rapporto_gas)
        
    

    return JsonResponse(dati_json, safe=False)

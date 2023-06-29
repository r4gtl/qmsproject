from datetime import datetime
from django.http import JsonResponse
from django.db.models import Count, Sum
from django_countries.fields import CountryField
from .models import DatoProduzione, MonitoraggioEnergiaElettrica


def filtro_dati_produzione(data_inizio, data_fine):    
    dati_produzione_filtrati = DatoProduzione.objects.filter(
            data_inserimento__gte=data_inizio,
            data_inserimento__lte=data_fine
        ).values('industries_served').annotate(total_quantity=Sum('n_pelli'))
   

    return dati_produzione_filtrati

# Funzione astratta per avere semplicemente la somma di un campo di un modello in un intervallo di date
def somma_quantity_intervallo_date(modello, campo_sommabile, campo_data, data_inizio, data_fine):       

        # Esegue la query per ottenere la somma del campo da sommare
        somma = modello.objects.filter(**{campo_data + '__range': (data_inizio, data_fine)}).aggregate(total=Sum(campo_sommabile))['total']

        # Verifica se la somma è None (nessun record trovato)
        if somma is None:
            somma = 0

        return somma




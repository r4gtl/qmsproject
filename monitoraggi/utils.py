from datetime import datetime
from django.http import JsonResponse
from django.db.models import Count, Sum
from django_countries.fields import CountryField
from .models import DatoProduzione


def filtro_dati_produzione(data_inizio, data_fine):    
    dati_produzione_filtrati = DatoProduzione.objects.filter(
            data_inserimento__gte=data_inizio,
            data_inserimento__lte=data_fine
        ).values('industries_served').annotate(total_quantity=Sum('n_pelli'))
   

    return dati_produzione_filtrati

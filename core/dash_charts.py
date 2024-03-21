from datetime import datetime
from django.http import JsonResponse
from django.db.models import Count, Sum, functions
from django_countries.fields import CountryField
from monitoraggi.models import DatoProduzione, MonitoraggioEnergiaElettrica




def produzione_intervallo_date(request):
    if request.method == 'GET':
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')

        data = DatoProduzione.objects.filter(
            data_inserimento__gte=from_date,
            data_inserimento__lte=to_date
        ).values('industries_served').annotate(
            total_quantity=Sum('n_pelli'),
            total_mq=Sum('mq'),  
            total_kg=Sum('kg') )
        
        data_json = list(data)
        
        return JsonResponse(data_json, safe=False)
    else:
        
        pass
    
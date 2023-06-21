from django.http import JsonResponse
from django.db.models import Sum, Count
import datetime

from .models import (Lotto, 
                    

                    )




# Charts
def origine_old(request):
    labels = []
    data = []
    # Calcola la data di 12 mesi fa dalla data corrente
    twelve_months_ago = datetime.datetime.now() - datetime.timedelta(days=365)
    #queryset = Lotto.objects.values('origine').annotate(lotti_count=Count('pk'))
    queryset = Lotto.objects.filter(data_acquisto__gte=twelve_months_ago).values('origine').annotate(lotti_count=Count('pk'))
    result = {
    q['origine']: q['lotti_count']
    for q in queryset
    }
    

    for entry in queryset:
        labels.append(entry['origine'])
        data.append(entry['lotti_count'])
        
    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

def origine(request):
    labels = []
    data = []
    
    # Calcola la data di 12 mesi fa dalla data corrente
    twelve_months_ago = datetime.datetime.now() - datetime.timedelta(days=365)
    
    # Filtra i lotti con data_acquisto successiva alla data di 12 mesi fa
    queryset = Lotto.objects.filter(data_acquisto__gte=twelve_months_ago).values('origine').annotate(lotti_count=Count('pk'))
    
    result = {
        q['origine']: q['lotti_count']
        for q in queryset
    }
    

    for entry in queryset:
        labels.append(entry['origine'])
        data.append(entry['lotti_count'])
        
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })
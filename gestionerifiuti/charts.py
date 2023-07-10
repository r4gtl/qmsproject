from django.http import JsonResponse
from django.db.models import Sum, Count
import datetime

from .models import (MovimentoRifiuti, CodiceSmaltRec, CodiceCER 
                    

                    )




# Charts
def cer_last_year(request):
    labels = []
    data = []
    # Calcola la data di 12 mesi fa dalla data corrente
    twelve_months_ago = datetime.datetime.now() - datetime.timedelta(days=365)
    #queryset = Lotto.objects.values('origine').annotate(lotti_count=Count('pk'))
    queryset = MovimentoRifiuti.objects.filter(data_movimento__gte=twelve_months_ago).filter(car_scar="carico").values('fk_codicecer__codice').annotate(rifiuti_prodotti=Sum('quantity'))
    result = {
    q['fk_codicecer__codice']: q['rifiuti_prodotti']
    for q in queryset
    }
    

    for entry in queryset:
        labels.append(entry['fk_codicecer__codice'])
        data.append(entry['rifiuti_prodotti'])
        
    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })
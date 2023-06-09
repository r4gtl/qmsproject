from django.http import JsonResponse
from django.db.models import Sum, Count
from datetime import datetime

from .models import (Lotto, 
                    

                    )




# Charts
def origine(request):
    labels = []
    data = []

    queryset = Lotto.objects.values('origine').annotate(lotti_count=Count('pk'))
    result = {
    q['origine']: q['lotti_count']
    for q in queryset
    }
    print("Result: " + str(result))

    for entry in queryset:
        labels.append(entry['origine'])
        data.append(entry['lotti_count'])
        
    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

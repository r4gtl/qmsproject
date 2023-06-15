from django.http import JsonResponse
import json
from django.db.models import Sum, Count
from datetime import datetime, timedelta
from django_countries.fields import Country

from .models import (DatoProduzione, 
                    

                    )

def produzione_ultimo_anno(request):
    today = datetime.now().date()
    twelve_months_ago = today - timedelta(days=365)

    data = DatoProduzione.objects.filter(
        data_inserimento__gte=twelve_months_ago, 
        data_inserimento__lte=today
    ).values('industries_served').annotate(total_quantity=Sum('n_pelli'))

    data_json = list(data)

    return JsonResponse(data_json, safe=False)
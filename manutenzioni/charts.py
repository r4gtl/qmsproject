from django.http import JsonResponse
from django.db.models import Sum, Count
from datetime import datetime, date, timedelta
from django.http import JsonResponse
import calendar

from .models import ManutenzioneStraordinaria, Attrezzatura



def get_monthly_data(request):
    today = date.today()
    last_month = today - timedelta(days=30)

    monthly_sums = {}
    for i in range(12):
        start_date = last_month.replace(day=1)
        end_date = last_month.replace(day=calendar.monthrange(last_month.year, last_month.month)[1])
        monthly_sum = ManutenzioneStraordinaria.objects.filter(data_manutenzione__range=(start_date, end_date)).aggregate(total_importo=Sum('importo'))['total_importo']
        monthly_sums[last_month.strftime('%b')] = monthly_sum
        last_month -= timedelta(days=last_month.day)

    months = list(monthly_sums.keys())
    months.reverse()  # Inverti l'ordine dell'elenco dei mesi
    sums = list(monthly_sums.values())
    sums.reverse()  # Inverti l'ordine dell'elenco delle somme
    data = {
        'months': months,
        'sums': sums,
    }

    return JsonResponse(data)

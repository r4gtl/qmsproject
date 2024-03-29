from django.shortcuts import render
from datetime import datetime, timedelta
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count, Sum, functions
from .utils import count_records_with_upcoming_expiry
from django.http import JsonResponse
from manutenzioni.models import Taratura, ManutenzioneOrdinaria
from monitoraggi.models import *
from autorizzazioni.models import DettaglioScadenzaAutorizzazione
from human_resources.models import DettaglioRegistroFormazione

# Create your views here.

def home(request):
    scadenze_manutenzioni = count_records_with_upcoming_expiry(Taratura, "prossima_scadenza", 30) + count_records_with_upcoming_expiry(ManutenzioneOrdinaria, "prossima_scadenza", 30)
    scadenze_formazione = count_records_with_upcoming_expiry(DettaglioRegistroFormazione, "prossima_scadenza", 30)
    
    context = { 
        'scadenze_manutenzioni': scadenze_manutenzioni,
        'scadenze_formazione': scadenze_formazione
        
    }
    return render(request, 'core/home.html', context)

def dashboard(request):
    
        
        return render(request, 'core/dashboard.html')


def produzione_old(request,from_date=None, to_date=None):
    if request.method == 'GET':
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        if from_date and to_date:
            from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
            to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
        else:
            today = datetime.now().date()
            from_date = today - timedelta(days=365)
            to_date = today
        
        data = DatoProduzione.objects.filter(
            data_inserimento__gte=from_date,
            data_inserimento__lte=to_date
        ).values('data_inserimento', 'industries_served').annotate(
            total_quantity=Sum('n_pelli'),
            total_mq=Sum('mq'),  
            total_kg=Sum('kg')
        ).order_by('-data_inserimento')
        
        
        
        data_json = list(data)
        
        return JsonResponse(data_json, safe=False)
    else:
        
        pass

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

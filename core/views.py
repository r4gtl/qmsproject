from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from .utils import count_records_with_upcoming_expiry
from manutenzioni.models import Taratura, ManutenzioneOrdinaria
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



from django.shortcuts import render
from datetime import date
from datetime import timedelta
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from manualeprocedure.models import Procedura
from manualeprocedure.filters import ProceduraFilter
from core.utils import count_records_with_upcoming_expiry
from autorizzazioni.models import DettaglioScadenzaAutorizzazione
from manutenzioni.models import Taratura, ManutenzioneOrdinaria

from .utils import get_scadenzario_completo

# Create your views here.

def lwg_home(request):
    # 04/09/2023 - disattivato perchè utilizzo la funzione get_scadenzario_completo
    #scadenze_autorizzazioni =count_records_with_upcoming_expiry(DettaglioScadenzaAutorizzazione, "scadenza_rinnovo", 30)
    #scadenze_manutenzioni = count_records_with_upcoming_expiry(Taratura, "prossima_scadenza", 30) + count_records_with_upcoming_expiry(ManutenzioneOrdinaria, "prossima_scadenza", 30)
    
    # Ricavo tutte le scadenze per visualizzarle nei toast
    scadenzario=get_scadenzario_completo()    
    today = date.today()
    thirty_days_from_today = today + timedelta(days=30)
    
    scadenzario = [scadenza for scadenza in scadenzario if scadenza['scadenza'] <= thirty_days_from_today]
    context = {
        #'scadenze_autorizzazioni': scadenze_autorizzazioni,
        #'scadenze_manutenzioni': scadenze_manutenzioni,
        'scadenzario':scadenzario
    }
    return render(request, 'lwg/lwg_home.html', context)


def lwg_procedure(request, fk_lwgsection):
    procedure = Procedura.objects.all()
    
    
    
    procedura_filter = ProceduraFilter(request.GET, 
                                    queryset=Procedura.objects.filter(fk_lwgsection=fk_lwgsection),
                                    fk_lwgsection=fk_lwgsection
                                    )
    
    
    page = request.GET.get('page', 1)
    paginator = Paginator(procedure, 50)
    
    try:
        procedure_home = paginator.page(page)
    except PageNotAnInteger:
        procedure_home = paginator.page(1)
    except EmptyPage:
        procedure_home = paginator.page(paginator.num_pages)
    context={
        'procedure_home': procedure_home,
        'filter': procedura_filter,
        
    }
    return render(request, "manualeprocedure/procedure_home.html", context)



'''
def scadenzario_completo(request):
    today = date.today()
    scadenzario = []
    scadenze_autorizzazioni = DettaglioScadenzaAutorizzazione.objects.filter(scadenza_rinnovo__gte=today).filter(is_rinnovata=False)
    for scadenza in scadenze_autorizzazioni:
        scadenzario.append({
            'scadenza': scadenza.scadenza_rinnovo,
            'descrizione': scadenza.fk_autorizzazione.descrizione,
            'nomemodello': 'autorizzazioni',
        })

    scadenze_manutenzioni = ManutenzioneOrdinaria.objects.filter(prossima_scadenza__gte=today)
    for scadenza in scadenze_manutenzioni:
        scadenzario.append({
            'scadenza': scadenza.prossima_scadenza,
            'descrizione': scadenza.descrizione,
            'nomemodello': 'manutenzioni',
        })
    scadenzario = sorted(scadenzario, key=lambda s: s['scadenza'])  # Ordina per data di scadenza
    context = {
        'scadenzario': scadenzario
    }

    return render(request, "lwg/scadenzario.html", context)

    '''

def scadenzario_completo(request):
    
    scadenzario = get_scadenzario_completo()
    
    context = {
        'scadenzario': scadenzario
    }
    
   


    return render(request, "lwg/scadenzario.html", context)

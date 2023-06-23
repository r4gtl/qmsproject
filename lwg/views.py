from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from manualeprocedure.models import Procedura
from manualeprocedure.filters import ProceduraFilter
from core.utils import count_records_with_upcoming_expiry
from autorizzazioni.models import DettaglioScadenzaAutorizzazione

# Create your views here.

def lwg_home(request):
    scadenze_autorizzazioni =count_records_with_upcoming_expiry(DettaglioScadenzaAutorizzazione, "scadenza_rinnovo", 30)
    context = {
        'scadenze_autorizzazioni': scadenze_autorizzazioni
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
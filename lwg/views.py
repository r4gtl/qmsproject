from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from manualeprocedure.models import Procedura
from manualeprocedure.filters import ProceduraFilter

# Create your views here.

def lwg_home(request):
    
    context = {
        
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
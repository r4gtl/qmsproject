from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *


# Create your views here.
 
def dashboard_emissions(request):
    
    camini = PuntoEmissione.objects.all()
    tot_camini = PuntoEmissione.objects.count()
    camini_filter = SostanzaFilter(request.GET, queryset=sostanze)
    filtered_camini = camini_filter.qs  # Ottieni i record filtrati
    camini_filter_count = filtered_camini.count()  # Conta i record filtrati

    # Paginazione Camini
    page_camini = request.GET.get('page', 1)
    paginator_camini = Paginator(filtered_camini, 50)
    try:
        camini_paginator = paginator_camini.page(page_camini)
    except PageNotAnInteger:
        camini_paginator = paginator_camini.page(1)
    except EmptyPage:
        camini_paginator = paginator_camini.page(paginator_camini.num_pages)
    context = {
        # Sostanze
        'camini': camini,
        'camini_paginator': camini_paginator,
        'tot_camini': tot_camini,
        'filtered_camini': filtered_camini,
        'camini_filter_count': camini_filter_count,
        
        

    }

    return render(request, 'chem_man/generiche/tabelle_generiche.html', context)
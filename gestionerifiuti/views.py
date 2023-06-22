from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages


from .models import (CodiceCER, 
                     CodiceSmaltRec, 
                     MovimentoRifiuti,
                     
                     )
from .filters import MovimentoRifiutiFilter

from .forms import (MovimentoRifiutiModelForm
                    
                    )



def gestione_rifiuti_home(request): 

    movimenti_rifiuti = MovimentoRifiuti.objects.all()
    
    movimenti_rifiuti_filter = MovimentoRifiutiFilter(request.GET, queryset=movimenti_rifiuti)
    
    page = request.GET.get('page', 1)
    paginator = Paginator(movimenti_rifiuti_filter.qs, 50)  # Utilizza lotti_filter.qs per la paginazione
    
        
    try:
        movimenti_rifiuti_paginator = paginator.page(page)
    except PageNotAnInteger:
        movimenti_rifiuti_paginator = paginator.page(1)
    except EmptyPage:
        movimenti_rifiuti_paginator = paginator.page(paginator.num_pages)
        
    context = {
        'dati_paginator': movimenti_rifiuti_paginator,
        'filter': movimenti_rifiuti_filter,
    }
    
    return render(request, 'gestionerifiuti/gestione_rifiuti_home.html', context)

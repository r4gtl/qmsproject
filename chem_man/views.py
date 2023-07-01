from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django_filters.views import FilterView


from .filters import ProdottoChimicoFilter

from .models import ProdottoChimico



from .forms import (FormProdottoChimico
)

# Create your views here.

def home_prodotti_chimici(request): 
    prodotti_chimici = ProdottoChimico.objects.all()
    prodotti_chimici_filter = ProdottoChimicoFilter(request.GET, queryset=prodotti_chimici)
    #filterset_class = FornitoreFilter
    page = request.GET.get('page', 1)
    paginator = Paginator(prodotti_chimici_filter.qs, 50)  # Utilizza fornitori_filter.qs per la paginazione
            
    try:
        prodotti_chimici_paginator = paginator.page(page)
    except PageNotAnInteger:
        prodotti_chimici_paginator = paginator.page(1)
    except EmptyPage:
        prodotti_chimici_paginator = paginator.page(paginator.num_pages)
        
    context = {
        #'fornitori': filterset_class,
        'prodotti_chimici_paginator': prodotti_chimici_paginator,
        'filter': prodotti_chimici_filter
    }
    return render(request, 'chem_man/home_prodotti_chimici.html', context)

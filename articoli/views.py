from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.urls import reverse, reverse_lazy
from django.db.models import Sum, Count
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import (Articolo, Colore
                    )

from .filters import ArticoloFilter, ColoreFilter



def articoli_home(request):
    articoli = Articolo.objects.all()
    articolo_filter = ArticoloFilter
    page = request.GET.get('page', 1)
    paginator = Paginator(articoli, 50)
    
    try:
        articoli_home = paginator.page(page)
    except PageNotAnInteger:
        articoli_home = paginator.page(1)
    except EmptyPage:
        articoli_home = paginator.page(paginator.num_pages)
    context={
        'articoli_home': articoli_home,
        'filter': articolo_filter,
        
    }
    return render(request, "articoli/articoli_home.html", context)

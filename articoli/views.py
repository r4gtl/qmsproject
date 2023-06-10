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
from .forms import ArticoloModelForm
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



class ArticoloCreateView(LoginRequiredMixin,CreateView):
    model = Articolo
    form_class = ArticoloModelForm
    template_name = 'articoli/articolo.html'
    success_message = 'Articolo aggiunto correttamente!'
    #success_url = reverse_lazy('human_resources:human_resources')

    def get_success_url(self):        
        if 'salva_esci' in self.request.POST:
            return reverse_lazy('articoli:articoli_home')
        
        pk_articolo=self.object.pk
        return reverse_lazy('articoli:modifica_articolo', kwargs={'pk':pk_articolo})
    
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    

class ArticoloUpdateView(LoginRequiredMixin,UpdateView):
    model = Articolo
    form_class = ArticoloModelForm
    template_name = 'articoli/articolo.html'
    success_message = 'Articolo modificato correttamente!'
    #success_url = reverse_lazy('human_resources:human_resources')

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_success_url(self):        
        if 'salva_esci' in self.request.POST:
            return reverse_lazy('articoli:articoli_home')
        
        pk_articolo=self.object.pk
        return reverse_lazy('articoli:modifica_articolo', kwargs={'pk':pk_articolo})
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        # context['elenco_formazione'] = DettaglioRegistroFormazione.objects.filter(fk_hr=self.object.pk)
        # context['elenco_valutazioni'] = ValutazioneOperatore.objects.filter(fk_hr=self.object.pk)
        return context
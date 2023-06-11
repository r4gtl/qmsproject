from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.urls import reverse, reverse_lazy
from django.db.models import Sum, Count
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import (Articolo, Colore, FaseLavoro
                    )
from .forms import ArticoloModelForm, ColoreModelForm, FaseLavoroModelForm
from .filters import ArticoloFilter, ColoreFilter, FaseLavoroFilter



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
    
def delete_articolo(request, pk): 
        deleteobject = get_object_or_404(Articolo, pk = pk)        
        deleteobject.delete()
        url_match= reverse_lazy('articoli:articoli_home')
        return redirect(url_match)
    


def colori_home(request):
    colori = Colore.objects.all()
    colore_filter = ColoreFilter
    page = request.GET.get('page', 1)
    paginator = Paginator(colori, 50)
    
    try:
        colori_home = paginator.page(page)
    except PageNotAnInteger:
        colori_home = paginator.page(1)
    except EmptyPage:
        colori_home = paginator.page(paginator.num_pages)
    context={
        'colori_home': colori_home,
        'filter': colore_filter,
        
    }
    return render(request, "articoli/colori_home.html", context)


class ColoreCreateView(LoginRequiredMixin,CreateView):
    model = Colore
    form_class = ColoreModelForm
    template_name = 'articoli/colore.html'
    success_message = 'Colore aggiunto correttamente!'
    #success_url = reverse_lazy('human_resources:human_resources')

    def get_success_url(self):        
        if 'salva_esci' in self.request.POST:
            return reverse_lazy('articoli:colori_home')
        
        pk_colore=self.object.pk
        return reverse_lazy('articoli:modifica_colore', kwargs={'pk':pk_colore})
    
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    

class ColoreUpdateView(LoginRequiredMixin,UpdateView):
    model = Colore
    form_class = ColoreModelForm
    template_name = 'articoli/colore.html'
    success_message = 'Colore modificato correttamente!'
    #success_url = reverse_lazy('human_resources:human_resources')

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_success_url(self):        
        if 'salva_esci' in self.request.POST:
            return reverse_lazy('articoli:colori_home')
        
        pk_colore=self.object.pk
        return reverse_lazy('articoli:modifica_colore', kwargs={'pk':pk_colore})
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        # context['elenco_formazione'] = DettaglioRegistroFormazione.objects.filter(fk_hr=self.object.pk)
        # context['elenco_valutazioni'] = ValutazioneOperatore.objects.filter(fk_hr=self.object.pk)
        return context
    
def delete_colore(request, pk): 
        deleteobject = get_object_or_404(Colore, pk = pk)        
        deleteobject.delete()
        url_match= reverse_lazy('articoli:colori_home')
        return redirect(url_match)
    



def fasi_lavoro_home(request):
    fasi_lavoro = FaseLavoro.objects.all()
    fase_lavoro_filter = FaseLavoroFilter
    page = request.GET.get('page', 1)
    paginator = Paginator(fasi_lavoro, 50)
    
    try:
        fasi_lavoro_home = paginator.page(page)
    except PageNotAnInteger:
        fasi_lavoro_home = paginator.page(1)
    except EmptyPage:
        fasi_lavoro_home = paginator.page(paginator.num_pages)
    context={
        'fasi_lavoro_home': fasi_lavoro_home,
        'filter': fase_lavoro_filter,
        
    }
    return render(request, "articoli/fasi_lavoro_home.html", context)


class FaseLavoroCreateView(LoginRequiredMixin,CreateView):
    model = FaseLavoro
    form_class = FaseLavoroModelForm
    template_name = 'articoli/fase_lavoro.html'
    success_message = 'Fase di lavoro aggiunta correttamente!'
    #success_url = reverse_lazy('human_resources:human_resources')

    def get_success_url(self):        
        if 'salva_esci' in self.request.POST:
            return reverse_lazy('articoli:fasi_lavoro_home')
        
        pk_fase=self.object.pk
        return reverse_lazy('articoli:modifica_fase_lavoro', kwargs={'pk':pk_fase})
    
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    

class FaseLavoroUpdateView(LoginRequiredMixin,UpdateView):
    model = FaseLavoro
    form_class = FaseLavoroModelForm
    template_name = 'articoli/fase_lavoro.html'
    success_message = 'Fase di Lavoro modificata correttamente!'
    #success_url = reverse_lazy('human_resources:human_resources')

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_success_url(self):        
        if 'salva_esci' in self.request.POST:
            return reverse_lazy('articoli:fasi_lavoro_home')
        
        pk_fase=self.object.pk
        return reverse_lazy('articoli:modifica_fase_lavoro', kwargs={'pk':pk_fase})
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        # context['elenco_formazione'] = DettaglioRegistroFormazione.objects.filter(fk_hr=self.object.pk)
        # context['elenco_valutazioni'] = ValutazioneOperatore.objects.filter(fk_hr=self.object.pk)
        return context
    
def delete_fase_lavoro(request, pk): 
        deleteobject = get_object_or_404(FaseLavoro, pk = pk)        
        deleteobject.delete()
        url_match= reverse_lazy('articoli:fasi_lavoro_home')
        return redirect(url_match)
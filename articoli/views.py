from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from django.views.generic.edit import CreateView, UpdateView
from .models import (Articolo, Colore, FaseLavoro, ElencoTest, TestArticolo,
                    Procedura, DettaglioProcedura
                    )
from .forms import *
from .filters import *



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
    
    def get_initial(self):
        created_by = self.request.user
        
        return {
            'created_by': created_by,
        }
    
    

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
        context['elenco_test'] = TestArticolo.objects.filter(fk_articolo=self.object.pk)
        context['elenco_revisioni'] = Procedura.objects.filter(fk_articolo=self.object.pk).order_by('-data_procedura')
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
    



def tabelle_generiche(request):

    # Fasi di Lavoro
    fasi_lavoro = FaseLavoro.objects.all()
    tot_fasi = FaseLavoro.objects.count()
    fasi_lavoro_filter = FaseLavoroFilter(request.GET, queryset=fasi_lavoro)
    filtered_fasi_lavoro = fasi_lavoro_filter.qs
    fase_lavoro_filter_count = filtered_fasi_lavoro.count()
    
    # Paginazione Fasi di Lavoro
    page_fasi_lavoro = request.GET.get('page', 1)
    paginator_fasi_lavoro = Paginator(filtered_fasi_lavoro, 50)
    try:
        fasi_lavoro_paginator = paginator_fasi_lavoro.page(page_fasi_lavoro)
    except PageNotAnInteger:
        fasi_lavoro_paginator = paginator_fasi_lavoro.page(1)
    except EmptyPage:
        fasi_lavoro_paginator = paginator_fasi_lavoro.page(paginator_fasi_lavoro.num_pages)


    # Elenco Test
    elenco_test = ElencoTest.objects.all()
    tot_test = ElencoTest.objects.count()
    elenco_test_filter = ElencoTestFilter(request.GET, queryset=elenco_test)
    filtered_elenco_test = elenco_test_filter.qs
    elenco_test_filter_count = filtered_elenco_test.count()
    
    # Paginazione Elenco Test
    page_elenco_test = request.GET.get('page', 1)
    paginator_elenco_test = Paginator(filtered_elenco_test, 50)
    try:
        elenco_test_paginator = paginator_elenco_test.page(page_elenco_test)
    except PageNotAnInteger:
        elenco_test_paginator = paginator_elenco_test.page(1)
    except EmptyPage:
        elenco_test_paginator = paginator_elenco_test.page(paginator_elenco_test.num_pages)



    context={
        
        'filter': fasi_lavoro_filter,
        'tot_fasi': tot_fasi,
        'fase_lavoro_filter_count': fase_lavoro_filter_count,
        'fasi_lavoro_paginator': fasi_lavoro_paginator,
        'elenco_test_filter': elenco_test_filter,
        'tot_test': tot_test,
        'elenco_test_filter_count': elenco_test_filter_count,
        'elenco_test_paginator': elenco_test_paginator,
        
    }
    return render(request, "articoli/tabelle_generiche.html", context)



# def fasi_lavoro_home(request):
#     fasi_lavoro = FaseLavoro.objects.all()
#     fase_lavoro_filter = FaseLavoroFilter
#     page = request.GET.get('page', 1)
#     paginator = Paginator(fasi_lavoro, 50)
    
#     try:
#         fasi_lavoro_home = paginator.page(page)
#     except PageNotAnInteger:
#         fasi_lavoro_home = paginator.page(1)
#     except EmptyPage:
#         fasi_lavoro_home = paginator.page(paginator.num_pages)
#     context={
#         'fasi_lavoro_home': fasi_lavoro_home,
#         'filter': fase_lavoro_filter,
        
#     }
#     return render(request, "articoli/fasi_lavoro_home.html", context)


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
            return reverse_lazy('articoli:tabelle_generiche')
        
        pk_fase=self.object.pk
        return reverse_lazy('articoli:modifica_fase_lavoro', kwargs={'pk':pk_fase})
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        context['elenco_attributi'] = DettaglioFaseLavoro.objects.filter(fk_fase_lavoro=self.object.pk)
        # context['elenco_valutazioni'] = ValutazioneOperatore.objects.filter(fk_hr=self.object.pk)
        return context
    
def delete_fase_lavoro(request, pk): 
        deleteobject = get_object_or_404(FaseLavoro, pk = pk)        
        deleteobject.delete()
        url_match= reverse_lazy('articoli:tabelle_generiche')
        return redirect(url_match)


# Dettaglio Fasi di Lavoro

class DettaglioFaseLavoroCreateView(LoginRequiredMixin,CreateView):
    model = DettaglioFaseLavoro
    form_class = DettaglioFaseLavoroModelForm
    template_name = 'articoli/dettaglio_fase_lavoro.html'
    success_message = 'Attributo aggiunto correttamente!'


    def get_success_url(self):
        fk_fase_lavoro=self.object.fk_fase_lavoro.pk
        return reverse_lazy('articoli:modifica_fase_lavoro', kwargs={'pk':fk_fase_lavoro})



    def form_valid(self, form):
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    def get_initial(self):
        created_by = self.request.user
        fk_fase_lavoro = self.kwargs['fk_fase_lavoro']
        return {
            'created_by': created_by,
            'fk_fase_lavoro': fk_fase_lavoro
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fk_fase_lavoro = self.kwargs['fk_fase_lavoro']
        context['fk_fase_lavoro'] = FaseLavoro.objects.get(pk=fk_fase_lavoro)

        return context


class DettaglioFaseLavoroUpdateView(LoginRequiredMixin, UpdateView):
    model = DettaglioFaseLavoro
    form_class = DettaglioFaseLavoroModelForm
    template_name = 'articoli/dettaglio_fase_lavoro.html'
    success_message = 'Attributo modificato correttamente!'


    def get_success_url(self):
        fk_fase_lavoro=self.object.fk_fase_lavoro.pk
        return reverse_lazy('articoli:modifica_fase_lavoro', kwargs={'pk':fk_fase_lavoro})


    def form_valid(self, form):
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fk_fase_lavoro = self.kwargs['fk_fase_lavoro']
        context['fk_fase_lavoro'] = DettaglioFaseLavoro.objects.get(pk=fk_fase_lavoro)

        return context


def delete_dettaglio_fase_lavoro(request, pk):
        deleteobject = get_object_or_404(DettaglioFaseLavoro, pk = pk)
        fk_fase_lavoro = deleteobject.fk_fase_lavoro.pk
        deleteobject.delete()
        url_match = reverse_lazy('articoli:modifica_fase_lavoro', kwargs={'pk':fk_fase_lavoro})
        return redirect(url_match)



class ElencoTestCreateView(LoginRequiredMixin,CreateView):
    model = ElencoTest
    form_class = ElencoTestModelForm
    template_name = 'articoli/elenco_test.html'
    success_message = 'Test aggiunto correttamente!'
    #success_url = reverse_lazy('human_resources:human_resources')

    def get_success_url(self):        
        #if 'salva_esci' in self.request.POST:
        return reverse_lazy('articoli:tabelle_generiche')
        
        #pk_fase=self.object.pk
        #return reverse_lazy('articoli:modifica_fase_lavoro', kwargs={'pk':pk_fase})
    
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    

class ElencoTestUpdateView(LoginRequiredMixin,UpdateView):
    model = ElencoTest
    form_class = ElencoTestModelForm
    template_name = 'articoli/elenco_test.html'
    success_message = 'Test modificato correttamente!'
    #success_url = reverse_lazy('human_resources:human_resources')

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_success_url(self):        
        #if 'salva_esci' in self.request.POST:
        return reverse_lazy('articoli:tabelle_generiche')
        
        #pk_fase=self.object.pk
        #return reverse_lazy('articoli:modifica_fase_lavoro', kwargs={'pk':pk_fase})
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        # context['elenco_formazione'] = DettaglioRegistroFormazione.objects.filter(fk_hr=self.object.pk)
        # context['elenco_valutazioni'] = ValutazioneOperatore.objects.filter(fk_hr=self.object.pk)
        return context
    
def delete_test(request, pk): 
        deleteobject = get_object_or_404(ElencoTest, pk = pk)        
        deleteobject.delete()
        url_match= reverse_lazy('articoli:tabelle_generiche')
        return redirect(url_match)


# Associa Test agli articoli

class TestArticoloCreateView(LoginRequiredMixin,CreateView):
    model = TestArticolo
    form_class = TestArticoloModelForm
    template_name = 'articoli/test_articolo.html'
    success_message = 'Test aggiunto correttamente!'


    def get_success_url(self):
        fk_articolo=self.object.fk_articolo.pk
        return reverse_lazy('articoli:modifica_articolo', kwargs={'pk':fk_articolo})



    def form_valid(self, form):
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    def get_initial(self):
        created_by = self.request.user
        fk_articolo = self.kwargs['fk_articolo']
        return {
            'created_by': created_by,
            'fk_articolo': fk_articolo
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fk_articolo = self.kwargs['fk_articolo']
        context['fk_articolo'] = Articolo.objects.get(pk=fk_articolo)

        return context


class TestArticoloUpdateView(LoginRequiredMixin, UpdateView):
    model = TestArticolo
    form_class = TestArticoloModelForm
    template_name = 'articoli/test_articolo.html'
    success_message = 'Test modificato correttamente!'


    def get_success_url(self):
        fk_articolo=self.object.fk_articolo.pk
        return reverse_lazy('articoli:modifica_articolo', kwargs={'pk':fk_articolo})


    def form_valid(self, form):
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fk_articolo = self.kwargs['fk_articolo']
        context['fk_articolo'] = Articolo.objects.get(pk=fk_articolo)

        return context


def delete_test_articolo(request, pk):
        deleteobject = get_object_or_404(TestArticolo, pk = pk)
        fk_articolo = deleteobject.fk_articolo.pk
        deleteobject.delete()
        url_match = reverse_lazy('articoli:modifica_articolo', kwargs={'pk':fk_articolo})
        return redirect(url_match)
    
    
# Procedure di Lavorazione


class ProceduraCreateView(LoginRequiredMixin,CreateView):
    model = Procedura
    form_class = ProceduraModelForm
    template_name = 'articoli/procedura.html'
    success_message = 'Procedura aggiunta correttamente!'


    def get_success_url(self):
        if 'salva_esci' in self.request.POST:
            fk_articolo=self.object.fk_articolo.pk
            return reverse_lazy('articoli:modifica_articolo', kwargs={'pk':fk_articolo})

        pk_procedura=self.object.pk
        return reverse_lazy('articoli:modifica_procedura', kwargs={'pk':pk_procedura})

    def form_valid(self, form):
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    def get_initial(self):
        created_by = self.request.user
        fk_articolo = self.kwargs['fk_articolo']
        return {
            'created_by': created_by,
            'fk_articolo': fk_articolo
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fk_articolo = self.kwargs['fk_articolo']
        context['fk_articolo'] = Articolo.objects.get(pk=fk_articolo)

        return context


class ProceduraUpdateView(LoginRequiredMixin, UpdateView):
    model = Procedura
    form_class = ProceduraModelForm
    template_name = 'articoli/procedura.html'
    success_message = 'Procedura modificata correttamente!'


    def get_success_url(self):
        if 'salva_esci' in self.request.POST:
            fk_articolo=self.object.fk_articolo.pk
            return reverse_lazy('articoli:modifica_articolo', kwargs={'pk':fk_articolo})

        pk_procedura=self.object.pk
        return reverse_lazy('articoli:modifica_procedura', kwargs={'pk':pk_procedura})


    def form_valid(self, form):
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fk_articolo = self.kwargs['fk_articolo']
        context['fk_articolo'] = Articolo.objects.get(pk=fk_articolo)

        return context


def delete_procedura(request, pk):
        deleteobject = get_object_or_404(Procedura, pk = pk)
        fk_articolo = deleteobject.fk_articolo.pk
        deleteobject.delete()
        url_match = reverse_lazy('articoli:modifica_articolo', kwargs={'pk':fk_articolo})
        return redirect(url_match)

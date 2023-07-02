from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django_filters.views import FilterView


from .filters import ProdottoChimicoFilter

from .models import ProdottoChimico, PrezzoProdotto, SchedaTecnica



from .forms import (ProdottoChimicoModelForm, PrezzoProdottoModelForm,
                    SchedaTecnicaModelForm,
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




# Prodotto Chimico

class ProdottoChimicoCreateView(LoginRequiredMixin,CreateView):
    model = ProdottoChimico
    form_class = ProdottoChimicoModelForm
    template_name = 'chem_man/prodotto_chimico.html'
    success_message = 'Prodotto chimico aggiunto correttamente!'
    

    def get_success_url(self):        
        if 'salva_esci' in self.request.POST:
            return reverse_lazy('chem_man:home_prodotti_chimici')
        
        pk_prodotto_chimico=self.object.pk
        return reverse_lazy('chem_man:modifica_prodotto_chimico', kwargs={'pk':pk_prodotto_chimico})
        

    
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_initial(self):
        created_by = self.request.user
        return {
            'created_by': created_by,
        }

class ProdottoChimicoUpdateView(LoginRequiredMixin, UpdateView):
    model = ProdottoChimico
    form_class = ProdottoChimicoModelForm
    template_name = 'chem_man/prodotto_chimico.html'
    success_message = 'Prodotto chimico modificato correttamente!'
    
    
    def get_success_url(self):        
        if 'salva_esci' in self.request.POST:
            return reverse_lazy('chem_man:home_prodotti_chimici')
        
        pk_prodotto_chimico=self.object.pk
        return reverse_lazy('chem_man:modifica_prodotto_chimico', kwargs={'pk':pk_prodotto_chimico})
            

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        pk_prodottochimico = self.object.pk        
        context['elenco_prezzi'] = PrezzoProdotto.objects.filter(fk_prodottochimico=pk_prodottochimico) 
        context['elenco_schede_tecniche'] = SchedaTecnica.objects.filter(fk_prodottochimico=pk_prodottochimico) 

        return context


def delete_prodotto_chimico(request, pk): 
        deleteobject = get_object_or_404(ProdottoChimico, pk = pk)                 
        deleteobject.delete()
        url_match = reverse_lazy('chem_man:home_prodotti_chimici')
        return redirect(url_match)



# Prezzo Prodotto Chimico

class PrezzoProdottoCreateView(LoginRequiredMixin,CreateView):
    model = PrezzoProdotto
    form_class = PrezzoProdottoModelForm
    template_name = 'chem_man/prezzo_prodotto_chimico.html'
    success_message = 'Prezzo aggiunto correttamente!'
    

    def get_success_url(self):                               
        fk_prodottochimico=self.object.fk_prodottochimico.pk
        return reverse_lazy('chem_man:modifica_prodotto_chimico', kwargs={'pk':fk_prodottochimico})
        

    
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_initial(self):
        created_by = self.request.user
        fk_prodottochimico = self.kwargs['fk_prodottochimico']
        return {
            'created_by': created_by,
            'fk_prodottochimico': fk_prodottochimico
        }
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        fk_prodottochimico = self.kwargs['fk_prodottochimico'] 
        context['fk_prodottochimico'] = ProdottoChimico.objects.get(pk=fk_prodottochimico)
        
        return context

class PrezzoProdottoUpdateView(LoginRequiredMixin, UpdateView):
    model = PrezzoProdotto
    form_class = PrezzoProdottoModelForm
    template_name = 'chem_man/prezzo_prodotto_chimico.html'
    success_message = 'Prezzo modificato correttamente!'
    
    
    def get_success_url(self):        
        fk_prodottochimico=self.object.fk_prodottochimico.pk
        return reverse_lazy('chem_man:modifica_prodotto_chimico', kwargs={'pk':fk_prodottochimico})
            

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        fk_prodottochimico = self.kwargs['fk_prodottochimico'] 
        context['fk_prodottochimico'] = ProdottoChimico.objects.get(pk=fk_prodottochimico)
        
        return context


def delete_prezzo_prodotto_chimico(request, pk): 
        deleteobject = get_object_or_404(PrezzoProdotto, pk = pk) 
        fk_prodottochimico = deleteobject.fk_prodottochimico.pk               
        deleteobject.delete()
        url_match = reverse_lazy('chem_man:modifica_prodotto_chimico', kwargs={'pk':fk_prodottochimico})
        return redirect(url_match)
    


# Scheda Tecnica Prodotto Chimico

class SchedaTecnicaCreateView(LoginRequiredMixin,CreateView):
    model = SchedaTecnica
    form_class = SchedaTecnicaModelForm
    template_name = 'chem_man/scheda_tecnica.html'
    success_message = 'Scheda tecnica aggiunta correttamente!'
    

    def get_success_url(self):                               
        fk_prodottochimico=self.object.fk_prodottochimico.pk
        return reverse_lazy('chem_man:modifica_prodotto_chimico', kwargs={'pk':fk_prodottochimico})
        

    
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_initial(self):
        created_by = self.request.user
        fk_prodottochimico = self.kwargs['fk_prodottochimico']
        return {
            'created_by': created_by,
            'fk_prodottochimico': fk_prodottochimico
        }
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        fk_prodottochimico = self.kwargs['fk_prodottochimico'] 
        context['fk_prodottochimico'] = ProdottoChimico.objects.get(pk=fk_prodottochimico)
        
        return context

class SchedaTecnicaUpdateView(LoginRequiredMixin, UpdateView):
    model = SchedaTecnica
    form_class = SchedaTecnicaModelForm
    template_name = 'chem_man/scheda_tecnica.html'
    success_message = 'Scehda tecnica modificata correttamente!'
    
    
    def get_success_url(self):        
        fk_prodottochimico=self.object.fk_prodottochimico.pk
        return reverse_lazy('chem_man:modifica_prodotto_chimico', kwargs={'pk':fk_prodottochimico})
            

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        fk_prodottochimico = self.kwargs['fk_prodottochimico'] 
        context['fk_prodottochimico'] = ProdottoChimico.objects.get(pk=fk_prodottochimico)
        
        return context


def delete_scheda_tecnica(request, pk): 
        deleteobject = get_object_or_404(SchedaTecnica, pk = pk) 
        fk_prodottochimico = deleteobject.fk_prodottochimico.pk               
        deleteobject.delete()
        url_match = reverse_lazy('chem_man:modifica_prodotto_chimico', kwargs={'pk':fk_prodottochimico})
        return redirect(url_match)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django_filters.views import FilterView


from .filters import ProdottoChimicoFilter, SostanzaFilter, SostanzaSVHCFilter

from .models import (ProdottoChimico, PrezzoProdotto, SchedaTecnica,
                    Sostanza, SostanzaSVHC, HazardStatement, PrecautionaryStatement,
                    )



from .forms import (ProdottoChimicoModelForm, PrezzoProdottoModelForm,
                    SchedaTecnicaModelForm, SostanzaModelForm,
                    SostanzaSVHCModelForm, HazardStatementModelForm,
                    PrecautionaryStatementModelForm,
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


# TABELLE GENERICHE

def tabelle_generiche(request):
    sostanze = Sostanza.objects.all()
    tot_sostanze = Sostanza.objects.count()
    sostanze_svhc = SostanzaSVHC.objects.all()
    tot_sostanze_svhc = SostanzaSVHC.objects.count()
    hazard_statements = HazardStatement.objects.all()
    precautionary_statements = PrecautionaryStatement.objects.all()
    

    sostanze_filter = SostanzaFilter(request.GET, queryset=sostanze)
    filtered_sostanze = sostanze_filter.qs  # Ottieni i record filtrati
    sostanze_filter_count = filtered_sostanze.count()  # Conta i record filtrati
    
    sostanze_svhc_filter = SostanzaSVHCFilter(request.GET, queryset=sostanze_svhc)
    filtered_sostanze_svhc = sostanze_svhc_filter.qs
    sostanze_svhc_filter_count = filtered_sostanze_svhc.count()
    

    # Paginazione Sostanze
    page_sostanze = request.GET.get('page', 1)
    paginator_sostanze = Paginator(filtered_sostanze, 50)
    try:
        sostanze_paginator = paginator_sostanze.page(page_sostanze)
    except PageNotAnInteger:
        sostanze_paginator = paginator_sostanze.page(1)
    except EmptyPage:
        sostanze_paginator = paginator_sostanze.page(paginator_sostanze.num_pages)

    # Paginazione Sostanze SVHC
    page_sostanze_svhc = request.GET.get('page', 1)
    paginator_sostanze_svhc = Paginator(filtered_sostanze_svhc, 50)
    try:
        sostanze_svhc_paginator = paginator_sostanze_svhc.page(page_sostanze_svhc)
    except PageNotAnInteger:
        sostanze_svhc_paginator = paginator_sostanze_svhc.page(1)
    except EmptyPage:
        sostanze_svhc_paginator = paginator_sostanze_svhc.page(paginator_sostanze_svhc.num_pages)

    context = {
        'sostanze': sostanze,
        'sostanze_paginator': sostanze_paginator,
        'sostanze_svhc': sostanze_svhc,
        'sostanze_svhc_paginator': sostanze_svhc_paginator,
        'tot_sostanze_svhc': tot_sostanze_svhc,
        'hazard_statements': hazard_statements,
        'precautionary_statements': precautionary_statements, 
        'filter_sostanze': sostanze_filter,
        'filter_svhc': sostanze_svhc_filter,
        'tot_sostanze': tot_sostanze,
        'sostanze_filter_count': sostanze_filter_count,
        'sostanze_svhc_filter_count': sostanze_svhc_filter_count
    }

    return render(request, 'chem_man/generiche/tabelle_generiche.html', context)





# Sostanze

class SostanzaCreateView(LoginRequiredMixin,CreateView):
    model = Sostanza
    form_class = SostanzaModelForm
    template_name = 'chem_man/generiche/sostanza.html'
    success_message = 'Sostanza aggiunta correttamente!'


    def get_success_url(self):
        return reverse_lazy('chem_man:tabelle_generiche')



    def form_valid(self, form):
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    def get_initial(self):
        created_by = self.request.user
        return {
            'created_by': created_by,
        }

class SostanzaUpdateView(LoginRequiredMixin, UpdateView):
    model = Sostanza
    form_class = SostanzaModelForm
    template_name = 'chem_man/generiche/sostanza.html'
    success_message = 'Sostanza modificata correttamente!'


    def get_success_url(self):
        return reverse_lazy('chem_man:tabelle_generiche')


    def form_valid(self, form):
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # pk_prodottochimico = self.object.pk
        # context['elenco_prezzi'] = PrezzoProdotto.objects.filter(fk_prodottochimico=pk_prodottochimico)
        # context['elenco_schede_tecniche'] = SchedaTecnica.objects.filter(fk_prodottochimico=pk_prodottochimico)

        return context


def delete_sostanza(request, pk):
        deleteobject = get_object_or_404(Sostanza, pk = pk)
        deleteobject.delete()
        url_match = reverse_lazy('chem_man:tabelle_generiche')
        return redirect(url_match)
    

# Sostanze SVHC


class SostanzaSVHCCreateView(LoginRequiredMixin,CreateView):
    model = SostanzaSVHC
    form_class = SostanzaSVHCModelForm
    template_name = 'chem_man/generiche/sostanza_svhc.html'
    success_message = 'Sostanza SVHC aggiunta correttamente!'


    def get_success_url(self):
        return reverse_lazy('chem_man:tabelle_generiche')



    def form_valid(self, form):
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    def get_initial(self):
        created_by = self.request.user
        return {
            'created_by': created_by,
        }

class SostanzaSVHCUpdateView(LoginRequiredMixin, UpdateView):
    model = SostanzaSVHC
    form_class = SostanzaSVHCModelForm
    template_name = 'chem_man/generiche/sostanza_svhc.html'
    success_message = 'Sostanza SVHC modificata correttamente!'


    def get_success_url(self):
        return reverse_lazy('chem_man:tabelle_generiche')


    def form_valid(self, form):
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # pk_prodottochimico = self.object.pk
        # context['elenco_prezzi'] = PrezzoProdotto.objects.filter(fk_prodottochimico=pk_prodottochimico)
        # context['elenco_schede_tecniche'] = SchedaTecnica.objects.filter(fk_prodottochimico=pk_prodottochimico)

        return context


def delete_sostanza_svhc(request, pk):
        deleteobject = get_object_or_404(SostanzaSVHC, pk = pk)
        deleteobject.delete()
        url_match = reverse_lazy('chem_man:tabelle_generiche')
        return redirect(url_match)
    
    
# Hazard Statements

class HazardStatementCreateView(LoginRequiredMixin,CreateView):
    model = HazardStatement
    form_class = HazardStatementModelForm
    template_name = 'chem_man/generiche/hazard_statement.html'
    success_message = 'Indicazione di Rischio aggiunta correttamente!'


    def get_success_url(self):
        return reverse_lazy('chem_man:tabelle_generiche')



    def form_valid(self, form):
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    def get_initial(self):
        created_by = self.request.user
        return {
            'created_by': created_by,
        }

class HazardStatementUpdateView(LoginRequiredMixin, UpdateView):
    model = HazardStatement
    form_class = HazardStatementModelForm
    template_name = 'chem_man/generiche/hazard_statement.html'
    success_message = 'Indicazione di Rischio modificata correttamente!'


    def get_success_url(self):
        return reverse_lazy('chem_man:tabelle_generiche')


    def form_valid(self, form):
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # pk_prodottochimico = self.object.pk
        # context['elenco_prezzi'] = PrezzoProdotto.objects.filter(fk_prodottochimico=pk_prodottochimico)
        # context['elenco_schede_tecniche'] = SchedaTecnica.objects.filter(fk_prodottochimico=pk_prodottochimico)

        return context


def delete_hazard_statement(request, pk):
        deleteobject = get_object_or_404(HazardStatement, pk = pk)
        deleteobject.delete()
        url_match = reverse_lazy('chem_man:tabelle_generiche')
        return redirect(url_match)
    

# Precautionary Statement


class PrecautionaryStatementCreateView(LoginRequiredMixin,CreateView):
    model = PrecautionaryStatement
    form_class = PrecautionaryStatementModelForm
    template_name = 'chem_man/generiche/precautionary_statement.html'
    success_message = 'Consiglio di prudenza aggiunto correttamente!'


    def get_success_url(self):
        return reverse_lazy('chem_man:tabelle_generiche')



    def form_valid(self, form):
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    def get_initial(self):
        created_by = self.request.user
        return {
            'created_by': created_by,
        }

class PrecautionaryStatementUpdateView(LoginRequiredMixin, UpdateView):
    model = PrecautionaryStatement
    form_class = PrecautionaryStatementModelForm
    template_name = 'chem_man/generiche/precautionary_statement.html'
    success_message = 'Consiglio di Prodenza modificato correttamente!'


    def get_success_url(self):
        return reverse_lazy('chem_man:tabelle_generiche')


    def form_valid(self, form):
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # pk_prodottochimico = self.object.pk
        # context['elenco_prezzi'] = PrezzoProdotto.objects.filter(fk_prodottochimico=pk_prodottochimico)
        # context['elenco_schede_tecniche'] = SchedaTecnica.objects.filter(fk_prodottochimico=pk_prodottochimico)

        return context


def delete_precautionary_statement(request, pk):
        deleteobject = get_object_or_404(PrecautionaryStatement, pk = pk)
        deleteobject.delete()
        url_match = reverse_lazy('chem_man:tabelle_generiche')
        return redirect(url_match)
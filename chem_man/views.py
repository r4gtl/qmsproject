import datetime
import pdb
from datetime import date

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from .filters import *
from .forms import *
from .models import (AcquistoProdottoChimico, DettaglioAcquistoProdottoChimico,
                     DettaglioOrdineProdottoChimico, HazardStatement,
                     HazardStatement_SDS, ImballaggioPC, OrdineProdottoChimico,
                     PrecautionaryStatement, PrecautionaryStatement_SDS,
                     PrezzoProdotto, ProdottoChimico, SchedaSicurezza,
                     SchedaTecnica, SimboloGHS, SimboloGHS_SDS, Sostanza,
                     Sostanza_SDS, SostanzaSVHC)


def home_prodotti_chimici(request):
    prodotti_chimici = ProdottoChimico.objects.all()
    prodotti_chimici_filter = ProdottoChimicoFilter(request.GET, queryset=prodotti_chimici)
    ultimo_agg_svhc = SostanzaSVHC.objects.aggregate(max_date=Max('data_inclusione'))['max_date']    
    page = request.GET.get('page', 1)
    paginator = Paginator(prodotti_chimici_filter.qs, 50)  # Utilizza fornitori_filter.qs per la paginazione

    try:
        prodotti_chimici_paginator = paginator.page(page)
    except PageNotAnInteger:
        prodotti_chimici_paginator = paginator.page(1)
    except EmptyPage:
        prodotti_chimici_paginator = paginator.page(paginator.num_pages)

    context = {
        
        'prodotti_chimici_paginator': prodotti_chimici_paginator,
        'filter': prodotti_chimici_filter,
        'ultimo_agg_svhc': ultimo_agg_svhc
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
        context['elenco_schede_sicurezza'] = SchedaSicurezza.objects.filter(fk_prodottochimico=pk_prodottochimico)

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
    tot_hazard_statements = HazardStatement.objects.count()
    precautionary_statements = PrecautionaryStatement.objects.all()
    tot_precautionary_statements = PrecautionaryStatement.objects.count()
    simboli_ghs = SimboloGHS.objects.all()
    tot_simboli_ghs = SimboloGHS.objects.count()
    imballaggi_pc = ImballaggioPC.objects.all()
    tot_imballaggi_pc = ImballaggioPC.objects.count()

    
    sostanze_filter = SostanzaFilter(request.GET, queryset=sostanze)
    filtered_sostanze = sostanze_filter.qs  # Ottieni i record filtrati
    sostanze_filter_count = filtered_sostanze.count()  # Conta i record filtrati
    
    sostanze_svhc_filter = SostanzaSVHCFilter(request.GET, queryset=sostanze_svhc)
    filtered_sostanze_svhc = sostanze_svhc_filter.qs
    sostanze_svhc_filter_count = filtered_sostanze_svhc.count()

    hazard_statements_filter = HazardStatementFilter(request.GET, queryset=hazard_statements)
    filtered_hazard_statements = hazard_statements_filter.qs
    hazard_statements_filter_count = filtered_hazard_statements.count()

    precautionary_statements_filter = PrecautionaryStatementFilter(request.GET, queryset=precautionary_statements)
    filtered_precautionary_statements = precautionary_statements_filter.qs
    precautionary_statements_filter_count = filtered_precautionary_statements.count()

    simboli_ghs_filter = SimboloGHSFilter(request.GET, queryset=simboli_ghs)
    filtered_simboli_ghs = simboli_ghs_filter.qs
    simboli_ghs_filter_count = filtered_simboli_ghs.count()
    
    imballaggi_pc_filter = ImballaggioPCFilter(request.GET, queryset=imballaggi_pc)
    filtered_imballaggi_pc = imballaggi_pc_filter.qs
    imballaggi_pc_filter_count = filtered_imballaggi_pc.count()


    # Paginazione Sostanze
    page_sostanze = request.GET.get('page_sostanze', 1)
    paginator_sostanze = Paginator(filtered_sostanze, 50)
    
    try:
        sostanze_paginator = paginator_sostanze.page(page_sostanze)
    except PageNotAnInteger:
        sostanze_paginator = paginator_sostanze.page(1)
    except EmptyPage:
        sostanze_paginator = paginator_sostanze.page(paginator_sostanze.num_pages)

    # Paginazione Sostanze SVHC
    page_sostanze_svhc = request.GET.get('page_sostanze_svhc', 1)
    paginator_sostanze_svhc = Paginator(filtered_sostanze_svhc, 50)
    try:
        sostanze_svhc_paginator = paginator_sostanze_svhc.page(page_sostanze_svhc)
    except PageNotAnInteger:
        sostanze_svhc_paginator = paginator_sostanze_svhc.page(1)
    except EmptyPage:
        sostanze_svhc_paginator = paginator_sostanze_svhc.page(paginator_sostanze_svhc.num_pages)

    # Paginazione Hazard Statements
    page_hazard_statements = request.GET.get('page_hazard_statements', 1)
    paginator_hazard_statements = Paginator(filtered_hazard_statements, 50)
    try:
        hazard_statements_paginator = paginator_hazard_statements.page(page_hazard_statements)
    except PageNotAnInteger:
        hazard_statements_paginator = paginator_hazard_statements.page(1)
    except EmptyPage:
        hazard_statements_paginator = paginator_hazard_statements.page(paginator_hazard_statements.num_pages)

    # Paginazione Precautionary Statements
    page_precautionary_statements = request.GET.get('page_precautionary_statements', 1)
    paginator_precautionary_statements = Paginator(filtered_precautionary_statements, 50)
    try:
        precautionary_statements_paginator = paginator_precautionary_statements.page(page_precautionary_statements)
    except PageNotAnInteger:
        precautionary_statements_paginator = paginator_precautionary_statements.page(1)
    except EmptyPage:
        precautionary_statements_paginator = paginator_precautionary_statements.page(paginator_precautionary_statements.num_pages)

    # Paginazione Simboli GHS
    page_simboli_ghs = request.GET.get('page_simboli_ghs', 1)
    paginator_simboli_ghs = Paginator(filtered_simboli_ghs, 50)
    try:
        simboli_ghs_paginator = paginator_simboli_ghs.page(page_simboli_ghs)
    except PageNotAnInteger:
        simboli_ghs_paginator = paginator_simboli_ghs.page(1)
    except EmptyPage:
        simboli_ghs_paginator = paginator_simboli_ghs.page(paginator_simboli_ghs.num_pages)

    # Paginazione Imballaggi PC
    page_imballaggi_pc = request.GET.get('page_imballaggi_pc', 1)
    imballaggi_pc_paginator = Paginator(filtered_imballaggi_pc, 50)
    try:
        imballaggi_pc_paginator = imballaggi_pc_paginator.page(page_imballaggi_pc)
    except PageNotAnInteger:
        imballaggi_pc_paginator = imballaggi_pc_paginator.page(1)
    except EmptyPage:
        imballaggi_pc_paginator = imballaggi_pc_paginator.page(imballaggi_pc_paginator.num_pages)


    context = {
        # Sostanze
        'sostanze': sostanze,
        'sostanze_paginator': sostanze_paginator,
        'tot_sostanze': tot_sostanze,
        'filter_sostanze': sostanze_filter,
        'sostanze_filter_count': sostanze_filter_count,
        
        # Sostanza SVHC
        'sostanze_svhc': sostanze_svhc,
        'sostanze_svhc_paginator': sostanze_svhc_paginator,
        'tot_sostanze_svhc': tot_sostanze_svhc,
        'filter_svhc': sostanze_svhc_filter,
        'sostanze_svhc_filter_count': sostanze_svhc_filter_count,
        
        # Hazard Statements
        'hazard_statements': hazard_statements,
        'hazard_statements_paginator': hazard_statements_paginator,
        'tot_hazard_statements': tot_hazard_statements,
        'filter_hazard_statements': hazard_statements_filter,
        'hazard_statements_filter_count': hazard_statements_filter_count,

        # Precautionary Statements
        'precautionary_statements': precautionary_statements, 
        'tot_precautionary_statements': tot_precautionary_statements,
        'precautionary_statements_paginator': precautionary_statements_paginator,
        'filter_precautionary_statements': precautionary_statements_filter,
        'precautionary_statements_filter_count': precautionary_statements_filter_count,

        # Simboli GHS
        'simboli_ghs': simboli_ghs, 
        'tot_simboli_ghs': tot_simboli_ghs,
        'simboli_ghs_paginator': simboli_ghs_paginator,
        'filter_simboli_ghs': simboli_ghs_filter,
        'simboli_ghs_filter_count': simboli_ghs_filter_count,

        # Imballaggi PC
        'imballaggi_pc': imballaggi_pc, 
        'tot_imballaggi_pc': tot_imballaggi_pc,
        'imballaggi_pc_paginator': imballaggi_pc_paginator,
        'filter_imballaggi_pc': imballaggi_pc_filter,
        'imballaggi_pc_filter_count': imballaggi_pc_filter_count

    }
    print(f'Filter_sostanze: {sostanze_filter}')
    print(f'Filter_svhc: {sostanze_svhc_filter}')
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
    success_message = 'Consiglio di prudenza modificato correttamente!'


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



# Simboli GHS


class SimboloGHSCreateView(LoginRequiredMixin,CreateView):
    model = SimboloGHS
    form_class = SimboloGHSModelForm
    template_name = 'chem_man/generiche/simbolo_ghs.html'
    success_message = 'Simbolo aggiunto correttamente!'


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

class SimboloGHSUpdateView(LoginRequiredMixin, UpdateView):
    model = SimboloGHS
    form_class = SimboloGHSModelForm
    template_name = 'chem_man/generiche/simbolo_ghs.html'
    success_message = 'Simbolo modificato correttamente!'


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


def delete_simbolo_ghs(request, pk):
        deleteobject = get_object_or_404(SimboloGHS, pk = pk)
        deleteobject.delete()
        url_match = reverse_lazy('chem_man:tabelle_generiche')
        return redirect(url_match)


# Imballaggi PC

class ImballaggioPCCreateView(LoginRequiredMixin,CreateView):
    model = ImballaggioPC
    form_class = ImballaggioPCModelForm
    template_name = 'chem_man/generiche/imballaggio_pc.html'
    success_message = 'Imballaggio aggiunto correttamente!'


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

class ImballaggioPCUpdateView(LoginRequiredMixin, UpdateView):
    model = ImballaggioPC
    form_class = ImballaggioPCModelForm
    template_name = 'chem_man/generiche/imballaggio_pc.html'
    success_message = 'Imballaggio aggiunto correttamente!'


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


def delete_imballaggio_pc(request, pk):
        deleteobject = get_object_or_404(ImballaggioPC, pk = pk)
        deleteobject.delete()
        url_match = reverse_lazy('chem_man:tabelle_generiche')
        return redirect(url_match)



# Schede di Sicurezza
class SchedaSicurezzaCreateView(LoginRequiredMixin,CreateView):
    model = SchedaSicurezza
    form_class = SchedaSicurezzaModelForm
    template_name = 'chem_man/scheda_sicurezza.html'
    success_message = 'Scheda sicurezza aggiunta correttamente!'


    def get_success_url(self):
        if 'salva_esci' in self.request.POST:
            fk_prodottochimico=self.object.fk_prodottochimico.pk
            return reverse_lazy('chem_man:modifica_prodotto_chimico', kwargs={'pk':fk_prodottochimico})

        pk=self.object.pk
        fk_prodottochimico= self.object.fk_prodottochimico.pk
        return reverse_lazy('chem_man:modifica_scheda_sicurezza', kwargs={'fk_prodottochimico':fk_prodottochimico, 'pk':pk})


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
        context['focus_button'] = 'id_data_revisione'

        return context

class SchedaSicurezzaUpdateView(LoginRequiredMixin, UpdateView):
    model = SchedaSicurezza
    form_class = SchedaSicurezzaModelForm
    template_name = 'chem_man/scheda_sicurezza.html'
    success_message = 'Scheda sicurezza modificata correttamente!'


    def get_success_url(self):
        if 'salva_esci' in self.request.POST:
            fk_prodottochimico=self.object.fk_prodottochimico.pk
            return reverse_lazy('chem_man:modifica_prodotto_chimico', kwargs={'pk':fk_prodottochimico})

        fk_prodottochimico=self.object.fk_prodottochimico.pk
        pk_sds=self.object.pk
        return reverse_lazy('chem_man:modifica_scheda_sicurezza', kwargs={'fk_prodottochimico':fk_prodottochimico, 'pk':pk_sds})


    def form_valid(self, form):
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk_sds = self.kwargs['pk']
        fk_prodottochimico = self.kwargs['fk_prodottochimico']   
        if 'focus_button' in self.kwargs:
            focus_button_param = self.kwargs['focus_button'] # Leggo kwargs se c'è l'id del pulsante in cui mettere il focus
            print(f'focus_button_param: {focus_button_param}')
            context['focus_button'] = focus_button_param
        else:
            context['focus_button'] = 'id_data_revisione'

        context['fk_prodottochimico'] = ProdottoChimico.objects.get(pk=fk_prodottochimico)
        context['elenco_simboli'] = SimboloGHS_SDS.objects.filter(fk_sds=pk_sds)
        context['elenco_hazard_statements'] = HazardStatement_SDS.objects.filter(fk_sds=pk_sds)
        context['elenco_precautionary_statements'] = PrecautionaryStatement_SDS.objects.filter(fk_sds=pk_sds)
        context['elenco_sostanze'] = Sostanza_SDS.objects.filter(fk_sds=pk_sds)

        return context


def delete_scheda_sicurezza(request, pk):
        deleteobject = get_object_or_404(SchedaSicurezza, pk = pk)
        fk_prodottochimico = deleteobject.fk_prodottochimico.pk
        deleteobject.delete()
        url_match = reverse_lazy('chem_man:modifica_prodotto_chimico', kwargs={'pk':fk_prodottochimico})
        return redirect(url_match)


# Simboli GSH collegati alle SDS

class SimboloGHS_SDSCreateView(LoginRequiredMixin,CreateView):
    model = SimboloGHS_SDS
    form_class = SimboloGHS_SDSModelForm
    template_name = 'chem_man/simbolo_ghs_sds.html'
    success_message = 'Simbolo aggiunto correttamente!'
    

    def get_success_url(self):   
        fk_sds=self.object.fk_sds.pk
        fk_prodottochimico= self.object.fk_sds.fk_prodottochimico.pk
        focus_button = 'btn_ghs_symbol'  # Imposto il pulsante su cui settare il focus
        
        return reverse_lazy('chem_man:modifica_scheda_sicurezza_with_focus_button', kwargs={'fk_prodottochimico':fk_prodottochimico, 'pk':fk_sds, 'focus_button': focus_button})
    
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_initial(self):
        created_by = self.request.user
        fk_sds = self.kwargs['fk_sds']

        return {
            'created_by': created_by,
            'fk_sds': fk_sds
        }

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['fk_sds'] 
        sds=SchedaSicurezza.objects.get(pk=pk)

        context['fk_sds'] = SchedaSicurezza.objects.get(pk=pk) 
        context['fk_prodottochimico'] = sds.fk_prodottochimico

        return context

class SimboloGHS_SDSUpdateView(LoginRequiredMixin, UpdateView):
    model = SimboloGHS_SDS
    form_class = SimboloGHS_SDSModelForm
    template_name = 'chem_man/simbolo_ghs_sds.html'
    success_message = 'Simbolo modificato correttamente!'
    
    
    def get_success_url(self):   
        fk_sds=self.object.fk_sds.pk
        fk_prodottochimico= self.object.fk_sds.fk_prodottochimico.pk
        focus_button = 'btn_ghs_symbol'  # Imposto il pulsante su cui settare il focus        
        success_url = reverse_lazy('chem_man:modifica_scheda_sicurezza_with_focus_button', kwargs={'fk_prodottochimico': fk_prodottochimico, 'pk': fk_sds, 'focus_button': focus_button})
        
        return success_url
        
    

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['fk_sds'] 
        sds=SchedaSicurezza.objects.get(pk=pk)        
        context['fk_prodottochimico'] = sds.fk_prodottochimico   
        context['fk_sds'] = SchedaSicurezza.objects.get(pk=pk)
        return context



def delete_simbolo_ghs_sds(request, pk): 
        deleteobject = get_object_or_404(SimboloGHS_SDS, pk = pk) 
        fk_sds = deleteobject.fk_sds.pk   
        fk_prodottochimico= deleteobject.fk_sds.fk_prodottochimico.pk             
        deleteobject.delete()
        focus_button = 'btn_ghs_symbol'  # Imposto il pulsante su cui settare il focus
        url_match = reverse_lazy('chem_man:modifica_scheda_sicurezza', kwargs={'fk_prodottochimico':fk_prodottochimico, 'pk':fk_sds, 'focus_button': focus_button})
        return redirect(url_match)



# Hazard statement collegati alle SDS

class HazardStatement_SDSCreateView(LoginRequiredMixin,CreateView):
    model = HazardStatement_SDS
    form_class = HazardStatement_SDSModelForm
    template_name = 'chem_man/hazard_statement_sds.html'
    success_message = 'Istruzione di pericolo aggiunta correttamente!'
    

    def get_success_url(self):   
        fk_sds=self.object.fk_sds.pk
        fk_prodottochimico= self.object.fk_sds.fk_prodottochimico.pk
        focus_button = 'btn_hazard_statement'  # Imposto il pulsante su cui settare il focus        
        success_url = reverse_lazy('chem_man:modifica_scheda_sicurezza_with_focus_button', kwargs={'fk_prodottochimico': fk_prodottochimico, 'pk': fk_sds, 'focus_button': focus_button})
        
        return success_url
    
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_initial(self):
        created_by = self.request.user
        fk_sds = self.kwargs['fk_sds']

        return {
            'created_by': created_by,
            'fk_sds': fk_sds
        }

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['fk_sds'] 
        sds=SchedaSicurezza.objects.get(pk=pk)
        context['fk_sds'] = SchedaSicurezza.objects.get(pk=pk) 
        context['fk_prodottochimico'] = sds.fk_prodottochimico

        return context

class HazardStatement_SDSUpdateView(LoginRequiredMixin, UpdateView):
    model = HazardStatement_SDS
    form_class = HazardStatement_SDSModelForm
    template_name = 'chem_man/hazard_statement_sds.html'
    success_message = 'Istruzione di pericolo modificata correttamente!'
    
    
    def get_success_url(self):   
        fk_sds=self.object.fk_sds.pk
        fk_prodottochimico= self.object.fk_sds.fk_prodottochimico.pk
        focus_button = 'btn_hazard_statement'  # Imposto il pulsante su cui settare il focus        
        success_url = reverse_lazy('chem_man:modifica_scheda_sicurezza_with_focus_button', kwargs={'fk_prodottochimico': fk_prodottochimico, 'pk': fk_sds, 'focus_button': focus_button})
        
        return success_url
    

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['fk_sds'] 
        sds=SchedaSicurezza.objects.get(pk=pk)        
        context['fk_prodottochimico'] = sds.fk_prodottochimico   
        context['fk_sds'] = SchedaSicurezza.objects.get(pk=pk)
        return context



def delete_hazard_statement_sds(request, pk): 
        deleteobject = get_object_or_404(HazardStatement_SDS, pk = pk) 
        fk_sds = deleteobject.fk_sds.pk   
        fk_prodottochimico= deleteobject.fk_sds.fk_prodottochimico.pk             
        deleteobject.delete()
        url_match = reverse_lazy('chem_man:modifica_scheda_sicurezza', kwargs={'fk_prodottochimico':fk_prodottochimico, 'pk':fk_sds})
        return redirect(url_match)



# Consigli di prudenza collegati alle SDS

class PrecautionaryStatement_SDSCreateView(LoginRequiredMixin,CreateView):
    model = PrecautionaryStatement_SDS
    form_class = PrecautionaryStatement_SDSModelForm
    template_name = 'chem_man/precautionary_statement_sds.html'
    success_message = 'Consiglio di prudenza aggiunto correttamente!'
    

    def get_success_url(self):   
        fk_sds=self.object.fk_sds.pk
        fk_prodottochimico= self.object.fk_sds.fk_prodottochimico.pk
        focus_button = 'btn_precautionary_statement'  # Imposto il pulsante su cui settare il focus        
        success_url = reverse_lazy('chem_man:modifica_scheda_sicurezza_with_focus_button', kwargs={'fk_prodottochimico': fk_prodottochimico, 'pk': fk_sds, 'focus_button': focus_button})
        
        return success_url
    
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_initial(self):
        created_by = self.request.user
        fk_sds = self.kwargs['fk_sds']

        return {
            'created_by': created_by,
            'fk_sds': fk_sds
        }

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['fk_sds'] 
        sds=SchedaSicurezza.objects.get(pk=pk)

        context['fk_sds'] = SchedaSicurezza.objects.get(pk=pk) 
        context['fk_prodottochimico'] = sds.fk_prodottochimico

        return context

class PrecautionaryStatement_SDSUpdateView(LoginRequiredMixin, UpdateView):
    model = PrecautionaryStatement_SDS
    form_class = PrecautionaryStatement_SDSModelForm
    template_name = 'chem_man/precautionary_statement_sds.html'
    success_message = 'Consiglio di prudenza modificato correttamente!'
    
    
    def get_success_url(self):   
        fk_sds=self.object.fk_sds.pk
        fk_prodottochimico= self.object.fk_sds.fk_prodottochimico.pk
        focus_button = 'btn_precautionary_statement'  # Imposto il pulsante su cui settare il focus        
        success_url = reverse_lazy('chem_man:modifica_scheda_sicurezza_with_focus_button', kwargs={'fk_prodottochimico': fk_prodottochimico, 'pk': fk_sds, 'focus_button': focus_button})
        
        return success_url
    

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['fk_sds'] 
        sds=SchedaSicurezza.objects.get(pk=pk)        
        context['fk_prodottochimico'] = sds.fk_prodottochimico   
        context['fk_sds'] = SchedaSicurezza.objects.get(pk=pk)
        return context



def delete_precautionary_statement_sds(request, pk): 
        deleteobject = get_object_or_404(PrecautionaryStatement_SDS, pk = pk) 
        fk_sds = deleteobject.fk_sds.pk   
        fk_prodottochimico= deleteobject.fk_sds.fk_prodottochimico.pk             
        deleteobject.delete()
        url_match = reverse_lazy('chem_man:modifica_scheda_sicurezza', kwargs={'fk_prodottochimico':fk_prodottochimico, 'pk':fk_sds})
        return redirect(url_match)


# Sostanze collegate alle SDS

class Sostanza_SDSCreateView(LoginRequiredMixin,CreateView):
    model = Sostanza_SDS
    form_class = Sostanza_SDSModelForm
    template_name = 'chem_man/sostanza_sds.html'
    success_message = 'Sostanza aggiunta correttamente!'
    

    def get_success_url(self):   
        fk_sds=self.object.fk_sds.pk
        fk_prodottochimico= self.object.fk_sds.fk_prodottochimico.pk
        focus_button = 'btn_substances'  # Imposto il pulsante su cui settare il focus        
        success_url = reverse_lazy('chem_man:modifica_scheda_sicurezza_with_focus_button', kwargs={'fk_prodottochimico': fk_prodottochimico, 'pk': fk_sds, 'focus_button': focus_button})
        
        return success_url
    
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        
        # Recupera l'ID della sostanza selezionata dal form
        fk_sostanza_id = self.request.POST.get('fk_sostanza')
        # Ottieni l'istanza del modello Sostanza corrispondente all'ID
        fk_sostanza = get_object_or_404(Sostanza, pk=fk_sostanza_id)
        # Crea un'istanza di Sostanza_SDS senza salvare nel database
        sostanza_sds = form.save(commit=False)
        # Assegna l'istanza di Sostanza al campo fk_sostanza del modello Sostanza_SDS
        sostanza_sds.fk_sostanza = fk_sostanza
        # Salva l'istanza di Sostanza_SDS nel database
        sostanza_sds.save()

        return super().form_valid(form)
    
    def form_invalid(self, form):
        # Stampa gli errori del form nella console
        print(form.errors)

        # Esegui altre azioni desiderate in caso di form non valido

        # Puoi anche chiamare la versione di default di form_invalid() per eseguire le azioni predefinite
        return super().form_invalid(form)

    def get_initial(self):
        created_by = self.request.user
        fk_sds = self.kwargs['fk_sds']

        return {
            'created_by': created_by,
            'fk_sds': fk_sds
        }

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['fk_sds'] 
        sds=SchedaSicurezza.objects.get(pk=pk)

        context['fk_sds'] = SchedaSicurezza.objects.get(pk=pk) 
        context['fk_prodottochimico'] = sds.fk_prodottochimico
        context['filter'] = SostanzaFilter(data=self.request.GET, queryset=Sostanza.objects.all())

        return context

class Sostanza_SDSUpdateView(LoginRequiredMixin, UpdateView):
    model = Sostanza_SDS
    form_class = Sostanza_SDSModelForm
    template_name = 'chem_man/sostanza_sds.html'
    success_message = 'Sostanza modificata correttamente!'
    
    def get_initial(self):
        initial = super().get_initial()
        fk_sostanza = self.object.fk_sostanza.pk
        initial['fk_sostanza'] = fk_sostanza
        return initial

    def get_success_url(self):   
        fk_sds=self.object.fk_sds.pk
        fk_prodottochimico= self.object.fk_sds.fk_prodottochimico.pk
        focus_button = 'btn_substances'  # Imposto il pulsante su cui settare il focus        
        success_url = reverse_lazy('chem_man:modifica_scheda_sicurezza_with_focus_button', kwargs={'fk_prodottochimico': fk_prodottochimico, 'pk': fk_sds, 'focus_button': focus_button})
        
        return success_url
    

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url

         # Recupera l'ID della sostanza selezionata dal form
        fk_sostanza_id = self.request.POST.get('fk_sostanza')
        # Ottieni l'istanza del modello Sostanza corrispondente all'ID
        fk_sostanza = get_object_or_404(Sostanza, pk=fk_sostanza_id)
        # Crea un'istanza di Sostanza_SDS senza salvare nel database
        sostanza_sds = form.save(commit=False)
        # Assegna l'istanza di Sostanza al campo fk_sostanza del modello Sostanza_SDS
        sostanza_sds.fk_sostanza = fk_sostanza
        # Salva l'istanza di Sostanza_SDS nel database
        sostanza_sds.save()

        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['fk_sds'] 
        sds=SchedaSicurezza.objects.get(pk=pk)        
        context['fk_prodottochimico'] = sds.fk_prodottochimico   
        context['fk_sds'] = SchedaSicurezza.objects.get(pk=pk)
        context['current_fk_sostanza'] = self.object.fk_sostanza.pk
        return context



def delete_sostanza_sds(request, pk): 
        deleteobject = get_object_or_404(Sostanza_SDS, pk = pk) 
        fk_sds = deleteobject.fk_sds.pk   
        fk_prodottochimico= deleteobject.fk_sds.fk_prodottochimico.pk             
        deleteobject.delete()
        url_match = reverse_lazy('chem_man:modifica_scheda_sicurezza', kwargs={'fk_prodottochimico':fk_prodottochimico, 'pk':fk_sds})
        return redirect(url_match)
    
    
#===========================================================================================================================    
'''ACQUISTI PRODOTTI CHIMICI'''
'''HOME PAGE ACQUISTI'''

def dashboard_acquisti_prodotti_chimici(request):
    ordini_pc = OrdineProdottoChimico.objects.all()
    ordini_pc_filter = OrdineProdottoChimicoFilter(request.GET, queryset = ordini_pc)
    
    page = request.GET.get('page', 1)
    paginator = Paginator(ordini_pc_filter.qs, 50)  # Utilizza fornitori_filter.qs per la paginazione

    try:
        ordini_pc_paginator = paginator.page(page)
    except PageNotAnInteger:
        ordini_pc_paginator = paginator.page(1)
    except EmptyPage:
        ordini_pc_paginator = paginator.page(paginator.num_pages)
    context = {
        'ordini_pc': ordini_pc,
        'ordini_pc_paginator': ordini_pc_paginator,
        'ordini_pc_filter': ordini_pc_filter
        
    }
    return render(request, 'chem_man/acquisti/home_acquisti_prodotti_chimici.html', context)



'''PRIMA PARTE ORDINI'''


def home_ordini_prodotti_chimici(request):
    ordini_pc = OrdineProdottoChimico.objects.all().order_by('-data_ordine')
    ordini_pc_filter = OrdineProdottoChimicoFilter(request.GET, queryset = ordini_pc)
    
    page = request.GET.get('page', 1)
    paginator = Paginator(ordini_pc_filter.qs, 50)  # Utilizza fornitori_filter.qs per la paginazione

    try:
        ordini_pc_paginator = paginator.page(page)
    except PageNotAnInteger:
        ordini_pc_paginator = paginator.page(1)
    except EmptyPage:
        ordini_pc_paginator = paginator.page(paginator.num_pages)
    context = {
        'ordini_pc': ordini_pc,
        'ordini_pc_paginator': ordini_pc_paginator,
        'ordini_pc_filter': ordini_pc_filter
        
    }
    return render(request, 'chem_man/acquisti/home_ordini_prodotti_chimici.html', context)

# Ordine

class OrdineProdottoChimicoCreateView(LoginRequiredMixin,CreateView):
    model = OrdineProdottoChimico
    form_class = OrdineProdottoChimicoModelForm
    template_name = 'chem_man/acquisti/ordine_prodotto_chimico.html'
    success_message = 'Ordine aggiunto correttamente!'


    def get_success_url(self):
        if 'salva_esci' in self.request.POST:
            return reverse_lazy('chem_man:home_ordini_prodotti_chimici')

        pk_ordine=self.object.pk
        return reverse_lazy('chem_man:modifica_ordine_prodotto_chimico', kwargs={'pk':pk_ordine})



    def form_valid(self, form):
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        initial['created_by'] = self.request.user
        initial['numero_ordine'] = self.calculate_initial_numero_ordine()
        return initial

    def calculate_initial_numero_ordine(self):
        current_year = date.today().year
        max_value = OrdineProdottoChimico.objects.filter(created_at__year=current_year).aggregate(Max('numero_ordine'))['numero_ordine__max']
        return (max_value + 1) if max_value else 1

class OrdineProdottoChimicoUpdateView(LoginRequiredMixin, UpdateView):
    model = OrdineProdottoChimico
    form_class = OrdineProdottoChimicoModelForm
    template_name = 'chem_man/acquisti/ordine_prodotto_chimico.html'
    success_message = 'Ordine modificato correttamente!'


    def get_success_url(self):
        if 'salva_esci' in self.request.POST:
            return reverse_lazy('chem_man:home_ordini_prodotti_chimici')

        pk_ordine=self.object.pk
        return reverse_lazy('chem_man:modifica_ordine_prodotto_chimico', kwargs={'pk':pk_ordine})


    def form_valid(self, form):
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk_ordine = self.object.pk
        # context['elenco_prezzi'] = PrezzoProdotto.objects.filter(fk_prodottochimico=pk_prodottochimico)
        # context['elenco_schede_tecniche'] = SchedaTecnica.objects.filter(fk_prodottochimico=pk_prodottochimico)
        context['elenco_dettagli'] = DettaglioOrdineProdottoChimico.objects.filter(fk_ordine=pk_ordine)
        
        return context


def delete_ordine_prodotto_chimico(request, pk):
        deleteobject = get_object_or_404(OrdineProdottoChimico, pk = pk)
        deleteobject.delete()
        url_match = reverse_lazy('chem_man:home_ordini_prodotti_chimici')
        return redirect(url_match)


# Dettaglio Ordine



class DettaglioOrdineProdottoChimicoCreateView(LoginRequiredMixin,CreateView):
    model = DettaglioOrdineProdottoChimico
    form_class = DettaglioOrdineProdottoChimicoModelForm
    template_name = 'chem_man/acquisti/dettaglio_ordine_prodotto_chimico.html'
    success_message = 'Dettaglio ordine aggiunto correttamente!'
    

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        ordine_id = self.kwargs.get('fk_ordine')
        ordine = OrdineProdottoChimico.objects.get(pk=ordine_id)
        form.fields['fk_prodotto_chimico'].queryset = form.fields['fk_prodotto_chimico'].queryset.filter(fk_fornitore=ordine.fk_fornitore)
        return form


    def get_success_url(self):   
        fk_ordine=self.object.fk_ordine.pk
        
        return reverse_lazy('chem_man:modifica_ordine_prodotto_chimico', kwargs={'pk':fk_ordine})
    
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_initial(self):
        created_by = self.request.user
        fk_ordine = self.kwargs['fk_ordine']

        return {
            'created_by': created_by,
            'fk_ordine': fk_ordine
        }

    def get_context_data(self, **kwargs):
        
        
        context = super().get_context_data(**kwargs)
        
        
        pk = self.kwargs['fk_ordine']         
        context['ordine_pc'] = pk
        #pass
        return context
    
class DettaglioOrdineProdottoChimicoUpdateView(LoginRequiredMixin, UpdateView):
    model = DettaglioOrdineProdottoChimico
    form_class = DettaglioOrdineProdottoChimicoModelForm
    template_name = 'chem_man/acquisti/dettaglio_ordine_prodotto_chimico.html'
    success_message = 'Dettaglio ordine modificato correttamente!'


    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        ordine_id = self.kwargs.get('fk_ordine')
        ordine = OrdineProdottoChimico.objects.get(pk=ordine_id)
        form.fields['fk_prodotto_chimico'].queryset = form.fields['fk_prodotto_chimico'].queryset.filter(fk_fornitore=ordine.fk_fornitore)
        return form


    def get_success_url(self):        

        fk_ordine = self.kwargs['fk_ordine']
        pk_dettaglio=self.object.pk
        return reverse_lazy('chem_man:modifica_ordine_prodotto_chimico', kwargs={'pk':fk_ordine})


    def form_valid(self, form):
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fk_ordine = self.kwargs['fk_ordine']
        context['elenco_dettagli'] = DettaglioOrdineProdottoChimico.objects.filter(fk_ordine=fk_ordine)
        context['ordine_pc']=fk_ordine
        context['dettagli_ordine'] = get_object_or_404(OrdineProdottoChimico, pk=fk_ordine)
        # context['elenco_schede_tecniche'] = SchedaTecnica.objects.filter(fk_prodottochimico=pk_prodottochimico)
        # context['elenco_schede_sicurezza'] = SchedaSicurezza.objects.filter(fk_prodottochimico=pk_prodottochimico)

        return context


def delete_dettaglio_ordine_prodotto_chimico(request, pk):
        deleteobject = get_object_or_404(DettaglioOrdineProdottoChimico, pk = pk)
        fk_ordine = deleteobject.fk_ordine.pk
        deleteobject.delete()
        url_match = reverse_lazy('chem_man:modifica_ordine_prodotto_chimico', kwargs={'pk':fk_ordine})
        return redirect(url_match)


'''SECONDA PARTE: ACQUISTI'''



def home_acquisti_prodotti_chimici(request):
    acquisti_pc = AcquistoProdottoChimico.objects.all()
    acquisti_pc_filter = AcquistoProdottoChimicoFilter(request.GET, queryset = acquisti_pc)
    
    page = request.GET.get('page', 1)
    paginator = Paginator(acquisti_pc_filter.qs, 50)  # Utilizza fornitori_filter.qs per la paginazione

    try:
        acquisti_pc_paginator = paginator.page(page)
    except PageNotAnInteger:
        acquisti_pc_paginator = paginator.page(1)
    except EmptyPage:
        acquisti_pc_paginator = paginator.page(paginator.num_pages)
    context = {
        'acquisti_pc': acquisti_pc,
        'acquisti_pc_paginator': acquisti_pc_paginator,
        'acquisti_pc_filter': acquisti_pc_filter
        
    }
    return render(request, 'chem_man/acquisti/home_acquisti_prodotti_chimici.html', context)

# Acquisto

class AcquistoProdottoChimicoCreateView(LoginRequiredMixin,CreateView):
    model = AcquistoProdottoChimico
    form_class = AcquistoProdottoChimicoModelForm
    template_name = 'chem_man/acquisti/acquisto_prodotto_chimico.html'
    success_message = 'Documento aggiunto correttamente!'


    def get_success_url(self):
        if 'salva_esci' in self.request.POST:
            return reverse_lazy('chem_man:home_acquisti_prodotti_chimici')

        pk_acquisto=self.object.pk
        return reverse_lazy('chem_man:modifica_acquisto_prodotto_chimico', kwargs={'pk':pk_acquisto})



    def form_valid(self, form):
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        initial['created_by'] = self.request.user
        
        return initial

    

class AcquistoProdottoChimicoUpdateView(LoginRequiredMixin, UpdateView):
    model = AcquistoProdottoChimico
    form_class = AcquistoProdottoChimicoModelForm
    template_name = 'chem_man/acquisti/acquisto_prodotto_chimico.html'
    success_message = 'Documento modificato correttamente!'


    def get_success_url(self):
        if 'salva_esci' in self.request.POST:
            return reverse_lazy('chem_man:home_documenti_acquisto_prodotti_chimici')

        pk_acquisto=self.object.pk
        return reverse_lazy('chem_man:modifica_acquisto_prodotto_chimico', kwargs={'pk':pk_acquisto})


    def form_valid(self, form):
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk_acquisto = self.object.pk
        # context['elenco_prezzi'] = PrezzoProdotto.objects.filter(fk_prodottochimico=pk_prodottochimico)
        # context['elenco_schede_tecniche'] = SchedaTecnica.objects.filter(fk_prodottochimico=pk_prodottochimico)
        context['elenco_dettagli'] = DettaglioAcquistoProdottoChimico.objects.filter(fk_acquisto=pk_acquisto)

        return context


def delete_acquisto_prodotto_chimico(request, pk):
        deleteobject = get_object_or_404(AcquistoProdottoChimico, pk = pk)
        deleteobject.delete()
        url_match = reverse_lazy('chem_man:home_documenti_acquisto_prodotti_chimici')
        return redirect(url_match)


# Dettaglio Acquisto
class DettaglioAcquistoProdottoChimicoCreateView(LoginRequiredMixin,CreateView):
    model = DettaglioAcquistoProdottoChimico
    form_class = DettaglioAcquistoProdottoChimicoModelForm
    template_name = 'chem_man/acquisti/dettaglio_acquisto_prodotto_chimico.html'
    success_message = 'Dettaglio acquisto aggiunto correttamente!'
    

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        acquisto_id = self.kwargs.get('fk_acquisto')
        acquisto = AcquistoProdottoChimico.objects.get(pk=acquisto_id)
        form.fields['fk_prodotto_chimico'].queryset = form.fields['fk_prodotto_chimico'].queryset.filter(fk_fornitore=acquisto.fk_fornitore)
        return form


    def get_success_url(self):   
        fk_acquisto=self.object.fk_acquisto.pk
        
        return reverse_lazy('chem_man:modifica_acquisto_prodotto_chimico', kwargs={'pk':fk_acquisto})
    
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_initial(self):
        created_by = self.request.user
        fk_acquisto = self.kwargs['fk_acquisto']

        return {
            'created_by': created_by,
            'fk_acquisto': fk_acquisto
        }

    def get_context_data(self, **kwargs):
        
        
        context = super().get_context_data(**kwargs)
        
        
        pk = self.kwargs['fk_acquisto']         
        context['acquisto_pc'] = pk
        #pass
        return context
    
class DettaglioAcquistoProdottoChimicoUpdateView(LoginRequiredMixin, UpdateView):
    model = DettaglioAcquistoProdottoChimico
    form_class = DettaglioAcquistoProdottoChimicoModelForm
    template_name = 'chem_man/acquisti/dettaglio_acquisto_prodotto_chimico.html'
    success_message = 'Dettaglio acquisto modificato correttamente!'


    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        acquisto_id = self.kwargs.get('fk_acquisto')
        acquisto = AcquistoProdottoChimico.objects.get(pk=acquisto_id)
        form.fields['fk_prodotto_chimico'].queryset = form.fields['fk_prodotto_chimico'].queryset.filter(fk_fornitore=acquisto.fk_fornitore)
        return form


    def get_success_url(self):        

        fk_acquisto = self.kwargs['fk_acquisto']
        pk_dettaglio=self.object.pk
        return reverse_lazy('chem_man:modifica_acquisto_prodotto_chimico', kwargs={'pk':fk_acquisto})


    def form_valid(self, form):
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fk_acquisto = self.kwargs['fk_acquisto']
        context['elenco_dettagli'] = DettaglioAcquistoProdottoChimico.objects.filter(fk_acquisto=fk_acquisto)
        context['acquisto_pc']=fk_acquisto
        # context['elenco_schede_tecniche'] = SchedaTecnica.objects.filter(fk_prodottochimico=pk_prodottochimico)
        # context['elenco_schede_sicurezza'] = SchedaSicurezza.objects.filter(fk_prodottochimico=pk_prodottochimico)

        return context


def delete_dettaglio_acquisto_prodotto_chimico(request, pk):
        deleteobject = get_object_or_404(DettaglioAcquistoProdottoChimico, pk = pk)
        fk_acquisto = deleteobject.fk_acquisto.pk
        deleteobject.delete()
        url_match = reverse_lazy('chem_man:modifica_acquisto_prodotto_chimico', kwargs={'pk':fk_acquisto})
        return redirect(url_match)



# Stampe
def stampa_ordine(request, pk):
    # Recupera il prodotto con l'id fornito o restituisce 404 se non trovato
    ordine = get_object_or_404(OrdineProdottoChimico, id=pk)
    dettagli_ordine=DettaglioOrdineProdottoChimico.objects.filter(fk_ordine=pk)
    context = {
        'ordine': ordine,
        'dettagli_ordine': dettagli_ordine
    }
    # Restituisci il prodotto nel template
    return render(request, 'chem_man/acquisti/stampa_ordine.html', context)
    
    
def controlla_dettagli_ordine(request, pk):
    ordine = get_object_or_404(OrdineProdottoChimico, id=pk)
    dettagli_presenti = DettaglioOrdineProdottoChimico.objects.filter(fk_ordine=ordine).exists()

    return JsonResponse({'dettagli_presenti': dettagli_presenti})



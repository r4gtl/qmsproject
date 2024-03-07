from datetime import date

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from human_resources.models import DettaglioRegistroFormazione, HR_Safety

from .filters import *
from .forms import *
from .models import *

# Create your views here.



def antincendio_home(request):

    squadra_antincendio = HR_Safety.objects.filter(fk_safety_role__descrizione="Addetto Antincendio").filter(data_fine_incarico__isnull=True)    
    # Per quanto riguarda lo scadenzario specifico, valutare se generare un elenco di fixture in cui
    # non si possano modificare le descrizioni in modo da potersi fidare delle descrizioni
    today = date.today()
    scadenzario = []
    scadenze_antincendio = DettaglioRegistroFormazione.objects.filter(prossima_scadenza__gte=today, fk_registro_formazione__fk_corso__descrizione__icontains='incendio')    
    for scadenza in scadenze_antincendio:
        
        scadenzario.append({
            'scadenza': scadenza.prossima_scadenza,
            'descrizione': str(scadenza.fk_hr) + ", " + str(scadenza.fk_registro_formazione.fk_corso.descrizione),            
            'url': "human_resources:human_resources",            
            'mese_anno': scadenza.prossima_scadenza.strftime('%B %Y')
            
        })
    
    
    
    
    # Estintori
    estintori = Estintore.objects.all()
    tot_estintori = Estintore.objects.filter(data_dismissione__isnull=True).count()
    estintori_filter = EstintoreFilter(request.GET, queryset=estintori)
    filtered_estintori = estintori_filter.qs
    estintori_filter_count = filtered_estintori.count()
    
    # Paginazione Estintori
    page_estintori = request.GET.get('page', 1)
    paginator_estintori = Paginator(filtered_estintori, 50)
    try:
        estintori_paginator = paginator_estintori.page(page_estintori)
    except PageNotAnInteger:
        estintori_paginator = paginator_estintori.page(1)
    except EmptyPage:
        estintori_paginator = paginator_estintori.page(paginator_estintori.num_pages)


     # Idranti
    idranti = Idrante.objects.all()
    tot_idranti = Idrante.objects.filter(data_dismissione__isnull=True).count()
    idranti_filter = IdranteFilter(request.GET, queryset=idranti)
    filtered_idranti = idranti_filter.qs
    idranti_filter_count = filtered_idranti.count()
    
    # Paginazione Idranti
    page_idranti = request.GET.get('page', 1)
    paginator_idranti = Paginator(filtered_idranti, 50)
    try:
        idranti_paginator = paginator_idranti.page(page_idranti)
    except PageNotAnInteger:
        idranti_paginator = paginator_idranti.page(1)
    except EmptyPage:
        idranti_paginator = paginator_idranti.page(paginator_idranti.num_pages)

    
     # Porte/Uscite
    porte_uscite = PortaUscita.objects.all()
    tot_porte_uscite = PortaUscita.objects.count()
    porte_uscite_filter = PortaUscitaFilter(request.GET, queryset=porte_uscite)
    filtered_porte_uscite = porte_uscite_filter.qs
    porte_uscite_filter_count = filtered_porte_uscite.count()
    
    # Paginazione Idranti
    page_porte_uscite = request.GET.get('page', 1)
    paginator_porte_uscite = Paginator(filtered_porte_uscite, 50)
    try:
        porte_uscite_paginator = paginator_porte_uscite.page(page_porte_uscite)
    except PageNotAnInteger:
        porte_uscite_paginator = paginator_porte_uscite.page(1)
    except EmptyPage:
        porte_uscite_paginator = paginator_porte_uscite.page(paginator_porte_uscite.num_pages)

    
    # Attrezzatura antincendio
    attrezzature_antincendio = AttrezzaturaAntincendio.objects.all()
    tot_attrezzature_antincendio = AttrezzaturaAntincendio.objects.count()
    attrezzature_antincendio_filter = AttrezzaturaAntincendioFilter(request.GET, queryset=attrezzature_antincendio)
    filtered_attrezzature_antincendio = attrezzature_antincendio_filter.qs
    attrezzature_antincendio_filter_count = filtered_attrezzature_antincendio.count()
    
    # Paginazione Attrezzatura antincendio
    page_attrezzature_antincendio = request.GET.get('page', 1)
    paginator_attrezzature_antincendio = Paginator(filtered_attrezzature_antincendio, 50)
    try:
        attrezzature_antincendio_paginator = paginator_attrezzature_antincendio.page(page_attrezzature_antincendio)
    except PageNotAnInteger:
        attrezzature_antincendio_paginator = paginator_attrezzature_antincendio.page(1)
    except EmptyPage:
        attrezzature_antincendio_paginator = paginator_attrezzature_antincendio.page(paginator_attrezzature_antincendio.num_pages)
        
    
    # Impianto Spegnimento
    impianti_spegnimento = ImpiantoSpegnimento.objects.all()
    tot_impianti_spegnimento = ImpiantoSpegnimento.objects.count()
    impianti_spegnimento_filter = ImpiantoSpegnimentoFilter(request.GET, queryset=impianti_spegnimento)
    filtered_impianti_spegnimento = impianti_spegnimento_filter.qs
    impianti_spegnimento_filter_count = filtered_impianti_spegnimento.count()
    
    # Paginazione Attrezzatura antincendio
    page_impianti_spegnimento = request.GET.get('page', 1)
    paginator_impianti_spegnimento = Paginator(filtered_impianti_spegnimento, 50)
    try:
        impianti_spegnimento_paginator = paginator_impianti_spegnimento.page(page_impianti_spegnimento)
    except PageNotAnInteger:
        impianti_spegnimento_paginator = paginator_impianti_spegnimento.page(1)
    except EmptyPage:
        impianti_spegnimento_paginator = paginator_impianti_spegnimento.page(paginator_impianti_spegnimento.num_pages)
    

    context = {

        'squadra_antincendio': squadra_antincendio,
        'scadenzario': scadenzario,
        

        # Estintori
        'estintori': estintori,
        'estintori_paginator': estintori_paginator,
        'tot_estintori': tot_estintori,
        'filter_estintori': estintori_filter,
        'estintori_filter_count': estintori_filter_count,

        # Idranti
        'idranti': idranti,
        'idranti_paginator': idranti_paginator,
        'tot_idranti': tot_idranti,
        'filter_idranti': idranti_filter,
        'idranti_filter_count': idranti_filter_count,

        # Porte/Uscite
        'porte_uscite': porte_uscite,
        'porte_uscite_paginator': porte_uscite_paginator,
        'tot_porte_uscite': tot_porte_uscite,
        'filter_porte_uscite': porte_uscite_filter,
        'porte_uscite_filter_count': porte_uscite_filter_count,
        
        # Attrezzatura Antincendio
        'attrezzature_antincendio': attrezzature_antincendio,
        'attrezzature_antincendio_paginator': attrezzature_antincendio_paginator,
        'tot_attrezzature_antincendio': tot_attrezzature_antincendio,
        'filter_attrezzature_antincendio': attrezzature_antincendio_filter,
        'attrezzature_antincendio_filter_count': attrezzature_antincendio_filter_count,
        
        # Impianto Spegnimento
        'impianti_spegnimento': impianti_spegnimento,
        'impianti_spegnimento_paginator': impianti_spegnimento_paginator,
        'tot_impianti_spegnimento': tot_impianti_spegnimento,
        'filter_impianti_spegnimento': impianti_spegnimento_filter,
        'impianti_spegnimento_filter_count': impianti_spegnimento_filter_count,
        
    }

    return render(request, 'antincendio/antincendio_home.html', context)



# Estintori

class EstintoreCreateView(LoginRequiredMixin,CreateView):
    model = Estintore
    form_class = EstintoreModelForm
    template_name = 'antincendio/estintore.html'
    success_message = 'Estintore aggiunto correttamente!'


    def get_success_url(self):
        return reverse_lazy('antincendio:antincendio_home')



    def form_valid(self, form):
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    def get_initial(self):
        created_by = self.request.user
        return {
            'created_by': created_by,
        }

class EstintoreUpdateView(LoginRequiredMixin, UpdateView):
    model = Estintore
    form_class = EstintoreModelForm
    template_name = 'antincendio/estintore.html'
    success_message = 'Estintore modificato correttamente!'


    def get_success_url(self):
        return reverse_lazy('antincendio:antincendio_home')


    def form_valid(self, form):
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # pk_prodottochimico = self.object.pk
        # context['elenco_prezzi'] = PrezzoProdotto.objects.filter(fk_prodottochimico=pk_prodottochimico)
        # context['elenco_schede_tecniche'] = SchedaTecnica.objects.filter(fk_prodottochimico=pk_prodottochimico)

        return context


def delete_estintore(request, pk):
        deleteobject = get_object_or_404(Estintore, pk = pk)
        deleteobject.delete()
        url_match = reverse_lazy('antincendio:antincendio_home')
        return redirect(url_match)


# Idranti

class IdranteCreateView(LoginRequiredMixin,CreateView):
    model = Idrante
    form_class = IdranteModelForm
    template_name = 'antincendio/idrante.html'
    success_message = 'Idrante aggiunto correttamente!'


    def get_success_url(self):
        return reverse_lazy('antincendio:antincendio_home')



    def form_valid(self, form):
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    def get_initial(self):
        created_by = self.request.user
        return {
            'created_by': created_by,
        }

class IdranteUpdateView(LoginRequiredMixin, UpdateView):
    model = Idrante
    form_class = IdranteModelForm
    template_name = 'antincendio/idrante.html'
    success_message = 'Idrante modificato correttamente!'


    def get_success_url(self):
        return reverse_lazy('antincendio:antincendio_home')


    def form_valid(self, form):
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # pk_prodottochimico = self.object.pk
        # context['elenco_prezzi'] = PrezzoProdotto.objects.filter(fk_prodottochimico=pk_prodottochimico)
        # context['elenco_schede_tecniche'] = SchedaTecnica.objects.filter(fk_prodottochimico=pk_prodottochimico)

        return context


def delete_idrante(request, pk):
        deleteobject = get_object_or_404(Idrante, pk = pk)
        deleteobject.delete()
        url_match = reverse_lazy('antincendio:antincendio_home')
        return redirect(url_match)



# Porte/Uscite

class PortaUscitaCreateView(LoginRequiredMixin,CreateView):
    model = PortaUscita
    form_class = PortaUscitaModelForm
    template_name = 'antincendio/porta_uscita.html'
    success_message = 'Porta/Uscita aggiunta correttamente!'


    def get_success_url(self):
        return reverse_lazy('antincendio:antincendio_home')



    def form_valid(self, form):
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    def get_initial(self):
        created_by = self.request.user
        return {
            'created_by': created_by,
        }

class PortaUscitaUpdateView(LoginRequiredMixin, UpdateView):
    model = PortaUscita
    form_class = PortaUscitaModelForm
    template_name = 'antincendio/porta_uscita.html'
    success_message = 'Porta/Uscita modificata correttamente!'


    def get_success_url(self):
        return reverse_lazy('antincendio:antincendio_home')


    def form_valid(self, form):
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # pk_prodottochimico = self.object.pk
        # context['elenco_prezzi'] = PrezzoProdotto.objects.filter(fk_prodottochimico=pk_prodottochimico)
        # context['elenco_schede_tecniche'] = SchedaTecnica.objects.filter(fk_prodottochimico=pk_prodottochimico)

        return context


def delete_porta_uscita(request, pk):
        deleteobject = get_object_or_404(PortaUscita, pk = pk)
        deleteobject.delete()
        url_match = reverse_lazy('antincendio:antincendio_home')
        return redirect(url_match)
    
# Attrezzatura antincendio

class AttrezzaturaAntincendioCreateView(LoginRequiredMixin,CreateView):
    model = AttrezzaturaAntincendio
    form_class = AttrezzaturaAntincendioModelForm
    template_name = 'antincendio/attrezzatura_antincendio.html'
    success_message = 'Attrezzatura aggiunta correttamente!'


    def get_success_url(self):
        return reverse_lazy('antincendio:antincendio_home')



    def form_valid(self, form):
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    def get_initial(self):
        created_by = self.request.user
        return {
            'created_by': created_by,
        }

class AttrezzaturaAntincendioUpdateView(LoginRequiredMixin, UpdateView):
    model = AttrezzaturaAntincendio
    form_class = AttrezzaturaAntincendioModelForm
    template_name = 'antincendio/attrezzatura_antincendio.html'
    success_message = 'Attrezzatura modificata correttamente!'


    def get_success_url(self):
        return reverse_lazy('antincendio:antincendio_home')


    def form_valid(self, form):
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # pk_prodottochimico = self.object.pk
        # context['elenco_prezzi'] = PrezzoProdotto.objects.filter(fk_prodottochimico=pk_prodottochimico)
        # context['elenco_schede_tecniche'] = SchedaTecnica.objects.filter(fk_prodottochimico=pk_prodottochimico)

        return context


def delete_attrezzatura_antincendio(request, pk):
        deleteobject = get_object_or_404(AttrezzaturaAntincendio, pk = pk)
        deleteobject.delete()
        url_match = reverse_lazy('antincendio:antincendio_home')
        return redirect(url_match)

# Impianto spegnimento

class ImpiantoSpegnimentoCreateView(LoginRequiredMixin,CreateView):
    model = ImpiantoSpegnimento
    form_class = ImpiantoSpegnimentoModelForm
    template_name = 'antincendio/impianto_spegnimento.html'
    success_message = 'Impianto aggiunto correttamente!'


    def get_success_url(self):
        return reverse_lazy('antincendio:antincendio_home')



    def form_valid(self, form):
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    def get_initial(self):
        created_by = self.request.user
        return {
            'created_by': created_by,
        }

class ImpiantoSpegnimentoUpdateView(LoginRequiredMixin, UpdateView):
    model = ImpiantoSpegnimento
    form_class = ImpiantoSpegnimentoModelForm
    template_name = 'antincendio/impianto_spegnimento.html'
    success_message = 'Impianto modificato correttamente!'


    def get_success_url(self):
        return reverse_lazy('antincendio:antincendio_home')


    def form_valid(self, form):
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # pk_prodottochimico = self.object.pk
        # context['elenco_prezzi'] = PrezzoProdotto.objects.filter(fk_prodottochimico=pk_prodottochimico)
        # context['elenco_schede_tecniche'] = SchedaTecnica.objects.filter(fk_prodottochimico=pk_prodottochimico)

        return context


def delete_impianto_spegnimento(request, pk):
        deleteobject = get_object_or_404(ImpiantoSpegnimento, pk = pk)
        deleteobject.delete()
        url_match = reverse_lazy('antincendio:antincendio_home')
        return redirect(url_match)



# Registro controlli attrezzature antincendio
def registro_controlli_home(request):

    registri_controlli = RegistroControlliAntincendio.objects.all()
    registri_controlli_filter = RegistroControlliAntincendioFilter(request.GET, queryset=registri_controlli)
    page = request.GET.get('page', 1)
    paginator = Paginator(registri_controlli_filter.qs, 50)  

    try:
        registri_controlli_paginator = paginator.page(page)
    except PageNotAnInteger:
        registri_controlli_paginator = paginator.page(1)
    except EmptyPage:
        registri_controlli_paginator = paginator.page(paginator.num_pages)


    context = {
        'registri_controlli_paginator': registri_controlli_paginator,
        'filter': registri_controlli_filter,

    }

    return render(request, 'antincendio/registri_antincendio/registri_antincendio_home.html', context)


# Registro Controlli

class RegistroControlliAntincendioCreateView(LoginRequiredMixin,CreateView):
    model = RegistroControlliAntincendio
    form_class = RegistroControlliAntincendioModelForm
    template_name = 'antincendio/registri_antincendio/registro_antincendio.html'
    success_message = 'Registro aggiunto correttamente!'


    def get_success_url(self):
        return reverse_lazy('antincendio:registro_controlli_home')



    def form_valid(self, form):
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    def get_initial(self):
        created_by = self.request.user
        return {
            'created_by': created_by,
        }

class RegistroControlliAntincendioUpdateView(LoginRequiredMixin, UpdateView):
    model = RegistroControlliAntincendio
    form_class = RegistroControlliAntincendioModelForm
    template_name = 'antincendio/registri_antincendio/registro_antincendio.html'
    success_message = 'Registro modificato correttamente!'


    def get_success_url(self):
        return reverse_lazy('antincendio:registro_controlli_home')


    def form_valid(self, form):
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk_registro = self.object.pk        
        context['registro'] = RegistroControlliAntincendio.objects.get(pk=pk_registro)
        

        return context


def delete_registro_controlli(request, pk):
        deleteobject = get_object_or_404(RegistroControlliAntincendio, pk = pk)
        deleteobject.delete()
        url_match = reverse_lazy('antincendio:registro_controlli_home')
        return redirect(url_match)


'''
View per gestire la stampa di un registro con tutte le attrezzature antincendio
'''
def stampa_mezzi_antincendio(request):
    estintori = Estintore.objects.filter(data_dismissione__isnull=True)
    idranti = Idrante.objects.filter(data_dismissione__isnull=True)
    porte_uscite = PortaUscita.objects.all()
    impianti_spegnimento = ImpiantoSpegnimento.objects.all()
    attrezzature = AttrezzaturaAntincendio.objects.all()
    data_odierna = date.today()
    year_today = date.today().year

    context = {
        'estintori': estintori,
        'idranti': idranti,
        'porte_uscite': porte_uscite,
        'impianti_spegnimento': impianti_spegnimento,
        'attrezzature': attrezzature,
        'data_odierna': data_odierna,
        'year_today': year_today

    }

    return render(request, 'antincendio/reports/registro_mezzi_antincendio.html', context)





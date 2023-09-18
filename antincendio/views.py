from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import *
from .filters import *
from .forms import *



# Create your views here.



def antincendio_home(request):

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




    context = {
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
        # pk_prodottochimico = self.object.pk
        # context['elenco_prezzi'] = PrezzoProdotto.objects.filter(fk_prodottochimico=pk_prodottochimico)
        # context['elenco_schede_tecniche'] = SchedaTecnica.objects.filter(fk_prodottochimico=pk_prodottochimico)

        return context


def delete_registro_controlli(request, pk):
        deleteobject = get_object_or_404(RegistroControlliAntincendio, pk = pk)
        deleteobject.delete()
        url_match = reverse_lazy('antincendio:registro_controlli_home')
        return redirect(url_match)


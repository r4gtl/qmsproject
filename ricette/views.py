from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Max
from django.views.generic.edit import CreateView, UpdateView
from .models import *
from .forms import *
from .filters import *




def home_ricette(request):
    return render(request, "ricette/home_ricette.html")


def home_ricette_rifinizione(request):
    ricette_rifinizione = RicettaRifinizione.objects.all()
    
    ricette_rifinizione_filter = RicettaRifinizioneFilter(request.GET, queryset=ricette_rifinizione)
    filtered_ricette_rifinizione = ricette_rifinizione_filter.qs  # Ottieni i record filtrati
    
    
    # Paginazione operazioni
    page_ricette_rifinizione = request.GET.get('page', 1)
    paginator_ricette_rifinizione = Paginator(filtered_ricette_rifinizione, 50)
    try:
        ricette_rifinizione_paginator = paginator_ricette_rifinizione.page(page_ricette_rifinizione)
    except PageNotAnInteger:
        ricette_rifinizione_paginator = paginator_ricette_rifinizione.page(1)
    except EmptyPage:
        ricette_rifinizione_paginator = paginator_ricette_rifinizione.page(paginator_ricette_rifinizione.num_pages)


    context = {
        # Operazioni
        'ricette_rifinizione': ricette_rifinizione,
        'ricette_rifinizione_paginator': ricette_rifinizione_paginator,        
        'filter_ricette_rifinizione': ricette_rifinizione_filter,        
        

    }

    return render(request, "ricette/home_ricette_rifinizione.html", context)
    




# Tabelle generiche


def tabelle_generiche(request):
    operazioni = OperazioneRicette.objects.all()
    tot_operazioni = OperazioneRicette.objects.count()
    operazioni_filter = OperazioneFilter(request.GET, queryset=operazioni)
    filtered_operazioni = operazioni_filter.qs  # Ottieni i record filtrati
    operazioni_filter_count = filtered_operazioni.count()  # Conta i record filtrati
    
    # Paginazione operazioni
    page_operazioni = request.GET.get('page', 1)
    paginator_operazioni = Paginator(filtered_operazioni, 50)
    try:
        operazioni_paginator = paginator_operazioni.page(page_operazioni)
    except PageNotAnInteger:
        operazioni_paginator = paginator_operazioni.page(1)
    except EmptyPage:
        operazioni_paginator = paginator_operazioni.page(paginator_operazioni.num_pages)


    context = {
        # Operazioni
        'operazioni': operazioni,
        'operazioni_paginator': operazioni_paginator,
        'tot_operazioni': tot_operazioni,
        'filter_operazioni': operazioni_filter,
        'operazioni_filter_count': operazioni_filter_count,
        

    }

    return render(request, 'ricette/generiche/tabelle_generiche.html', context)

class OperazioneRicetteCreateView(LoginRequiredMixin,CreateView):
    model = OperazioneRicette
    form_class = OperazioneRicetteModelForm
    template_name = 'ricette/generiche/operazione_ricette.html'
    success_message = 'Operazione aggiunta correttamente!'


    def get_success_url(self):
        return reverse_lazy('ricette:tabelle_generiche')



    def form_valid(self, form):
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    def get_initial(self):
        created_by = self.request.user
        return {
            'created_by': created_by,
        }

class OperazioneRicetteUpdateView(LoginRequiredMixin, UpdateView):
    model = OperazioneRicette
    form_class = OperazioneRicetteModelForm
    template_name = 'ricette/generiche/operazione_ricette.html'
    success_message = 'Operazione modificata correttamente!'


    def get_success_url(self):
        return reverse_lazy('ricette:tabelle_generiche')


    def form_valid(self, form):
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk_operazione = self.object.pk
        # context['elenco_prezzi'] = PrezzoProdotto.objects.filter(fk_prodottochimico=pk_prodottochimico)
        # context['elenco_schede_tecniche'] = SchedaTecnica.objects.filter(fk_prodottochimico=pk_prodottochimico)
        # context['elenco_schede_sicurezza'] = SchedaSicurezza.objects.filter(fk_prodottochimico=pk_prodottochimico)

        return context


def delete_operazione(request, pk):
        deleteobject = get_object_or_404(OperazioneRicette, pk = pk)
        deleteobject.delete()
        url_match = reverse_lazy('ricette:tabelle_generiche')
        return redirect(url_match)


# Ricette Rifinizione
class RicettaRifinizioneCreateView(LoginRequiredMixin,CreateView):
    model = RicettaRifinizione
    form_class = RicettaRifinizioneModelForm
    template_name = 'ricette/ricetta_rifinizione.html'
    success_message = 'Ricetta aggiunta correttamente!'


    def get_success_url(self):
        return reverse_lazy('ricette:home_ricette')



    def form_valid(self, form):
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    def get_initial(self):
        created_by = self.request.user
        return {
            'created_by': created_by,
        }

class RicettaRifinizioneUpdateView(LoginRequiredMixin, UpdateView):
    model = RicettaRifinizione
    form_class = RicettaRifinizioneModelForm
    template_name = 'rricette/ricetta_rifinizione.html'
    success_message = 'Ricetta modificata correttamente!'


    def get_success_url(self):
        return reverse_lazy('ricette:home_ricette')


    def form_valid(self, form):
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk_operazione = self.object.pk
        # context['elenco_prezzi'] = PrezzoProdotto.objects.filter(fk_prodottochimico=pk_prodottochimico)
        # context['elenco_schede_tecniche'] = SchedaTecnica.objects.filter(fk_prodottochimico=pk_prodottochimico)
        # context['elenco_schede_sicurezza'] = SchedaSicurezza.objects.filter(fk_prodottochimico=pk_prodottochimico)

        return context


def delete_ricetta_rifinizione(request, pk):
        deleteobject = get_object_or_404(RicettaRifinizione, pk = pk)
        deleteobject.delete()
        url_match = reverse_lazy('ricette:home_ricette')
        return redirect(url_match)
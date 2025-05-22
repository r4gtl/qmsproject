import datetime
import pdb
from datetime import (  # Aggiunta in data 08/02/2024 per il totale solventi acquistati nell'anno
    date, datetime)

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.staticfiles import finders
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import DecimalField, ExpressionWrapper, F, Max, Sum
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from qmsproject.context_processors import nome_sito

from .filters import *
from .forms import *
from .models import DettaglioOrdineCliente, OrdineCliente, SchedaLavorazione


def home_ordini_cliente(request):
    ordini_cliente = OrdineCliente.objects.all()
    ordini_cliente_filter = OrdineClienteFilter(
        request.GET, queryset=ordini_cliente
    )
    
    page = request.GET.get("page", 1)
    paginator = Paginator(
        ordini_cliente_filter.qs, 50
    )  

    try:
        ordini_cliente_paginator = paginator.page(page)
    except PageNotAnInteger:
        ordini_cliente_paginator = paginator.page(1)
    except EmptyPage:
        ordini_cliente_paginator = paginator.page(paginator.num_pages)
    
    context = {
        "ordini_cliente_paginator": ordini_cliente_paginator,
        "filter": ordini_cliente_filter,
        
    }
    return render(request, "vendite/home_ordini_cliente.html", context)


class OrdineClienteCreateView(LoginRequiredMixin, CreateView):
    model = OrdineCliente
    form_class = OrdineClienteModelForm
    template_name = "vendite/ordine_cliente.html"
    success_message = "Ordine aggiunto correttamente!"

    def get_success_url(self):
        if "salva_esci" in self.request.POST:
            return reverse_lazy("vendite:home_ordini_cliente")

        pk_ordine_cliente = self.object.pk
        return reverse_lazy(
            "vendite:modifica_ordine_cliente", kwargs={"pk": pk_ordine_cliente}
        )

    def form_valid(self, form):
        messages.info(self.request, self.success_message)  # Compare sul success_url
        return super().form_valid(form)

    def form_invalid(self, form):
        for errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"Errore: {error}")

        return super().form_invalid(form)

    def get_initial(self):
        created_by = self.request.user
        return {
            "created_by": created_by,
        }


class OrdineClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = OrdineCliente
    form_class = OrdineClienteModelForm
    template_name = "vendite/ordine_cliente.html"
    success_message = "Ordine Cliente modificato correttamente!"

    def get_success_url(self):
        if "salva_esci" in self.request.POST:
            return reverse_lazy("vendite:home_ordini_cliente")

        pk_ordine_cliente = self.object.pk
        return reverse_lazy(
            "vendite:modifica_ordine_cliente", kwargs={"pk": pk_ordine_cliente}
        )

    def form_valid(self, form):
        messages.info(self.request, self.success_message)  # Compare sul success_url
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Si è verificato un errore nel modulo. Per favore, correggi gli errori.",
        )
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk_ordine = self.kwargs["pk"]        
        filters = {"fk_ordine": pk_ordine}
        dettaglio_ordini = DettaglioOrdineCliente.objects.filter(**filters)        
        context["dettaglio_ordini"] = dettaglio_ordini
        
        return context


def delete_ordine_cliente(request, pk):
    deleteobject = get_object_or_404(OrdineCliente, pk=pk)
    deleteobject.delete()
    url_match = reverse_lazy("vendite:home_ordini_cliente")
    return redirect(url_match)


# Dettagli ordine

class DettaglioOrdineClienteCreateView(LoginRequiredMixin, CreateView):
    model = DettaglioOrdineCliente
    form_class = DettaglioOrdineClienteModelForm
    template_name = "vendite/dettaglio_ordine_cliente.html"
    success_message = "Dettaglio aggiunto correttamente!"

    def get_success_url(self):
        fk_ordinecliente = self.object.fk_ordine.pk
        focus_button = "btn_aggiungi_dettaglio"  # Imposto il pulsante su cui settare il focus

        return reverse_lazy(
            #"vendite:modifica_dettaglio_ordine_with_focus_button",
            "vendite:modifica_ordine_cliente", 
            kwargs={"pk": fk_ordinecliente}
        )
        

    def form_valid(self, form):
        messages.info(self.request, self.success_message)  # Compare sul success_url
        return super().form_valid(form)

    def get_initial(self):
        created_by = self.request.user
        fk_ordinecliente = self.kwargs["fk_ordine"]
        return {"created_by": created_by, "fk_ordine": fk_ordinecliente}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fk_ordinecliente = self.kwargs["fk_ordine"]
        context["fk_ordinecliente"] = OrdineCliente.objects.get(
            pk=fk_ordinecliente
        )

        return context


class DettaglioOrdineClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = DettaglioOrdineCliente
    form_class = DettaglioOrdineClienteModelForm
    template_name = "vendite/dettaglio_ordine_cliente.html"
    success_message = "Dettaglio modificato correttamente!"

    def get_success_url(self):
        fk_ordinecliente = self.object.fk_ordine.pk
        #pk_dettaglio=self.object.pk
        return reverse_lazy(
            "vendite:modifica_ordine_cliente", kwargs={"pk": fk_ordinecliente}
        )

    def form_valid(self, form):
        messages.info(self.request, self.success_message)  # Compare sul success_url
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fk_ordinecliente = self.kwargs["fk_ordine"]
        
        context["fk_ordinecliente"] = OrdineCliente.objects.get(
            pk=fk_ordinecliente
        )

        return context


def delete_dettaglio_ordine_cliente(request, pk):
    deleteobject = get_object_or_404(DettaglioOrdineCliente, pk=pk)
    fk_ordinecliente = deleteobject.fk_ordine.pk
    deleteobject.delete()
    url_match = reverse_lazy(
        "vendite:modifica_ordine_cliente", kwargs={"pk": fk_ordinecliente}
    )
    return redirect(url_match)


# SCHEDE LAVORAZIONE

def home_schede_lavorazione(request):
    schede_lavorazione = SchedaLavorazione.objects.all()
    schede_lavorazione_filter = SchedaLavorazioneFilter(
        request.GET, queryset=schede_lavorazione
    )
    
    page = request.GET.get("page", 1)
    paginator = Paginator(
        schede_lavorazione_filter.qs, 50
    )  

    try:
        schede_lavorazione_paginator = paginator.page(page)
    except PageNotAnInteger:
        schede_lavorazione_paginator = paginator.page(1)
    except EmptyPage:
        schede_lavorazione_paginator = paginator.page(paginator.num_pages)
    
    context = {
        "schede_lavorazione_paginator": schede_lavorazione_paginator,
        "filter": schede_lavorazione_filter,
        
    }
    return render(request, "vendite/home_schede_lavorazione.html", context)


class SchedaLavorazioneCreateView(LoginRequiredMixin, CreateView):
    model = SchedaLavorazione
    form_class = SchedaLavorazioneModelForm
    template_name = "vendite/scheda_lavorazione.html"
    success_message = "Scheda Lavorazione aggiunto correttamente!"

    def get_success_url(self):
        if "salva_esci" in self.request.POST:
            return reverse_lazy("vendite:home_schede_lavorazione")

        pk_scheda_lavorazione = self.object.pk
        return reverse_lazy(
            "vendite:modifica_scheda_lavorazione", kwargs={"pk": pk_scheda_lavorazione}
        )

    def form_valid(self, form):
        messages.info(self.request, self.success_message)  # Compare sul success_url
        return super().form_valid(form)

    def form_invalid(self, form):
        for errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"Errore: {error}")

        return super().form_invalid(form)

    def get_initial(self):
        created_by = self.request.user
        return {
            "created_by": created_by,
        }


class SchedaLavorazioneUpdateView(LoginRequiredMixin, UpdateView):
    model = SchedaLavorazione
    form_class = SchedaLavorazioneModelForm
    template_name = "vendite/scheda_lavorazione.html"
    success_message = "Scheda Lavorazione modificata correttamente!"

    def get_success_url(self):
        if "salva_esci" in self.request.POST:
            return reverse_lazy("vendite:home_schede_lavorazione")

        pk_scheda_lavorazione = self.object.pk
        return reverse_lazy(
            "vendite:modifica_scheda_lavorazione", kwargs={"pk": pk_scheda_lavorazione}
        )

    def form_valid(self, form):
        messages.info(self.request, self.success_message)  # Compare sul success_url
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Si è verificato un errore nel modulo. Per favore, correggi gli errori.",
        )
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #pk_scheda_lavorazione = self.kwargs["pk"]        
        #filters = {"fk_ordine": pk_ordine}
        #dettaglio_ordini = DettaglioOrdineCliente.objects.filter(**filters)        
        #context["dettaglio_ordini"] = dettaglio_ordini
        
        return context


def delete_scheda_lavorazione(request, pk):
    deleteobject = get_object_or_404(SchedaLavorazione, pk=pk)
    deleteobject.delete()
    url_match = reverse_lazy("vendite:home_schede_lavorazione")
    return redirect(url_match)
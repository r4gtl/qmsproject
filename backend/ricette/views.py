from datetime import date

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import F, FloatField, Max, OuterRef, Subquery, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from .filters import *
from .forms import *
from .models import *


def home_ricette(request):
    return render(request, "ricette/home_ricette.html")


# Ricette rifinizione pagine principali
def home_ricette_rifinizione(request):
    ricette_rifinizione = RicettaRifinizione.objects.all()

    ricette_rifinizione_filter = RicettaRifinizioneFilter(
        request.GET, queryset=ricette_rifinizione
    )
    filtered_ricette_rifinizione = (
        ricette_rifinizione_filter.qs
    )  # Ottieni i record filtrati

    # Paginazione operazioni
    page_ricette_rifinizione = request.GET.get("page", 1)
    paginator_ricette_rifinizione = Paginator(filtered_ricette_rifinizione, 50)
    try:
        ricette_rifinizione_paginator = paginator_ricette_rifinizione.page(
            page_ricette_rifinizione
        )
    except PageNotAnInteger:
        ricette_rifinizione_paginator = paginator_ricette_rifinizione.page(1)
    except EmptyPage:
        ricette_rifinizione_paginator = paginator_ricette_rifinizione.page(
            paginator_ricette_rifinizione.num_pages
        )

    context = {
        # Operazioni
        "ricette_rifinizione": ricette_rifinizione,
        "ricette_rifinizione_paginator": ricette_rifinizione_paginator,
        "filter": ricette_rifinizione_filter,
    }

    return render(request, "ricette/home_ricette_rifinizione.html", context)


def home_ricette_colori_rifinizione(request):
    ricette_colori_rifinizione = RicettaColoreRifinizione.objects.all()

    ricette_colori_rifinizione_filter = RicettaColoreRifinizioneFilter(
        request.GET, queryset=ricette_colori_rifinizione
    )
    filtered_ricette_colori_rifinizione = (
        ricette_colori_rifinizione_filter.qs
    )  # Ottieni i record filtrati

    # Paginazione operazioni
    page_ricette_colori_rifinizione = request.GET.get("page", 1)
    paginator_ricette_colori_rifinizione = Paginator(
        filtered_ricette_colori_rifinizione, 50
    )
    try:
        ricette_colori_rifinizione_paginator = (
            paginator_ricette_colori_rifinizione.page(page_ricette_colori_rifinizione)
        )
    except PageNotAnInteger:
        ricette_colori_rifinizione_paginator = (
            paginator_ricette_colori_rifinizione.page(1)
        )
    except EmptyPage:
        ricette_colori_rifinizione_paginator = (
            paginator_ricette_colori_rifinizione.page(
                paginator_ricette_colori_rifinizione.num_pages
            )
        )

    context = {
        # Operazioni
        "ricette_colori_rifinizione": ricette_colori_rifinizione,
        "ricette_colori_rifinizione_paginator": ricette_colori_rifinizione_paginator,
        "filter": ricette_colori_rifinizione_filter,
    }

    return render(request, "ricette/home_ricette_colori_rifinizione.html", context)


# Fine ricette rifinizione pagine principali


# Ricette bagnato pagine principali
def home_ricette_bagnato(request):
    ricette_bagnato = RicettaBagnato.objects.all()

    ricette_bagnato_filter = RicettaBagnatoFilter(request.GET, queryset=ricette_bagnato)
    filtered_ricette_bagnato = ricette_bagnato_filter.qs  # Ottieni i record filtrati

    # Paginazione operazioni
    page_ricette_bagnato = request.GET.get("page", 1)
    paginator_ricette_bagnato = Paginator(filtered_ricette_bagnato, 50)
    try:
        ricette_bagnato_paginator = paginator_ricette_bagnato.page(page_ricette_bagnato)
    except PageNotAnInteger:
        ricette_bagnato_paginator = paginator_ricette_bagnato.page(1)
    except EmptyPage:
        ricette_bagnato_paginator = paginator_ricette_bagnato.page(
            paginator_ricette_bagnato.num_pages
        )

    context = {
        # Operazioni
        "ricette_bagnato": ricette_bagnato,
        "ricette_bagnato_paginator": ricette_bagnato_paginator,
        "filter": ricette_bagnato_filter,
    }

    return render(request, "ricette/home_ricette_bagnato.html", context)


def home_ricette_colori_bagnato(request):
    ricette_colori_bagnato = RicettaColoreBagnato.objects.all()

    ricette_colori_bagnato_filter = RicettaColoreBagnatoFilter(
        request.GET, queryset=ricette_colori_bagnato
    )
    filtered_ricette_colori_bagnato = (
        ricette_colori_bagnato_filter.qs
    )  # Ottieni i record filtrati

    # Paginazione operazioni
    page_ricette_colori_bagnato = request.GET.get("page", 1)
    paginator_ricette_colori_bagnato = Paginator(filtered_ricette_colori_bagnato, 50)
    try:
        ricette_colori_bagnato_paginator = paginator_ricette_colori_bagnato.page(
            page_ricette_colori_bagnato
        )
    except PageNotAnInteger:
        ricette_colori_bagnato_paginator = paginator_ricette_colori_bagnato.page(1)
    except EmptyPage:
        ricette_colori_bagnato_paginator = paginator_ricette_colori_bagnato.page(
            paginator_ricette_colori_bagnato.num_pages
        )

    context = {
        # Operazioni
        "ricette_colori_bagnato": ricette_colori_bagnato,
        "ricette_colori_bagnato_paginator": ricette_colori_bagnato_paginator,
        "filter": ricette_colori_bagnato_filter,
    }

    return render(request, "ricette/home_ricette_colori_bagnato.html", context)


# Fine ricette bagnato pagine principali

# Tabelle generiche


def tabelle_generiche(request):
    operazioni = OperazioneRicette.objects.all()
    tot_operazioni = OperazioneRicette.objects.count()
    operazioni_filter = OperazioneFilter(request.GET, queryset=operazioni)
    filtered_operazioni = operazioni_filter.qs  # Ottieni i record filtrati
    operazioni_filter_count = filtered_operazioni.count()  # Conta i record filtrati

    # Paginazione operazioni
    page_operazioni = request.GET.get("page", 1)
    paginator_operazioni = Paginator(filtered_operazioni, 50)
    try:
        operazioni_paginator = paginator_operazioni.page(page_operazioni)
    except PageNotAnInteger:
        operazioni_paginator = paginator_operazioni.page(1)
    except EmptyPage:
        operazioni_paginator = paginator_operazioni.page(paginator_operazioni.num_pages)

    context = {
        # Operazioni
        "operazioni": operazioni,
        "operazioni_paginator": operazioni_paginator,
        "tot_operazioni": tot_operazioni,
        "filter_operazioni": operazioni_filter,
        "operazioni_filter_count": operazioni_filter_count,
    }

    return render(request, "ricette/generiche/tabelle_generiche.html", context)


class OperazioneRicetteCreateView(LoginRequiredMixin, CreateView):
    model = OperazioneRicette
    form_class = OperazioneRicetteModelForm
    template_name = "ricette/generiche/operazione_ricette.html"
    success_message = "Operazione aggiunta correttamente!"

    def get_success_url(self):
        return reverse_lazy("ricette:tabelle_generiche")

    def form_valid(self, form):
        messages.info(self.request, self.success_message)  # Compare sul success_url
        return super().form_valid(form)

    def get_initial(self):
        created_by = self.request.user
        return {
            "created_by": created_by,
        }


class OperazioneRicetteUpdateView(LoginRequiredMixin, UpdateView):
    model = OperazioneRicette
    form_class = OperazioneRicetteModelForm
    template_name = "ricette/generiche/operazione_ricette.html"
    success_message = "Operazione modificata correttamente!"

    def get_success_url(self):
        return reverse_lazy("ricette:tabelle_generiche")

    def form_valid(self, form):
        messages.info(self.request, self.success_message)  # Compare sul success_url
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk_operazione = self.object.pk
        # context['elenco_prezzi'] = PrezzoProdotto.objects.filter(fk_prodottochimico=pk_prodottochimico)
        # context['elenco_schede_tecniche'] = SchedaTecnica.objects.filter(fk_prodottochimico=pk_prodottochimico)
        # context['elenco_schede_sicurezza'] = SchedaSicurezza.objects.filter(fk_prodottochimico=pk_prodottochimico)

        return context


def delete_operazione(request, pk):
    deleteobject = get_object_or_404(OperazioneRicette, pk=pk)
    deleteobject.delete()
    url_match = reverse_lazy("ricette:tabelle_generiche")
    return redirect(url_match)


# Ricette Rifinizione
# Ricetta


class RicettaRifinizioneCreateView(LoginRequiredMixin, CreateView):
    model = RicettaRifinizione
    form_class = RicettaRifinizioneModelForm
    template_name = "ricette/ricetta_rifinizione.html"
    success_message = "Ricetta aggiunta correttamente!"

    def get_success_url(self):
        if "salva_esci" in self.request.POST:
            return reverse_lazy("ricette:home_ricette_rifinizione")

        pk_ricetta = self.object.pk

        return reverse_lazy(
            "ricette:modifica_ricetta_rifinizione", kwargs={"pk": pk_ricetta}
        )

    def form_valid(self, form):
        if "salva_esci" in self.request.POST:
            return redirect("ricette:home_ricette_rifinizione")
        else:
            form.instance.created_by = self.request.user
            messages.info(self.request, self.success_message)
            return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        if self.request.GET.get("numero_ricetta"):
            print(f"Articolo: ")
            fk_articolo = self.request.GET.get("fk_articolo")
            last_recipe = (
                RicettaRifinizione.objects.filter(fk_articolo=fk_articolo)
                .order_by("-numero_revisione")
                .first()
            )
            numero_revisione = last_recipe.numero_revisione + 1
            numero_ricetta = self.request.GET.get("numero_ricetta")
            data_ricetta = self.request.GET.get("data_ricetta")
            numero_revisione = numero_revisione
            data_revisione = self.request.GET.get("data_revisione")
            note = self.request.GET.get("note")
            ricetta_per_pelli = self.request.GET.get("ricetta_per_pelli")

            # Inizializza i campi del form con i valori recuperati
            initial["numero_ricetta"] = numero_ricetta
            initial["data_ricetta"] = data_ricetta
            initial["fk_articolo"] = fk_articolo
            initial["numero_revisione"] = numero_revisione
            initial["data_revisione"] = data_revisione
            initial["note"] = note
            initial["ricetta_per_pelli"] = ricetta_per_pelli
            initial["created_by"] = self.request.user

        else:
            initial["created_by"] = self.request.user
            initial["ricetta_per_pelli"] = 100
        print(f"Initial: {initial}")
        return initial


class RicettaRifinizioneUpdateView(LoginRequiredMixin, UpdateView):
    model = RicettaRifinizione
    form_class = RicettaRifinizioneModelForm
    template_name = "ricette/ricetta_rifinizione.html"
    success_message = "Ricetta modificata correttamente!"

    def get_success_url(self):
        if "salva_esci" in self.request.POST:
            return reverse_lazy("ricette:home_ricette_rifinizione")

        pk_ricetta = self.object.pk
        return reverse_lazy(
            "ricette:modifica_ricetta_rifinizione", kwargs={"pk": pk_ricetta}
        )

    def form_valid(self, form):
        messages.info(self.request, self.success_message)  # Compare sul success_url
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk_ricetta_rifinizione = self.object.pk
        if "focus_button" in self.kwargs:
            focus_button_param = self.kwargs[
                "focus_button"
            ]  # Leggo kwargs se c'è l'id del pulsante in cui mettere il focus
            print(f"focus_button_param: {focus_button_param}")
            context["focus_button"] = focus_button_param

        context["elenco_dettagli"] = DettaglioRicettaRifinizione.objects.filter(
            fk_ricetta_rifinizione=pk_ricetta_rifinizione
        )

        return context


def delete_ricetta_rifinizione(request, pk):
    deleteobject = get_object_or_404(RicettaRifinizione, pk=pk)
    deleteobject.delete()
    url_match = reverse_lazy("ricette:home_ricette_rifinizione")
    return redirect(url_match)


# Dettaglio
class DettaglioRicettaRifinizioneCreateView(LoginRequiredMixin, CreateView):
    model = DettaglioRicettaRifinizione
    form_class = DettaglioRicettaRifinizioneModelForm
    template_name = "ricette/dettaglio_ricetta_rifinizione.html"
    success_message = "Dettaglio aggiunto correttamente!"

    def get_success_url(self):
        fk_ricetta_rifinizione = self.object.fk_ricetta_rifinizione.pk
        focus_button = "btn_new_detail"  # Imposto il pulsante su cui settare il focus

        return reverse_lazy(
            "ricette:modifica_dettaglio_ricetta_rifinizione_with_focus_button",
            kwargs={"pk": fk_ricetta_rifinizione, "focus_button": focus_button},
        )
        # return reverse_lazy('ricette:modifica_ricetta_rifinizione', kwargs={'pk':fk_ricetta_rifinizione})

    def form_valid(self, form):
        messages.info(self.request, self.success_message)  # Compare sul success_url
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        ricetta_id = self.kwargs.get("fk_ricetta_rifinizione")
        max_numero_riga = DettaglioRicettaRifinizione.objects.filter(
            fk_ricetta_rifinizione=ricetta_id
        ).aggregate(models.Max("numero_riga"))["numero_riga__max"]
        next_numero_riga = max_numero_riga + 1 if max_numero_riga else 1
        initial["numero_riga"] = next_numero_riga

        ricetta_id = self.kwargs.get("fk_ricetta_rifinizione")

        initial["fk_ricetta_rifinizione"] = ricetta_id
        initial["created_by"] = self.request.user
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk_ricetta = self.kwargs["fk_ricetta_rifinizione"]
        context["ricetta_rifinizione"] = pk_ricetta
        context["dettagli_ricetta"] = get_object_or_404(
            RicettaRifinizione, pk=pk_ricetta
        )
        return context


class DettaglioRicettaRifinizioneUpdateView(LoginRequiredMixin, UpdateView):
    model = DettaglioRicettaRifinizione
    form_class = DettaglioRicettaRifinizioneModelForm
    template_name = "ricette/dettaglio_ricetta_rifinizione.html"
    success_message = "Dettaglio modificato correttamente!"

    def get_success_url(self):
        fk_ricetta_rifinizione = self.object.fk_ricetta_rifinizione.pk
        return reverse_lazy(
            "ricette:modifica_ricetta_rifinizione",
            kwargs={"pk": fk_ricetta_rifinizione},
        )

    def form_valid(self, form):
        messages.info(self.request, self.success_message)  # Compare sul success_url
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk_ricetta = self.kwargs["fk_ricetta_rifinizione"]
        context["ricetta_rifinizione"] = pk_ricetta
        context["dettagli_ricetta"] = get_object_or_404(
            RicettaRifinizione, pk=pk_ricetta
        )
        return context


def delete_dettaglio_ricetta_rifinizione(request, pk):
    deleteobject = get_object_or_404(DettaglioRicettaRifinizione, pk=pk)
    fk_ricetta_rifinizione = deleteobject.fk_ricetta_rifinizione.pk
    deleteobject.delete()
    url_match = reverse_lazy(
        "ricette:modifica_ricetta_rifinizione", kwargs={"pk": fk_ricetta_rifinizione}
    )
    return redirect(url_match)


# RICETTE COLORE RIFINIZIONE
class RicettaColoreRifinizioneCreateView(LoginRequiredMixin, CreateView):
    model = RicettaColoreRifinizione
    form_class = RicettaColoreRifinizioneModelForm
    template_name = "ricette/ricetta_colore_rifinizione.html"
    success_message = "Ricetta aggiunta correttamente!"

    def get_success_url(self):
        if "salva_esci" in self.request.POST:
            return reverse_lazy("ricette:home_ricette_colori_rifinizione")

        pk_ricetta = self.object.pk
        return reverse_lazy(
            "ricette:modifica_ricetta_colore_rifinizione", kwargs={"pk": pk_ricetta}
        )

    def form_valid(self, form):
        if "salva_esci" in self.request.POST:
            return redirect("ricette:home_ricette_colori_rifinizione")
        else:
            form.instance.created_by = self.request.user
            messages.info(self.request, self.success_message)
            return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()

        if self.request.GET.get("numero_ricetta"):
            fk_articolo = self.request.GET.get("fk_articolo")
            fk_colore = self.request.GET.get("fk_colore")
            last_recipe = (
                RicettaColoreRifinizione.objects.filter(
                    fk_articolo=fk_articolo, fk_colore=fk_colore
                )
                .order_by("-numero_revisione")
                .first()
            )
            numero_revisione = last_recipe.numero_revisione + 1
            numero_ricetta = self.request.GET.get("numero_ricetta")
            data_ricetta = self.request.GET.get("data_ricetta")
            numero_revisione = numero_revisione
            data_revisione = self.request.GET.get("data_revisione")
            note = self.request.GET.get("note")

            # Inizializza i campi del form con i valori recuperati
            initial["numero_ricetta"] = numero_ricetta
            initial["data_ricetta"] = data_ricetta
            initial["fk_articolo"] = fk_articolo
            initial["fk_colore"] = fk_colore
            initial["numero_revisione"] = numero_revisione
            initial["data_revisione"] = data_revisione
            initial["note"] = note
            initial["created_by"] = self.request.user

        else:
            ultima_ricetta = (
                RicettaColoreRifinizione.objects.all()
                .order_by("-numero_ricetta")
                .first()
            )
            data_odierna = date.today()
            if ultima_ricetta:
                initial["numero_ricetta"] = ultima_ricetta.numero_ricetta + 1
            else:
                # Nessuna ultima ricetta trovata, quindi impostare il numero di ricetta iniziale a 1 o a un altro valore predefinito
                initial["numero_ricetta"] = 1

            initial["data_ricetta"] = data_odierna
            initial["numero_revisione"] = 1
            initial["data_revisione"] = data_odierna
            initial["created_by"] = self.request.user

        return initial


class RicettaColoreRifinizioneUpdateView(LoginRequiredMixin, UpdateView):
    model = RicettaColoreRifinizione
    form_class = RicettaColoreRifinizioneModelForm
    template_name = "ricette/ricetta_colore_rifinizione.html"
    success_message = "Ricetta modificata correttamente!"

    def get_success_url(self):
        if "salva_esci" in self.request.POST:
            return reverse_lazy("ricette:home_ricette_colori_rifinizione")

        pk_ricetta = self.object.pk
        return reverse_lazy(
            "ricette:modifica_ricetta_colore_rifinizione", kwargs={"pk": pk_ricetta}
        )

    def form_valid(self, form):
        messages.info(self.request, self.success_message)  # Compare sul success_url
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk_ricetta_colore_rifinizione = self.object.pk
        if "focus_button" in self.kwargs:
            focus_button_param = self.kwargs[
                "focus_button"
            ]  # Leggo kwargs se c'è l'id del pulsante in cui mettere il focus
            context["focus_button"] = focus_button_param
        context["elenco_dettagli"] = DettaglioRicettaColoreRifinizione.objects.filter(
            fk_ricetta_colore_rifinizione=pk_ricetta_colore_rifinizione
        )

        return context


def delete_ricetta_colore_rifinizione(request, pk):
    deleteobject = get_object_or_404(RicettaColoreRifinizione, pk=pk)
    deleteobject.delete()
    url_match = reverse_lazy("ricette:home_ricette_colori_rifinizione")
    return redirect(url_match)


# Dettaglio
class DettaglioRicettaColoreRifinizioneCreateView(LoginRequiredMixin, CreateView):
    model = DettaglioRicettaColoreRifinizione
    form_class = DettaglioRicettaColoreRifinizioneModelForm
    template_name = "ricette/dettaglio_ricetta_colore_rifinizione.html"
    success_message = "Dettaglio aggiunto correttamente!"

    def get_success_url(self):
        fk_ricetta_colore_rifinizione = self.object.fk_ricetta_colore_rifinizione.pk
        focus_button = "btn_new_detail"  # Imposto il pulsante su cui settare il focus

        return reverse_lazy(
            "ricette:modifica_ricetta_colore_rifinizione_with_focus_button",
            kwargs={"pk": fk_ricetta_colore_rifinizione, "focus_button": focus_button},
        )

        # return reverse_lazy('ricette:modifica_ricetta_colore_rifinizione', kwargs={'pk':fk_ricetta_colore_rifinizione})

    def form_valid(self, form):
        messages.info(self.request, self.success_message)  # Compare sul success_url
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        ricetta_id = self.kwargs.get("fk_ricetta_colore_rifinizione")
        max_numero_riga = DettaglioRicettaColoreRifinizione.objects.filter(
            fk_ricetta_colore_rifinizione=ricetta_id
        ).aggregate(models.Max("numero_riga"))["numero_riga__max"]
        next_numero_riga = max_numero_riga + 1 if max_numero_riga else 1
        initial["numero_riga"] = next_numero_riga

        ricetta_id = self.kwargs.get("fk_ricetta_colore_rifinizione")

        initial["fk_ricetta_colore_rifinizione"] = ricetta_id
        initial["created_by"] = self.request.user
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for key, value in kwargs.items():
            print(f"{key}: {value}")
        pk_ricetta = self.kwargs["fk_ricetta_colore_rifinizione"]

        context["ricetta_colore_rifinizione"] = pk_ricetta
        context["dettagli_ricetta"] = get_object_or_404(
            RicettaColoreRifinizione, pk=pk_ricetta
        )
        return context


class DettaglioRicettaColoreRifinizioneUpdateView(LoginRequiredMixin, UpdateView):
    model = DettaglioRicettaColoreRifinizione
    form_class = DettaglioRicettaColoreRifinizioneModelForm
    template_name = "ricette/dettaglio_ricetta_colore_rifinizione.html"
    success_message = "Dettaglio modificato correttamente!"

    def get_success_url(self):
        fk_ricetta_colore_rifinizione = self.object.fk_ricetta_colore_rifinizione.pk
        return reverse_lazy(
            "ricette:modifica_ricetta_colore_rifinizione",
            kwargs={"pk": fk_ricetta_colore_rifinizione},
        )

    def form_valid(self, form):
        messages.info(self.request, self.success_message)  # Compare sul success_url
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk_ricetta = self.kwargs["fk_ricetta_colore_rifinizione"]
        context["ricetta_colore_rifinizione"] = pk_ricetta
        context["dettagli_ricetta"] = get_object_or_404(
            RicettaColoreRifinizione, pk=pk_ricetta
        )
        return context


def delete_dettaglio_ricetta_colore_rifinizione(request, pk):
    deleteobject = get_object_or_404(DettaglioRicettaColoreRifinizione, pk=pk)
    fk_ricetta_colore_rifinizione = deleteobject.fk_ricetta_colore_rifinizione.pk
    deleteobject.delete()
    url_match = reverse_lazy(
        "ricette:modifica_ricetta_colore_rifinizione",
        kwargs={"pk": fk_ricetta_colore_rifinizione},
    )
    return redirect(url_match)


# RICETTE BAGNATO


class RicettaBagnatoCreateView(LoginRequiredMixin, CreateView):
    model = RicettaBagnato
    form_class = RicettaBagnatoModelForm
    template_name = "ricette/ricetta_bagnato.html"
    success_message = "Ricetta aggiunta correttamente!"

    def get_success_url(self):
        if "salva_esci" in self.request.POST:
            return reverse_lazy("ricette:home_ricette_bagnato")

        pk_ricetta = self.object.pk
        return reverse_lazy(
            "ricette:modifica_ricetta_bagnato", kwargs={"pk": pk_ricetta}
        )

    def form_valid(self, form):
        if "salva_esci" in self.request.POST:
            return redirect("ricette:home_ricette_bagnato")
        else:
            form.instance.created_by = self.request.user
            messages.info(self.request, self.success_message)
            return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        if self.request.GET.get("numero_ricetta"):
            print(f"Articolo: ")
            fk_articolo = self.request.GET.get("fk_articolo")
            fk_tipogrezzo = self.request.GET.get("fk_tipogrezzo")
            fk_tipoanimale = self.request.GET.get("fk_tipoanimale")
            last_recipe = (
                RicettaBagnato.objects.filter(
                    fk_articolo=fk_articolo,
                    fk_tipogrezzo=fk_tipogrezzo,
                    fk_tipoanimale=fk_tipoanimale,
                )
                .order_by("-numero_revisione")
                .first()
            )

            numero_revisione = last_recipe.numero_revisione + 1
            numero_ricetta = self.request.GET.get("numero_ricetta")
            data_ricetta = self.request.GET.get("data_ricetta")
            numero_revisione = numero_revisione
            data_revisione = self.request.GET.get("data_revisione")

            note = self.request.GET.get("note")
            kg_ricetta = self.request.GET.get("kg_ricetta")

            # Inizializza i campi del form con i valori recuperati
            initial["numero_ricetta"] = numero_ricetta
            initial["data_ricetta"] = data_ricetta
            initial["fk_articolo"] = fk_articolo
            initial["numero_revisione"] = numero_revisione
            initial["data_revisione"] = data_revisione
            initial["fk_tipogrezzo"] = fk_tipogrezzo
            initial["fk_tipoanimale"] = fk_tipoanimale
            initial["note"] = note
            initial["kg_ricetta"] = kg_ricetta
            initial["created_by"] = self.request.user

        else:
            data_odierna = date.today()
            last_recipe = (
                RicettaBagnato.objects.all().order_by("-numero_ricetta").first()
            )
            if last_recipe:
                initial["numero_ricetta"] = last_recipe.numero_ricetta + 1
            else:
                initial["numero_ricetta"] = 1

            initial["data_ricetta"] = data_odierna
            initial["numero_revisione"] = 1
            initial["data_revisione"] = data_odierna
            initial["created_by"] = self.request.user
            initial["kg_ricetta"] = 100
        print(f"Initial: {initial}")
        return initial


class RicettaBagnatoUpdateView(LoginRequiredMixin, UpdateView):
    model = RicettaBagnato
    form_class = RicettaBagnatoModelForm
    template_name = "ricette/ricetta_bagnato.html"
    success_message = "Ricetta modificata correttamente!"

    def get_success_url(self):
        if "salva_esci" in self.request.POST:
            return reverse_lazy("ricette:home_ricette_bagnato")

        pk_ricetta = self.object.pk
        return reverse_lazy(
            "ricette:modifica_ricetta_bagnato", kwargs={"pk": pk_ricetta}
        )

    def form_valid(self, form):
        messages.info(self.request, self.success_message)  # Compare sul success_url
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk_ricetta_bagnato = self.object.pk
        context["elenco_dettagli"] = DettaglioRicettaBagnato.objects.filter(
            fk_ricetta_bagnato=pk_ricetta_bagnato
        )

        return context


def delete_ricetta_bagnato(request, pk):
    deleteobject = get_object_or_404(RicettaBagnato, pk=pk)
    print("Sto cancellando!!!")
    deleteobject.delete()
    url_match = reverse_lazy("ricette:home_ricette_bagnato")
    return redirect(url_match)


# Dettaglio
class DettaglioRicettaBagnatoCreateView(LoginRequiredMixin, CreateView):
    model = DettaglioRicettaBagnato
    form_class = DettaglioRicettaBagnatoModelForm
    template_name = "ricette/dettaglio_ricetta_bagnato.html"
    success_message = "Dettaglio aggiunto correttamente!"

    def get_success_url(self):
        fk_ricetta_bagnato = self.object.fk_ricetta_bagnato.pk
        return reverse_lazy(
            "ricette:modifica_ricetta_bagnato", kwargs={"pk": fk_ricetta_bagnato}
        )

    def form_valid(self, form):
        messages.info(self.request, self.success_message)  # Compare sul success_url
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        ricetta_id = self.kwargs.get("fk_ricetta_bagnato")
        max_numero_riga = DettaglioRicettaBagnato.objects.filter(
            fk_ricetta_bagnato=ricetta_id
        ).aggregate(models.Max("numero_riga"))["numero_riga__max"]
        next_numero_riga = max_numero_riga + 1 if max_numero_riga else 1
        print(f"next_numero_riga: {next_numero_riga}")
        initial["numero_riga"] = next_numero_riga
        ricetta_id = self.kwargs.get("fk_ricetta_bagnato")
        initial["fk_ricetta_bagnato"] = ricetta_id
        initial["created_by"] = self.request.user
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk_ricetta = self.kwargs["fk_ricetta_bagnato"]
        context["ricetta_bagnato"] = pk_ricetta
        context["dettagli_ricetta"] = get_object_or_404(RicettaBagnato, pk=pk_ricetta)
        return context


class DettaglioRicettaBagnatoUpdateView(LoginRequiredMixin, UpdateView):
    model = DettaglioRicettaBagnato
    form_class = DettaglioRicettaBagnatoModelForm
    template_name = "ricette/dettaglio_ricetta_bagnato.html"
    success_message = "Dettaglio modificato correttamente!"

    def get_success_url(self):
        fk_ricetta_bagnato = self.object.fk_ricetta_bagnato.pk
        return reverse_lazy(
            "ricette:modifica_ricetta_bagnato", kwargs={"pk": fk_ricetta_bagnato}
        )

    def form_valid(self, form):
        messages.info(self.request, self.success_message)  # Compare sul success_url
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk_ricetta = self.kwargs["fk_ricetta_bagnato"]
        context["ricetta_bagnato"] = pk_ricetta
        context["dettagli_ricetta"] = get_object_or_404(RicettaBagnato, pk=pk_ricetta)
        return context


def delete_dettaglio_ricetta_bagnato(request, pk):
    deleteobject = get_object_or_404(DettaglioRicettaBagnato, pk=pk)
    fk_ricetta_bagnato = deleteobject.fk_ricetta_bagnato.pk
    deleteobject.delete()
    url_match = reverse_lazy(
        "ricette:modifica_ricetta_bagnato", kwargs={"pk": fk_ricetta_bagnato}
    )
    return redirect(url_match)


# RICETTE COLORE BAGNATO
class RicettaColoreBagnatoCreateView(LoginRequiredMixin, CreateView):
    model = RicettaColoreBagnato
    form_class = RicettaColoreBagnatoModelForm
    template_name = "ricette/ricetta_colore_bagnato.html"
    success_message = "Ricetta aggiunta correttamente!"

    def get_success_url(self):
        if "salva_esci" in self.request.POST:
            return reverse_lazy("ricette:home_ricette_colori_bagnato")

        pk_ricetta = self.object.pk
        return reverse_lazy(
            "ricette:modifica_ricetta_colore_bagnato", kwargs={"pk": pk_ricetta}
        )

    def form_valid(self, form):
        if "salva_esci" in self.request.POST:
            return redirect("ricette:home_ricette_colori_bagnato")
        else:
            form.instance.created_by = self.request.user
            messages.info(self.request, self.success_message)
            return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()

        if self.request.GET.get("numero_ricetta"):
            fk_articolo = self.request.GET.get("fk_articolo")
            fk_colore = self.request.GET.get("fk_colore")
            last_recipe = (
                RicettaColoreBagnato.objects.filter(
                    fk_articolo=fk_articolo, fk_colore=fk_colore
                )
                .order_by("-numero_revisione")
                .first()
            )
            numero_revisione = last_recipe.numero_revisione + 1
            numero_ricetta = self.request.GET.get("numero_ricetta")
            data_ricetta = self.request.GET.get("data_ricetta")
            numero_revisione = numero_revisione
            data_revisione = self.request.GET.get("data_revisione")
            note = self.request.GET.get("note")

            # Inizializza i campi del form con i valori recuperati
            initial["numero_ricetta"] = numero_ricetta
            initial["data_ricetta"] = data_ricetta
            initial["fk_articolo"] = fk_articolo
            initial["fk_colore"] = fk_colore
            initial["numero_revisione"] = numero_revisione
            initial["data_revisione"] = data_revisione
            initial["note"] = note
            initial["created_by"] = self.request.user

        else:
            ultima_ricetta = (
                RicettaColoreBagnato.objects.all().order_by("-numero_ricetta").first()
            )
            data_odierna = date.today()
            if ultima_ricetta:
                initial["numero_ricetta"] = ultima_ricetta.numero_ricetta + 1
            else:
                # Nessuna ultima ricetta trovata, quindi impostare il numero di ricetta iniziale a 1 o a un altro valore predefinito
                initial["numero_ricetta"] = 1

            initial["data_ricetta"] = data_odierna
            initial["numero_revisione"] = 1
            initial["data_revisione"] = data_odierna
            initial["created_by"] = self.request.user

        return initial


class RicettaColoreBagnatoUpdateView(LoginRequiredMixin, UpdateView):
    model = RicettaColoreBagnato
    form_class = RicettaColoreBagnatoModelForm
    template_name = "ricette/ricetta_colore_bagnato.html"
    success_message = "Ricetta modificata correttamente!"

    def get_success_url(self):
        if "salva_esci" in self.request.POST:
            return reverse_lazy("ricette:home_ricette_colori_bagnato")

        pk_ricetta = self.object.pk
        return reverse_lazy(
            "ricette:modifica_ricetta_colore_bagnato", kwargs={"pk": pk_ricetta}
        )

    def form_valid(self, form):
        messages.info(self.request, self.success_message)  # Compare sul success_url
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk_ricetta_colore_bagnato = self.object.pk
        numero_ricetta_colore_bagnato = self.object.numero_ricetta
        if "focus_button" in self.kwargs:
            focus_button_param = self.kwargs[
                "focus_button"
            ]  # Leggo kwargs se c'è l'id del pulsante in cui mettere il focus
            context["focus_button"] = focus_button_param
        context["elenco_dettagli"] = DettaglioRicettaColoreBagnato.objects.filter(
            fk_ricetta_colore_bagnato=pk_ricetta_colore_bagnato
        )
        context["xr_fondi_colori"] = XRFondoColore.objects.filter(
            numero_ricetta=numero_ricetta_colore_bagnato
        )

        return context


def delete_ricetta_colore_bagnato(request, pk):
    deleteobject = get_object_or_404(RicettaColoreBagnato, pk=pk)

    # Trova tutte le istanze di XRFondoColore con lo stesso numero_ricetta
    XRFondoColore.objects.filter(numero_ricetta=deleteobject.numero_ricetta).delete()

    deleteobject.delete()
    url_match = reverse_lazy("ricette:home_ricette_colori_bagnato")
    return redirect(url_match)


# Dettaglio
class DettaglioRicettaColoreBagnatoCreateView(LoginRequiredMixin, CreateView):
    model = DettaglioRicettaColoreBagnato
    form_class = DettaglioRicettaColoreBagnatoModelForm
    template_name = "ricette/dettaglio_ricetta_colore_bagnato.html"
    success_message = "Dettaglio aggiunto correttamente!"

    def get_success_url(self):
        fk_ricetta_colore_bagnato = self.object.fk_ricetta_colore_bagnato.pk
        focus_button = "btn_new_detail"  # Imposto il pulsante su cui settare il focus

        return reverse_lazy(
            "ricette:modifica_ricetta_colore_bagnato_with_focus_button",
            kwargs={"pk": fk_ricetta_colore_bagnato, "focus_button": focus_button},
        )

        # return reverse_lazy('ricette:modifica_ricetta_colore_rifinizione', kwargs={'pk':fk_ricetta_colore_rifinizione})

    def form_valid(self, form):
        messages.info(self.request, self.success_message)  # Compare sul success_url
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        ricetta_id = self.kwargs.get("fk_ricetta_colore_bagnato")
        max_numero_riga = DettaglioRicettaColoreBagnato.objects.filter(
            fk_ricetta_colore_bagnato=ricetta_id
        ).aggregate(models.Max("numero_riga"))["numero_riga__max"]
        next_numero_riga = max_numero_riga + 1 if max_numero_riga else 1
        initial["numero_riga"] = next_numero_riga

        ricetta_id = self.kwargs.get("fk_ricetta_colore_bagnato")

        initial["fk_ricetta_colore_bagnato"] = ricetta_id
        initial["created_by"] = self.request.user
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for key, value in kwargs.items():
            print(f"{key}: {value}")
        pk_ricetta = self.kwargs["fk_ricetta_colore_bagnato"]

        context["ricetta_colore_bagnato"] = pk_ricetta
        context["dettagli_ricetta"] = get_object_or_404(
            RicettaColoreBagnato, pk=pk_ricetta
        )
        return context


class DettaglioRicettaColoreBagnatoUpdateView(LoginRequiredMixin, UpdateView):
    model = DettaglioRicettaColoreBagnato
    form_class = DettaglioRicettaColoreBagnatoModelForm
    template_name = "ricette/dettaglio_ricetta_colore_bagnato.html"
    success_message = "Dettaglio modificato correttamente!"

    def get_success_url(self):
        fk_ricetta_colore_bagnato = self.object.fk_ricetta_colore_bagnato.pk
        return reverse_lazy(
            "ricette:modifica_ricetta_colore_bagnato",
            kwargs={"pk": fk_ricetta_colore_bagnato},
        )

    def form_valid(self, form):
        messages.info(self.request, self.success_message)  # Compare sul success_url
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk_ricetta = self.kwargs["fk_ricetta_colore_bagnato"]
        context["ricetta_colore_bagnato"] = pk_ricetta
        context["dettagli_ricetta"] = get_object_or_404(
            RicettaColoreBagnato, pk=pk_ricetta
        )
        return context


def delete_dettaglio_ricetta_colore_bagnato(request, pk):
    deleteobject = get_object_or_404(DettaglioRicettaColoreBagnato, pk=pk)
    fk_ricetta_colore_bagnato = deleteobject.fk_ricetta_colore_bagnato.pk
    deleteobject.delete()
    url_match = reverse_lazy(
        "ricette:modifica_ricetta_colore_bagnato",
        kwargs={"pk": fk_ricetta_colore_bagnato},
    )
    return redirect(url_match)


# XR Fondo Colore


class XRFondoColoreCreateView(LoginRequiredMixin, CreateView):
    model = XRFondoColore
    form_class = XRFondoColoreModelForm
    template_name = "ricette/xr_fondo_colore.html"
    success_message = "Colore associato correttamente!"

    def get_success_url(self):
        numero_ricetta = self.object.numero_ricetta
        focus_button = "btn_new_assoc"  # Imposto il pulsante su cui settare il focus

        return reverse_lazy(
            "ricette:modifica_ricetta_colore_bagnato_with_focus_button",
            kwargs={"pk": numero_ricetta, "focus_button": focus_button},
        )

        # return reverse_lazy('ricette:modifica_ricetta_colore_rifinizione', kwargs={'pk':fk_ricetta_colore_rifinizione})

    def form_valid(self, form):
        messages.info(self.request, self.success_message)  # Compare sul success_url
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        numero_ricetta = self.kwargs.get("numero_ricetta")
        # print(f"Numero Ricetta Initial: {numero_ricetta}")
        initial["numero_ricetta"] = numero_ricetta
        initial["created_by"] = self.request.user
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for key, value in kwargs.items():
            print(f"{key}: {value}")
        pk_ricetta = self.kwargs["numero_ricetta"]
        # print(f"Numero Ricetta context: {pk_ricetta}")

        context["ricetta_colore_bagnato"] = pk_ricetta
        # context['dettagli_ricetta'] = get_object_or_404(RicettaColoreBagnato, pk=pk_ricetta)
        return context


class XRFondoColoreUpdateView(LoginRequiredMixin, UpdateView):
    model = XRFondoColore
    form_class = XRFondoColoreModelForm
    template_name = "ricette/xr_fondo_colore.html"
    success_message = "Associazione modificata correttamente!"

    def get_success_url(self):
        numero_ricetta = self.object.numero_ricetta
        return reverse_lazy(
            "ricette:modifica_ricetta_colore_bagnato", kwargs={"pk": numero_ricetta}
        )

    def form_valid(self, form):
        messages.info(self.request, self.success_message)  # Compare sul success_url
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk_ricetta = self.kwargs["numero_ricetta"]
        context["ricetta_colore_bagnato"] = pk_ricetta
        context["dettagli_ricetta"] = get_object_or_404(
            RicettaColoreBagnato, pk=pk_ricetta
        )
        return context


def delete_xr_fondo_colore(request, pk):
    deleteobject = get_object_or_404(XRFondoColore, pk=pk)
    numero_ricetta = deleteobject.numero_ricetta
    deleteobject.delete()
    url_match = reverse_lazy(
        "ricette:modifica_ricetta_colore_bagnato", kwargs={"pk": numero_ricetta}
    )
    return redirect(url_match)

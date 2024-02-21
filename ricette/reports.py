from django.shortcuts import get_object_or_404, redirect, render

from .models import *


def ricetta_rifinizione_print(request, pk):
    ricetta = get_object_or_404(RicettaRifinizione, pk=pk)
    dettaglio_ricetta = DettaglioRicettaRifinizione.objects.filter(pk=pk)
    
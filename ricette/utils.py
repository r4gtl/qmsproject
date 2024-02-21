import json

from chem_man.models import ProdottoChimico
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import RequestContext
from django.template.loader import get_template, render_to_string

from .models import DettaglioRicettaRifinizione


def search_prodotto_chimico(request):
    search_term = request.GET.get('search', '')
    if search_term:
        # Effettua la ricerca dei prodotti chimici
        prodotti_chimici = ProdottoChimico.objects.filter(
            Q(descrizione__icontains=search_term)
        )
        # Costruisci il markup HTML per la tabella dei risultati della ricerca
        results_html = "<table class='table'><thead><tr><th>ID</th><th>Descrizione</th><th>Fornitore</th></tr></thead><tbody>"
        for prodotto in prodotti_chimici:
            results_html += f"<tr data-id='{prodotto.pk}'><td class='prodotto-id'>{prodotto.pk}</td><td class='prodotto-descrizione'>{prodotto.descrizione}</td><td>{prodotto.fk_fornitore}</td></tr>"
        results_html += "</tbody></table>"
        
        return JsonResponse({'html': results_html})
    else:
        return JsonResponse({'html': ''})




'''
def search_prodotto_chimico(request):
    search_term = request.GET.get('search', '')
    if search_term:
        # Dividi il termine di ricerca in singole parole
        search_terms = search_term.split()

        # Inizializza una lista vuota per i risultati
        prodotti_chimici = []

        # Effettua la ricerca dei prodotti chimici per ogni parola di ricerca
        for term in search_terms:
            prodotti_chimici += ProdottoChimico.objects.filter(descrizione__icontains=term)

        # Rimuovi i duplicati dalla lista dei risultati
        prodotti_chimici = list(set(prodotti_chimici))

        # Costruisci il markup HTML per la tabella dei risultati della ricerca
        results_html = "<table class='table'><thead><tr><th>ID</th><th>Descrizione</th><th>Fornitore</th></tr></thead><tbody>"
        for prodotto in prodotti_chimici:
            results_html += f"<tr data-id='{prodotto.pk}'><td class='prodotto-id'>{prodotto.pk}</td><td class='prodotto-descrizione'>{prodotto.descrizione}</td><td>{prodotto.fk_fornitore}</td></tr>"
        results_html += "</tbody></table>"
        print(f"results_html: {results_html}")
        return JsonResponse({'html': results_html})
    else:
        return JsonResponse({'html': ''})
        '''

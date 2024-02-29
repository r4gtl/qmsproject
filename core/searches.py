from articoli.models import Articolo, Colore
from chem_man.models import ProdottoChimico
from django.db.models import Q
from django.http import JsonResponse
from ricette.models import (RicettaBagnato, RicettaColoreRifinizione,
                            RicettaRifinizione)


def search_prodotto_chimico(request):
    search_term = request.GET.get('search', '')
    if search_term:
        # Effettua la ricerca dei prodotti chimici
        prodotti_chimici = ProdottoChimico.objects.filter(
            Q(descrizione__icontains=search_term)
        )
        # Costruisci il markup HTML per la tabella dei risultati della ricerca
        results_html = "<table class='table table-search'><thead><tr><th>ID</th><th>Descrizione</th><th>Fornitore</th></tr></thead><tbody>"
        for prodotto in prodotti_chimici:
            results_html += f"<tr data-id='{prodotto.pk}'><td class='prodotto-id'>{prodotto.pk}</td><td class='prodotto-descrizione'>{prodotto.descrizione}</td><td>{prodotto.fk_fornitore}</td></tr>"
        results_html += "</tbody></table>"
        
        return JsonResponse({'html': results_html})
    else:
        return JsonResponse({'html': ''})
    

def search_articolo(request):
    search_term = request.GET.get('search', '')
    if search_term:
        # Effettua la ricerca dell'Articolo
        articoli = Articolo.objects.filter(
            Q(descrizione__icontains=search_term)
        )
        # Costruisci il markup HTML per la tabella dei risultati della ricerca
        results_html = "<table class='table table-search'><thead><tr><th>ID</th><th>Descrizione</th></tr></thead><tbody>"
        for articolo in articoli:
            results_html += f"<tr data-id='{articolo.pk}'><td class='articolo-id'>{articolo.pk}</td><td class='articolo-descrizione'>{articolo.descrizione}</td></tr>"
        results_html += "</tbody></table>"
        
        return JsonResponse({'html': results_html})
    else:
        return JsonResponse({'html': ''})



def search_colore(request):
    search_term = request.GET.get('search', '')
    if search_term:
        # Effettua la ricerca dell'Articolo
        colori = Colore.objects.filter(
            Q(descrizione__icontains=search_term)
        )
        # Costruisci il markup HTML per la tabella dei risultati della ricerca
        results_html = "<table class='table table-search'><thead><tr><th>ID</th><th>Descrizione</th></tr></thead><tbody>"
        for colore in colori:
            results_html += f"<tr data-id='{colore.pk}'><td class='colore-id'>{colore.pk}</td><td class='colore-descrizione'>{colore.descrizione}</td></tr>"
        results_html += "</tbody></table>"
        
        return JsonResponse({'html': results_html})
    else:
        return JsonResponse({'html': ''})
    


def search_revisione_rifinizione(request):
    search_term = request.GET.get('search', '')
    if search_term:
        # Effettua la ricerca dei prodotti chimici
        ricette_rifinizione = RicettaRifinizione.objects.filter(
            Q(fk_articolo__descrizione__icontains=search_term)
        )
        # Costruisci il markup HTML per la tabella dei risultati della ricerca
        results_html = "<table class='table table-search'><thead><tr><th>ID</th><th>Articolo</th><th>Revisione N.</th><th>Data Revisione</th></tr></thead><tbody>"
        for ricetta in ricette_rifinizione:
            results_html += f"<tr data-id='{ricetta.pk}'><td class='ricetta-id'>{ricetta.pk}</td><td class='ricetta-articolo'>{ricetta.fk_articolo}</td><td class='ricetta-revisione'>{ricetta.numero_revisione}</td><td class='ricetta-revisione-data'>{ricetta.data_revisione}</td></tr>"
        results_html += "</tbody></table>"
        
        
        return JsonResponse({'html': results_html})
    else:
        return JsonResponse({'html': ''})
    


def search_revisione_colore_rifinizione(request):
    search_term = request.GET.get('search', '')
    if search_term:
        # Effettua la ricerca dei prodotti chimici
        ricette_colore_rifinizione = RicettaColoreRifinizione.objects.filter(
            Q(fk_articolo__descrizione__icontains=search_term)|
            Q(fk_colore__descrizione__icontains=search_term)
            )
        
        # Costruisci il markup HTML per la tabella dei risultati della ricerca
        results_html = "<table class='table table-search'><thead><tr><th>ID</th><th>Articolo</th><th>Colore</th><th>Revisione N.</th><th>Data Revisione</th></tr></thead><tbody>"
        for ricetta in ricette_colore_rifinizione:
            results_html += f"<tr data-id='{ricetta.pk}'><td class='ricetta-id'>{ricetta.pk}</td><td class='ricetta-articolo'>{ricetta.fk_articolo}</td><td class='ricetta-colore'>{ricetta.fk_colore}</td><td class='ricetta-revisione'>{ricetta.numero_revisione}</td><td class='ricetta-revisione-data'>{ricetta.data_revisione}</td></tr>"
        results_html += "</tbody></table>"
        
        
        return JsonResponse({'html': results_html})
    else:
        return JsonResponse({'html': ''})
    


def search_prodotto_chimico_rifinizione(request):
    search_term = request.GET.get('search', '')
    if search_term:
        prodotti_chimici_rifinizione = ProdottoChimico.objects.filter(
                Q(reparto='rifinizione') | Q(reparto__isnull=True)
            )
        
        # Effettua la ricerca dei prodotti chimici
        prodotti_chimici = prodotti_chimici_rifinizione.filter(
            Q(descrizione__icontains=search_term)
        )
        
        # Costruisci il markup HTML per la tabella dei risultati della ricerca
        results_html = "<table class='table table-search'><thead><tr><th>ID</th><th>Descrizione</th><th>Fornitore</th></tr></thead><tbody>"
        for prodotto in prodotti_chimici:
            results_html += f"<tr data-id='{prodotto.pk}'><td class='prodotto-id'>{prodotto.pk}</td><td class='prodotto-descrizione'>{prodotto.descrizione}</td><td>{prodotto.fk_fornitore}</td></tr>"
        results_html += "</tbody></table>"
        
        return JsonResponse({'html': results_html})
    else:
        return JsonResponse({'html': ''})
    


def search_revisione_bagnato(request):
    search_term = request.GET.get('search', '')
    if search_term:
        # Effettua la ricerca dei prodotti chimici
        ricette_bagnato = RicettaBagnato.objects.filter(
            Q(fk_articolo__descrizione__icontains=search_term)
        )
        # Costruisci il markup HTML per la tabella dei risultati della ricerca
        results_html = "<table class='table table-search'><thead><tr><th>ID</th><th>Articolo</th><th>Revisione N.</th><th>Data Revisione</th></tr></thead><tbody>"
        for ricetta in ricette_bagnato:
            results_html += f"<tr data-id='{ricetta.pk}'><td class='ricetta-id'>{ricetta.pk}</td><td class='ricetta-articolo'>{ricetta.fk_articolo}</td><td class='ricetta-revisione'>{ricetta.numero_revisione}</td><td class='ricetta-revisione-data'>{ricetta.data_revisione}</td></tr>"
        results_html += "</tbody></table>"
        
        
        return JsonResponse({'html': results_html})
    else:
        return JsonResponse({'html': ''})
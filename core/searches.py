from articoli.models import Articolo
from chem_man.models import ProdottoChimico
from django.db.models import Q
from django.http import JsonResponse


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
        print(f"results_html: {results_html}")
        return JsonResponse({'html': results_html})
    else:
        return JsonResponse({'html': ''})
from django.http import JsonResponse
from django.views import View

from .models import (Sostanza, SostanzaSVHC, SimboloGHS,
                     ProdottoChimico, ImballaggioPC
)

from django.db.models import Q




# Serve per avere i dati per passare l'immagine del simbolo GHS da visualizzare al cambio di un campo 
# option
def get_symbol_image_url(request):
    fk_simbolo_ghs_id = request.GET.get('fk_simbolo_ghs_id')
    
    try:
        simbolo_ghs = SimboloGHS.objects.get(id=fk_simbolo_ghs_id)
        image_url = simbolo_ghs.symbol_image.url
        print("image_url: " + str(image_url))
        return JsonResponse({'success': True, 'image_url': image_url})
    except SimboloGHS.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Symbol GHS not found'})
    

def search_sostanza(request):
    term = request.GET.get('term', '')  # Valore di ricerca dalla query string
    results = []

    if term:
        query = Q(num_cas__icontains=term) | Q(num_ec__icontains=term)
        sostanze = Sostanza.objects.filter(query)[:10]

        for sostanza in sostanze:
            result = {
                'id': sostanza.id,
                'descrizione': sostanza.descrizione,
                'num_cas': sostanza.num_cas,
                'num_ec': sostanza.num_ec
            }
            print("Result: " + str(result))
            results.append(result)

    return JsonResponse(results, safe=False)



def get_sostanza_details(request):
    sostanza_id = request.GET.get('id')
    
    try:
        sostanza = Sostanza.objects.get(pk=sostanza_id)
    except Sostanza.DoesNotExist:
        return JsonResponse({'error': 'Sostanza non trovata'}, status=404)
    
    # Restituisci i dettagli dell'oggetto Sostanza
    data = {
        'id': sostanza.pk,
        'descrizione': sostanza.descrizione,
        'num_cas': sostanza.num_cas,
        'num_ec': sostanza.num_ec,
    }
    
    return JsonResponse(data)


def check_if_svhc(request):
    fk_sostanza_id = request.GET.get('fk_sostanza')
    exists = SostanzaSVHC.objects.filter(Q(num_cas=fk_sostanza_id) | Q(num_ec=fk_sostanza_id)).exists()
    return JsonResponse({'exists': exists})


# Funzione per poter filtrare gli imballaggi nel Dettaglio Ordine PC
def get_prodotto_chimico(request):
    product_id = request.GET.get('product_id')
    if product_id is not None:
        try:
            prodotto_chimico = ProdottoChimico.objects.get(pk=product_id)
            return JsonResponse({'fk_imballaggio': prodotto_chimico.fk_imballaggio.id})
        except ProdottoChimico.DoesNotExist:
            pass

    return JsonResponse({'error': 'Invalid request'})


# Ottenere l'ultimo prezzo quando si inserisce il dettaglio acquisto
def get_ultimo_prezzo(request):
    if request.method == 'GET':
        prodotto_id = request.GET.get('prodotto_id')
        try:
            # Recupera l'ultimo prezzo del prodotto associato dall'ID
            prezzo = ProdottoChimico.objects.get(pk=prodotto_id).ultimo_prezzo
            return JsonResponse({'ultimo_prezzo': prezzo})
        except ProdottoChimico.DoesNotExist:
            return JsonResponse({'ultimo_prezzo': None})
        
# Ottenere la percentuale di solvente 
def get_solvente(request):
    if request.method == 'GET':
        prodotto_id = request.GET.get('prodotto_id')
        try:
            # Recupera il valore del campo solvente del prodotto associato dall'ID
            solvente = ProdottoChimico.objects.get(pk=prodotto_id).solvente
            return JsonResponse({'solvente': solvente})
        except ProdottoChimico.DoesNotExist:
            return JsonResponse({'solvente': None})
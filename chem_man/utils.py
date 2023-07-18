from django.http import JsonResponse
from django.views import View

from .models import Sostanza, SostanzaSVHC, SimboloGHS

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
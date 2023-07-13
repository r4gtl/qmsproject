from django.http import JsonResponse
from .models import SimboloGHS



# Serve per avere i dati per passare l'immagine del simbolo GHS da visualizzare al cambio di un campo 
# option
def get_symbol_image_url(request):
    fk_simbolo_ghs_id = request.GET.get('fk_simbolo_ghs_id')
    
    try:
        simbolo_ghs = SimboloGHS.objects.get(id=fk_simbolo_ghs_id)
        image_url = simbolo_ghs.symbol_image.url
        return JsonResponse({'success': True, 'image_url': image_url})
    except SimboloGHS.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Symbol GHS not found'})

from django.http import JsonResponse
from.models import CodiceCER, CodiceSmaltRec


def get_descrizione_cer(request):
    codice_cer_id = request.GET.get('codice_cer_id')
    
    try:
        codice_cer = CodiceCER.objects.get(id=codice_cer_id)
        descrizione = codice_cer.descrizione
        return JsonResponse({'descrizione': descrizione})
    except CodiceCER.DoesNotExist:
        return JsonResponse({'descrizione': ''})
    
def get_descrizione_smaltrec(request):
    codice_smaltrec_id = request.GET.get('codice_smaltrec_id')
    
    try:
        codice_smaltrec = CodiceSmaltRec.objects.get(id=codice_smaltrec_id)
        descrizione = codice_smaltrec.descrizione
        return JsonResponse({'descrizione': descrizione})
    except CodiceCER.DoesNotExist:
        return JsonResponse({'descrizione': ''})
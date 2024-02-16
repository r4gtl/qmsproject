import json

from django.http import JsonResponse

from .models import DettaglioProcedura

'''13/02/2024 prova trascinamento riga tabella'''
def update_row_numbers(request):
    
    if request.method == 'POST': 
        data = json.loads(request.body)
        data_list = data['data']
        
        # Itera sui dati ricevuti e aggiorna i record nel database
        for item in data_list:            
            pk = item['pk']
            new_numero_riga = item['numero_riga']
            dettaglio = DettaglioProcedura.objects.get(pk=pk)
            dettaglio.numero_riga = new_numero_riga
            dettaglio.save()
        
        return JsonResponse({'message': 'Numeri di riga aggiornati con successo'}, status=200)
    
    else:        
        return JsonResponse({'error': 'Richiesta non valida'}, status=400)
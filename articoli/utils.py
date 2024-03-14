
from django.http import JsonResponse
from django.urls import reverse

from .models import DettaglioFaseLavoro, FaseLavoro


def accoda_dettaglio_fase_lavoro(request):
    if request.method == 'POST':
        fase_id = request.POST.get('fase_id')
        print(f"fase_id: {fase_id}")
        fase_attiva = request.POST.get('faseAttiva')    
        print(f"fase_attiva: {fase_attiva}")

        fase_attiva = FaseLavoro.objects.get(pk=fase_attiva) # Recupero l'istanza da passare alla FK
        # Filtro le istanze di DettaglioRicettaRifinizione in base a ricetta_id
        dettagli_fase = DettaglioFaseLavoro.objects.filter(fk_fase_lavoro=fase_id)

        # Duplico le istanze filtrate e modifico fk_ricetta_rifinizione
        for dettaglio in dettagli_fase:
            DettaglioFaseLavoro.objects.create(
                fk_fase_lavoro=fase_attiva,
                attributo=dettaglio.attributo,
                note=dettaglio.note,                
                created_by=dettaglio.created_by
            )
        
        redirect_url = reverse('articoli:modifica_fase_lavoro', kwargs={'pk': fase_attiva.pk})
        return JsonResponse({'redirect_url': redirect_url}) 
    else:
        return JsonResponse({'error': 'Richiesta non valida.'})



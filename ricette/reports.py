from django.db.models import F, OuterRef, Subquery, Sum
from django.shortcuts import get_object_or_404, render

from .models import *


def ricetta_rifinizione_print(request, pk):
    ricetta = get_object_or_404(RicettaRifinizione, pk=pk)
    dettagli_ricetta = DettaglioRicettaRifinizione.objects.filter(fk_ricetta_rifinizione=pk)
    # Sottquery per ottenere l'ultimo prezzo per ciascun prodotto chimico
    ultimi_prezzi = PrezzoProdotto.objects.filter(
        fk_prodottochimico=OuterRef('fk_prodotto_chimico')
    ).order_by('-data_inserimento').values('prezzo')[:1]

    # Raggruppa i dettagli per fk_operazione_ricette e calcola i totali per ogni gruppo
    dettagli_raggruppati = dettagli_ricetta.annotate(
        ultimo_prezzo=Subquery(ultimi_prezzi)
    ).values('fk_operazione_ricette').annotate(
        subtotale=Sum(F('quantity') * F('ultimo_prezzo')),        
        subquantity=Sum('quantity')
    )
    
    totale = sum(dettaglio['subtotale'] if dettaglio['subtotale'] is not None else 0 for dettaglio in dettagli_raggruppati)

    
    context = {
        'ricetta': ricetta,
        'dettagli_ricetta': dettagli_ricetta,
        'dettagli_raggruppati': dettagli_raggruppati,
        'totale': totale
        
    }
    return render(request, 'ricette/reports/ricetta_rifinizione_print.html', context)
    



def ricetta_colore_rifinizione_print(request, pk):
    ricetta = get_object_or_404(RicettaColoreRifinizione, pk=pk)
    dettagli_ricetta = DettaglioRicettaColoreRifinizione.objects.filter(fk_ricetta_colore_rifinizione=pk)
    # Sottquery per ottenere l'ultimo prezzo per ciascun prodotto chimico
    ultimi_prezzi = PrezzoProdotto.objects.filter(
        fk_prodottochimico=OuterRef('fk_prodotto_chimico')
    ).order_by('-data_inserimento').values('prezzo')[:1]

    # Raggruppa i dettagli per fk_operazione_ricette e calcola i totali per ogni gruppo
    dettagli_raggruppati = dettagli_ricetta.annotate(
        ultimo_prezzo=Subquery(ultimi_prezzi)
    ).values('fk_operazione_ricette').annotate(
        subtotale=Sum(F('quantity') * F('ultimo_prezzo')),        
        subquantity=Sum('quantity')
    )
    
    totale = sum(dettaglio['subtotale'] if dettaglio['subtotale'] is not None else 0 for dettaglio in dettagli_raggruppati)

    
    context = {
        'ricetta': ricetta,
        'dettagli_ricetta': dettagli_ricetta,
        'dettagli_raggruppati': dettagli_raggruppati,
        'totale': totale
        
    }
    return render(request, 'ricette/reports/ricetta_colore_rifinizione_print.html', context)



def ricetta_bagnato_print(request, pk):
    ricetta = get_object_or_404(RicettaBagnato, pk=pk)
    dettagli_ricetta = DettaglioRicettaBagnato.objects.filter(fk_ricetta_bagnato=pk)
    # Sottquery per ottenere l'ultimo prezzo per ciascun prodotto chimico
    ultimi_prezzi = PrezzoProdotto.objects.filter(
        fk_prodottochimico=OuterRef('fk_prodotto_chimico')
    ).order_by('-data_inserimento').values('prezzo')[:1]

    # Raggruppa i dettagli per fk_operazione_ricette e calcola i totali per ogni gruppo
    dettagli_raggruppati = dettagli_ricetta.annotate(
        ultimo_prezzo=Subquery(ultimi_prezzi)
    ).values('fk_operazione_ricette').annotate(
        subtotale=Sum(F('quantity') * F('ultimo_prezzo')),        
        subquantity=Sum('quantity')
    )
    
    totale = sum(dettaglio['subtotale'] if dettaglio['subtotale'] is not None else 0 for dettaglio in dettagli_raggruppati)

    
    context = {
        'ricetta': ricetta,
        'dettagli_ricetta': dettagli_ricetta,
        'dettagli_raggruppati': dettagli_raggruppati,
        'totale': totale
        
    }
    return render(request, 'ricette/reports/ricetta_bagnato_print.html', context)
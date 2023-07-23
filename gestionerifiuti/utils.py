from django.http import JsonResponse
from datetime import datetime
from decimal import Decimal
from django.db.models.functions import Coalesce
from django.db.models import Q, Sum, Value, IntegerField, DecimalField
from.models import CodiceCER, CodiceSmaltRec, MovimentoRifiuti



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
    
def somma_quantita_per_anno_smaltimento_recupero(tipo_movimento):
    current_year = datetime.now().year
    last_three_years = [current_year - i for i in range(1, 4)]

    # Filtra i movimenti per gli ultimi 3 anni escluso l'anno corrente e solo se il carico è "carico"
    movimenti_carico = MovimentoRifiuti.objects.filter(
        data_movimento__year__in=last_three_years,
        car_scar='carico',
        fk_smaltrec__smalt_rec=tipo_movimento  # Aggiungi il filtro per il tipo di movimento
    ).exclude(data_movimento__year=current_year)

    # Raggruppa i dati per "smaltimento" o "recupero" e anno di movimento
    dati_raggruppati = movimenti_carico.values('fk_smaltrec', 'data_movimento__year').annotate(
        totale_quantita=Coalesce(Sum('quantity', output_field=IntegerField()), 0)
    )
    
    # Crea un dizionario con le somme delle quantità divise per "smaltimento" e "recupero" e per anno
    risultato = {}
    for dato in dati_raggruppati:
        fk_smaltrec = dato['fk_smaltrec']
        anno_movimento = dato['data_movimento__year']
        totale_quantita = dato['totale_quantita']

        if fk_smaltrec not in risultato:
            risultato[fk_smaltrec] = {anno_movimento: totale_quantita}
            
        else:
            risultato[fk_smaltrec][anno_movimento] = totale_quantita
            
    
    for fk_smaltrec in risultato:
        for year in last_three_years:
            risultato[fk_smaltrec].setdefault(year, 0)
            
    # Ordina il risultato per la chiave dell'anno in modo crescente
    risultato_ordinato = {}
    for fk_smaltrec, dati_per_anno in risultato.items():
        risultato_ordinato[fk_smaltrec] = dict(sorted(dati_per_anno.items(), key=lambda x: x[0]))
    
    return risultato_ordinato
    
    

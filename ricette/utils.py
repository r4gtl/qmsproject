from .models import RicettaRifinizione, DettaglioRicettaRifinizione
from chem_man.models import ProdottoChimico
from django.db import models
from django.db.models import Sum



def calcola_totale_prezzi(id_ricetta_rifinizione):
    try:
        ricetta_rifinizione = RicettaRifinizione.objects.get(pk=id_ricetta_rifinizione)
        totale_prezzi = ProdottoChimico.objects.filter(
            dettaglio_ricette_rifinizione__fk_ricetta_rifinizione=ricetta_rifinizione
        ).aggregate(Sum('prezzo'))['prezzo__sum'] or 0.0
        return totale_prezzi
    except RicettaRifinizione.DoesNotExist:
        return 0.0
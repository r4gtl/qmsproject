from datetime import datetime

from chem_man.models import ProdottoChimico
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse

from .forms import RicettaRifinizioneModelForm
from .models import (DettaglioRicettaColoreRifinizione,
                     DettaglioRicettaRifinizione, RicettaColoreRifinizione,
                     RicettaRifinizione)


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



def search_revisione_rifinizione(request):
    search_term = request.GET.get('search', '')
    if search_term:
        # Effettua la ricerca dei prodotti chimici
        ricette_rifinizione = RicettaRifinizione.objects.filter(
            Q(fk_articolo__descrizione__icontains=search_term)
        )
        # Costruisci il markup HTML per la tabella dei risultati della ricerca
        results_html = "<table class='table table-search'><thead><tr><th>ID</th><th>Articolo</th><th>Revisione N.</th><th>Data Revisione</th></tr></thead><tbody>"
        for ricetta in ricette_rifinizione:
            results_html += f"<tr data-id='{ricetta.pk}'><td class='ricetta-id'>{ricetta.pk}</td><td class='ricetta-articolo'>{ricetta.fk_articolo}</td><td class='ricetta-revisione'>{ricetta.numero_revisione}</td><td class='ricetta-revisione-data'>{ricetta.data_revisione}</td></tr>"
        results_html += "</tbody></table>"
        
        
        return JsonResponse({'html': results_html})
    else:
        return JsonResponse({'html': ''})


'''
def search_prodotto_chimico(request):
    search_term = request.GET.get('search', '')
    if search_term:
        # Dividi il termine di ricerca in singole parole
        search_terms = search_term.split()

        # Inizializza una lista vuota per i risultati
        prodotti_chimici = []

        # Effettua la ricerca dei prodotti chimici per ogni parola di ricerca
        for term in search_terms:
            prodotti_chimici += ProdottoChimico.objects.filter(descrizione__icontains=term)

        # Rimuovi i duplicati dalla lista dei risultati
        prodotti_chimici = list(set(prodotti_chimici))

        # Costruisci il markup HTML per la tabella dei risultati della ricerca
        results_html = "<table class='table'><thead><tr><th>ID</th><th>Descrizione</th><th>Fornitore</th></tr></thead><tbody>"
        for prodotto in prodotti_chimici:
            results_html += f"<tr data-id='{prodotto.pk}'><td class='prodotto-id'>{prodotto.pk}</td><td class='prodotto-descrizione'>{prodotto.descrizione}</td><td>{prodotto.fk_fornitore}</td></tr>"
        results_html += "</tbody></table>"
        print(f"results_html: {results_html}")
        return JsonResponse({'html': results_html})
    else:
        return JsonResponse({'html': ''})
        '''

def new_finishing_revision(request):
    if request.method == 'POST':
        numero_ricetta = request.POST.get('numero_ricetta')
        data_ricetta = request.POST.get('data_ricetta')
        fk_articolo = request.POST.get('fk_articolo')
        note = request.POST.get('note')
        ricetta_per_pelli = request.POST.get('ricetta_per_pelli')
        
        print(f"numero_ricetta: {numero_ricetta}")
        print(f"data_ricetta: {data_ricetta}")
        print(f"fk_articolo: {fk_articolo}")
        print(f"note: {note}")
        print(f"ricetta_per_pelli: {ricetta_per_pelli}")
        # Esegui la logica per creare la nuova istanza della RicettaRifinizione
        # Ad esempio:
        ultima_ricetta = RicettaRifinizione.objects.filter(fk_articolo=fk_articolo).order_by('-numero_revisione').first()

        # Determina il nuovo numero di revisione
        if ultima_ricetta:
            nuovo_numero_revisione = ultima_ricetta.numero_revisione + 1
        else:
            nuovo_numero_revisione = 1  # Se non ci sono ricette precedenti, inizia con 1

        data_revisione = datetime.now().date()
        
        # Crea la nuova istanza della RicettaRifinizione
        nuova_ricetta = RicettaRifinizione.objects.create(
            numero_ricetta=numero_ricetta,
            data_ricetta=data_ricetta,
            numero_revisione=nuovo_numero_revisione,  # Assegna il nuovo numero di revisione
            data_revisione=data_revisione,
            note=note,
            fk_articolo=fk_articolo,
            ricetta_per_pelli=ricetta_per_pelli,
            # Altri campi della nuova istanza se necessario
        )

        # Invia una risposta JSON per indicare il successo
        return JsonResponse({'message': 'Nuova ricetta creata con successo!'})
    else:
        # Se la richiesta non è di tipo POST, restituisci un errore
        return JsonResponse({'error': 'Metodo non consentito'}, status=405)


def accoda_dettaglio_ricetta_rifinizione(request):
    if request.method == 'POST':
        ricetta_id = request.POST.get('ricetta_id')
        ricetta_attiva = request.POST.get('ricettaAttiva')
        print(f"ricetta_attiva: {ricetta_attiva}" )
        print(f"ricetta_id: {ricetta_id}" )
        ricetta_attiva = RicettaRifinizione.objects.get(pk=ricetta_attiva) # Recupero l'istanza da passare alla FK
        # Filtro le istanze di DettaglioRicettaRifinizione in base a ricetta_id
        dettagli_ricetta = DettaglioRicettaColoreRifinizione.objects.filter(fk_ricetta_rifinizione=ricetta_id)

        # Duplico le istanze filtrate e modifico fk_ricetta_rifinizione
        for dettaglio in dettagli_ricetta:
            DettaglioRicettaRifinizione.objects.create(
                fk_ricetta_rifinizione=ricetta_attiva,
                fk_operazione_ricette=dettaglio.fk_operazione_ricette,
                numero_riga=dettaglio.numero_riga,
                quantity=dettaglio.quantity,
                fk_prodotto_chimico=dettaglio.fk_prodotto_chimico,
                note=dettaglio.note,
                created_by=dettaglio.created_by
            )
        print(f"ricetta_attiva.pk: {ricetta_attiva.pk}")
        #return redirect(reverse('ricette:modifica_ricetta_rifinizione', kwargs={'pk': int(ricetta_attiva.pk)}))
        #return JsonResponse({'message': 'Dettagli della ricetta rifinizione aggiunti correttamente.'})
        redirect_url = reverse('ricette:modifica_ricetta_rifinizione', kwargs={'pk': ricetta_attiva.pk})
        return JsonResponse({'redirect_url': redirect_url}) 
    else:
        return JsonResponse({'error': 'Richiesta non valida.'})
    

def accoda_dettaglio_ricetta_colore_rifinizione(request):
    if request.method == 'POST':
        ricetta_id = request.POST.get('ricetta_id')
        ricetta_attiva = request.POST.get('ricettaAttiva')
        print(f"ricetta_attiva: {ricetta_attiva}" )
        print(f"ricetta_id: {ricetta_id}" )
        ricetta_attiva = RicettaColoreRifinizione.objects.get(pk=ricetta_attiva) # Recupero l'istanza da passare alla FK
        # Filtro le istanze di DettaglioRicettaRifinizione in base a ricetta_id
        dettagli_ricetta = DettaglioRicettaColoreRifinizione.objects.filter(fk_ricetta_colore_rifinizione=ricetta_id)

        # Duplico le istanze filtrate e modifico fk_ricetta_rifinizione
        for dettaglio in dettagli_ricetta:
            DettaglioRicettaColoreRifinizione.objects.create(
                fk_ricetta_colore_rifinizione=ricetta_attiva,
                fk_operazione_ricette=dettaglio.fk_operazione_ricette,
                numero_riga=dettaglio.numero_riga,
                quantity=dettaglio.quantity,
                fk_prodotto_chimico=dettaglio.fk_prodotto_chimico,
                note=dettaglio.note,
                created_by=dettaglio.created_by
            )
        print(f"ricetta_attiva.pk: {ricetta_attiva.pk}")
        #return redirect(reverse('ricette:modifica_ricetta_rifinizione', kwargs={'pk': int(ricetta_attiva.pk)}))
        #return JsonResponse({'message': 'Dettagli della ricetta rifinizione aggiunti correttamente.'})
        redirect_url = reverse('ricette:modifica_ricetta_rifinizione', kwargs={'pk': ricetta_attiva.pk})
        return JsonResponse({'redirect_url': redirect_url}) 
    else:
        return JsonResponse({'error': 'Richiesta non valida.'})
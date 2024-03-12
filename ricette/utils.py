from datetime import datetime

from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse

from .forms import RicettaRifinizioneModelForm
from .models import (DettaglioRicettaBagnato,
                     DettaglioRicettaColoreRifinizione,
                     DettaglioRicettaRifinizione, RicettaBagnato,
                     RicettaColoreRifinizione, RicettaRifinizione)


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
        ricetta_attiva = RicettaRifinizione.objects.get(pk=ricetta_attiva) # Recupero l'istanza da passare alla FK
        # Filtro le istanze di DettaglioRicettaRifinizione in base a ricetta_id
        dettagli_ricetta = DettaglioRicettaRifinizione.objects.filter(fk_ricetta_rifinizione=ricetta_id)

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
        
        redirect_url = reverse('ricette:modifica_ricetta_rifinizione', kwargs={'pk': ricetta_attiva.pk})
        return JsonResponse({'redirect_url': redirect_url}) 
    else:
        return JsonResponse({'error': 'Richiesta non valida.'})
    

def accoda_dettaglio_ricetta_colore_rifinizione(request):
    if request.method == 'POST':
        ricetta_id = request.POST.get('ricetta_id')
        ricetta_attiva = request.POST.get('ricettaAttiva')
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
        
        redirect_url = reverse('ricette:modifica_ricetta_rifinizione', kwargs={'pk': ricetta_attiva.pk})
        return JsonResponse({'redirect_url': redirect_url}) 
    else:
        return JsonResponse({'error': 'Richiesta non valida.'})
    


def accoda_dettaglio_ricetta_bagnato(request):
    if request.method == 'POST':
        ricetta_id = request.POST.get('ricetta_id')
        ricetta_attiva = request.POST.get('ricettaAttiva')        
        ricetta_attiva = RicettaBagnato.objects.get(pk=ricetta_attiva) # Recupero l'istanza da passare alla FK
        # Filtro le istanze di DettaglioRicettaRifinizione in base a ricetta_id
        dettagli_ricetta = DettaglioRicettaBagnato.objects.filter(fk_ricetta_bagnato=ricetta_id)

        # Duplico le istanze filtrate e modifico fk_ricetta_rifinizione
        for dettaglio in dettagli_ricetta:
            DettaglioRicettaBagnato.objects.create(
                fk_ricetta_bagnato=ricetta_attiva,
                fk_operazione_ricette=dettaglio.fk_operazione_ricette,
                numero_riga=dettaglio.numero_riga,
                quantity=dettaglio.quantity,
                tempo=dettaglio.tempo,
                temperatura=dettaglio.temperatura,
                procedura=dettaglio.procedura,
                fk_prodotto_chimico=dettaglio.fk_prodotto_chimico,
                note=dettaglio.note,
                created_by=dettaglio.created_by
            )
        
        redirect_url = reverse('ricette:modifica_ricetta_bagnato', kwargs={'pk': ricetta_attiva.pk})
        return JsonResponse({'redirect_url': redirect_url}) 
    else:
        return JsonResponse({'error': 'Richiesta non valida.'})
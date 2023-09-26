from .models import DettaglioRicettaRifinizione
from django.http import JsonResponse
from django.template.loader import render_to_string

def update_numero_riga(request):
    if request.method == "POST" and ("application/json" in request.META.get("HTTP_ACCEPT", "")):
        instance_id = request.POST.get("instance_id")
        new_numero_riga = request.POST.get("new_numero_riga")
        print("instance_id: " + str(instance_id))
        print("new_numero_riga: " + str(new_numero_riga))

        # Validazione: Assicurati che new_numero_riga sia un numero valido
        try:
            new_numero_riga = int(new_numero_riga)
            print("new_numero_riga corretto")
        except ValueError:
            return JsonResponse({"success": False, "error_message": "Il nuovo numero di riga non è valido."})

        try:
            dettaglio = DettaglioRicettaRifinizione.objects.get(pk=instance_id)
            dettaglio.numero_riga = new_numero_riga
            dettaglio.save()

            # Ricarica i dati dall'oggetto dal database
            dettaglio.refresh_from_db()

            # Verifica se il numero di riga è stato aggiornato correttamente
            if dettaglio.numero_riga == new_numero_riga:
                print("Le modifiche sono state salvate correttamente.")
            else:
                print("Si è verificato un problema durante il salvataggio delle modifiche.")
                return JsonResponse({"success": False, "error_message": "Si è verificato un problema durante il salvataggio delle modifiche."})

            # Esegui l'aggiornamento della riga di destinazione
            target_instance_id = request.POST.get("target_instance_id")
            target_new_numero_riga = request.POST.get("target_new_numero_riga")
            print("target_instance_id: " + str(target_instance_id))
            print("target_new_numero_riga: " + str(target_new_numero_riga))

            try:
                target_dettaglio = DettaglioRicettaRifinizione.objects.get(pk=target_instance_id)
                target_dettaglio.numero_riga = target_new_numero_riga
                target_dettaglio.save()

                # Ricarica i dati dall'oggetto dal database
                target_dettaglio.refresh_from_db()

                # Verifica se il numero di riga è stato aggiornato correttamente nella riga di destinazione
                if target_dettaglio.numero_riga == target_new_numero_riga:
                    print("Aggiornamento della riga di destinazione riuscito.")
                else:
                    print("Si è verificato un problema durante l'aggiornamento della riga di destinazione.")
                    return JsonResponse({"success": False, "error_message": "Si è verificato un problema durante l'aggiornamento della riga di destinazione."})

                return JsonResponse({"success": True})
            except DettaglioRicettaRifinizione.DoesNotExist:
                print("L'istanza di destinazione non esiste.")
                return JsonResponse({"success": False, "error_message": "L'istanza di destinazione non esiste."})

        except DettaglioRicettaRifinizione.DoesNotExist:
            print("L'istanza non esiste.")
            return JsonResponse({"success": False, "error_message": "L'istanza non esiste."})
    else:
        print("Richiesta non valida.")
        return JsonResponse({"success": False, "error_message": "Richiesta non valida."})
    


def get_updated_table_data(request):
    pk_ricetta_rifinizione = request.GET.get("pk_ricetta_rifinizione")

    # Otteni i dati aggiornati dalla tabella basata su pk_ricetta_rifinizione
    updated_rows = DettaglioRicettaRifinizione.objects.filter(fk_ricetta_rifinizione=pk_ricetta_rifinizione)

    # Ora puoi creare l'HTML della tabella con i dati aggiornati
    table_html = render_to_string('path/to/updated_table_template.html', {'updated_rows': updated_rows})

    # Restituisci l'HTML della tabella come parte della risposta JSON
    return JsonResponse({"success": True, "table_html": table_html})

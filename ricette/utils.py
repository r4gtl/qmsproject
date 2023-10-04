from .models import DettaglioRicettaRifinizione
from django.http import JsonResponse,HttpResponse
from django.template.loader import render_to_string, get_template
from django.shortcuts import render
from django.template import RequestContext

def update_numero_riga(request):
    if request.method == "POST" and ("application/json" in request.META.get("HTTP_ACCEPT", "")):
        instance_id = request.POST.get("instance_id")
        new_numero_riga = request.POST.get("new_numero_riga")
        print("instance_id (riga 7): " + str(instance_id))
        print("new_numero_riga (riga 8): " + str(new_numero_riga))

        # Validazione: Assicurati che new_numero_riga sia un numero valido
        # try:
        #     new_numero_riga = int(new_numero_riga)
        #     print("new_numero_riga corretto")
        # except ValueError:
        #     return JsonResponse({"success": False, "error_message": "Il nuovo numero di riga non è valido."})

        if new_numero_riga is not None:
            try:
                new_numero_riga = int(new_numero_riga)
                print("new_numero_riga corretto")
            except ValueError:
                return JsonResponse({"success": False, "error_message": "Il nuovo numero di riga non è valido."})
        else:
            return JsonResponse({"success": False, "error_message": "Il nuovo numero di riga è mancante o non valido."})
        
        
        try:
            dettaglio = DettaglioRicettaRifinizione.objects.get(pk=instance_id)
            dettaglio.numero_riga = new_numero_riga
            dettaglio.save()

            # Ricarica i dati dall'oggetto dal database
            dettaglio.refresh_from_db()

            # Verifica se il numero di riga è stato aggiornato correttamente
            # if dettaglio.numero_riga == new_numero_riga:
            #     print("Le modifiche sono state salvate correttamente.")
            # else:
            #     print("Si è verificato un problema durante il salvataggio delle modifiche.")
            #     return JsonResponse({"success": False, "error_message": "Si è verificato un problema durante il salvataggio delle modifiche."})

            # Esegui l'aggiornamento della riga di destinazione
            instance_id = request.POST.get("instance_id")
            new_numero_riga = request.POST.get("new_numero_riga")
            
            print(f"target_instance_id (riga 45): {instance_id}")
            print(f"target_new_numero_riga: {new_numero_riga}")

            try:
                target_dettaglio = DettaglioRicettaRifinizione.objects.get(pk=instance_id)
                target_dettaglio.numero_riga = new_numero_riga
                target_dettaglio.save()

                # Ricarica i dati dall'oggetto dal database
                #target_dettaglio.refresh_from_db()

                # Verifica se il numero di riga è stato aggiornato correttamente nella riga di destinazione
                # if target_dettaglio.numero_riga == target_new_numero_riga:
                #     print("Aggiornamento della riga di destinazione riuscito.")
                # else:
                #     print("Errore, target_dettaglio.numero_riga: " + str(target_dettaglio.numero_riga))
                #     print("Errore, target_new_numero_riga: " + str(target_new_numero_riga))
                #     print("Si è verificato un problema durante l'aggiornamento della riga di destinazione.")
                #     return JsonResponse({"success": False, "error_message": "Si è verificato un problema durante l'aggiornamento della riga di destinazione."})

                return JsonResponse({"success": True})
            except DettaglioRicettaRifinizione.DoesNotExist:
                error_message = f"L'istanza con ID {instance_id} non esiste nel database."
                print(error_message)
                return JsonResponse({"success": False, "error_message": error_message})

        except DettaglioRicettaRifinizione.DoesNotExist:
            print("L'istanza non esiste.")
            return JsonResponse({"success": False, "error_message": "L'istanza non esiste."})
    else:
        print("Richiesta non valida.")
        return JsonResponse({"success": False, "error_message": "Richiesta non valida."})
    


def get_updated_table_data(request):
    pk_ricetta_rifinizione = request.GET.get("pk_ricetta_rifinizione")
    updated_rows = DettaglioRicettaRifinizione.objects.filter(fk_ricetta_rifinizione=pk_ricetta_rifinizione)
    
    # Crea un contesto RequestContext
    context = {'updated_rows': updated_rows}

    # Usa RequestContext quando chiami render_to_string
    template = get_template('ricette/partials/_dettaglio_ricetta_rifinizione_table.html')
    table_html = template.render(context)
    
    # Restituisci solo l'HTML della tabella come HttpResponse
    return HttpResponse(table_html)

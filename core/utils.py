import json
from datetime import date, timedelta

from django.apps import apps
from django.core.serializers import serialize
from django.db.models import Max, Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

'''
Questa funzione serve per conteggiare quanti record hanno la prossima scadenza nei prossimi x giorni.
Utilizzata inizialmente per i badge con il numero di prossime scadenze e la possibilità di aprire un template scadenzario.
Esempio:
record_count = count_records_with_upcoming_expiry(MyModel, "prossima_scadenza", 30)
'''

def count_records_with_upcoming_expiry(model, date_field, days):
    current_date = date.today()
    end_date = current_date + timedelta(days=days)
    
    count = model.objects.filter(
        Q(**{f"{date_field}__gte": current_date}) & Q(**{f"{date_field}__lte": end_date})
    ).count()
    
    return count



def get_records_with_upcoming_expiry(model, date_field, days):
    current_date = date.today()
    end_date = current_date + timedelta(days=days)
    
    records = model.objects.filter(
        Q(**{f"{date_field}__gte": current_date}) & Q(**{f"{date_field}__lte": end_date})
    )
    
    return records



'''
Questa funzione serve per conteggiare quanti record ci sono nell'intervallo richiesto.
Utilizzata inizialmente per avere un controllo sui monitoraggi.
Esempio:
record_count = get_record_last_interval(MyModel, "data_lettura", 365)
'''

def get_record_last_interval(model, date_field, days):
    current_date = date.today()
    begin_date = current_date - timedelta(days=days)
    
    count = model.objects.filter(
        Q(**{f"{date_field}__lte": current_date}) & Q(**{f"{date_field}__gte": begin_date})
    ).count()
    
    return count




@csrf_exempt
def update_numero_riga_down(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        model_name = request.POST.get('model')
        app_label = request.POST.get('app_label')
        dettaglio_id = request.POST.get('dettaglio_id')
        action = request.POST.get('action')

        # Ottieni il modello dinamicamente
        model = apps.get_model(app_label=app_label, model_name=model_name)
        dettaglio = model.objects.get(pk=dettaglio_id)

        # Controlla se c'è una riga precedente
        riga_precedente = model.objects.filter(
            fk_procedura=dettaglio.fk_procedura,
            numero_riga=dettaglio.numero_riga - 1
        ).first()

        if riga_precedente:
            # Scambia le posizioni delle due righe
            dettaglio.numero_riga, riga_precedente.numero_riga = riga_precedente.numero_riga, dettaglio.numero_riga
            dettaglio.save()
            riga_precedente.save()

            # Dopo aver salvato le righe, ottieni l'elenco aggiornato delle righe
            elenco_aggiornato = serialize('json', model.objects.filter(fk_procedura=dettaglio.fk_procedura).order_by('numero_riga'))
            elenco_aggiornato_dict = json.loads(elenco_aggiornato)
            print(f'Elenco aggiornato down: {elenco_aggiornato_dict}')

            return JsonResponse({'success': True, 'elenco_aggiornato': elenco_aggiornato_dict, 'numero_riga': dettaglio.numero_riga})

        return JsonResponse({'success': False, 'error': 'Nessuna riga precedente disponibile'})

    return JsonResponse({'success': False, 'error': 'Richiesta non valida'}, status=400)

# Nella funzione update_numero_riga_up
@csrf_exempt
def update_numero_riga_up(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        model_name = request.POST.get('model')
        app_label = request.POST.get('app_label')
        dettaglio_id = request.POST.get('dettaglio_id')
        action = request.POST.get('action')

        # Ottieni il modello dinamicamente
        model = apps.get_model(app_label=app_label, model_name=model_name)
        dettaglio = model.objects.get(pk=dettaglio_id)

        # Controlla se c'è una riga successiva
        riga_successiva = model.objects.filter(
            fk_procedura=dettaglio.fk_procedura,
            numero_riga=dettaglio.numero_riga + 1
        ).first()

        # Verifica se la riga è già al massimo delle righe con lo stesso ID
        max_numero_riga = model.objects.filter(fk_procedura=dettaglio.fk_procedura).aggregate(Max('numero_riga'))['numero_riga__max']
        
        if riga_successiva:
            # Abbassa la riga successiva di 1
            riga_successiva.numero_riga -= 1
            riga_successiva.save()

            # Aumenta la riga corrente di 1
            dettaglio.numero_riga += 1
            dettaglio.save()

            # Dopo aver salvato le righe, ottieni l'elenco aggiornato delle righe
            elenco_aggiornato = serialize('json', model.objects.filter(fk_procedura=dettaglio.fk_procedura).order_by('numero_riga'))
            elenco_aggiornato_dict = json.loads(elenco_aggiornato)
            print(f'Elenco aggiornato up: {elenco_aggiornato_dict}')

            return JsonResponse({'success': True, 'elenco_aggiornato': elenco_aggiornato_dict, 'numero_riga': dettaglio.numero_riga})

        elif dettaglio.numero_riga < max_numero_riga:
            # Aumenta la riga corrente di 1
            dettaglio.numero_riga += 1
            dettaglio.save()

            # Dopo aver salvato le righe, ottieni l'elenco aggiornato delle righe
            elenco_aggiornato = serialize('json', model.objects.filter(fk_procedura=dettaglio.fk_procedura).order_by('numero_riga'))
            elenco_aggiornato_dict = json.loads(elenco_aggiornato)
            print(f'Elenco aggiornato up: {elenco_aggiornato_dict}')

            return JsonResponse({'success': True, 'elenco_aggiornato': elenco_aggiornato_dict, 'numero_riga': dettaglio.numero_riga})

        return JsonResponse({'success': False, 'error': 'La riga è già al massimo delle righe disponibili'})

    return JsonResponse({'success': False, 'error': 'Richiesta non valida'}, status=400)



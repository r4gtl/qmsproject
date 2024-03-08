import json
from datetime import date, timedelta

from articoli.models import *
from django.apps import apps
from django.core.exceptions import ValidationError
from django.core.serializers import serialize
from django.db import models
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

# Prova astrazione update_row_numbers per drag 'n drop


def update_row_numbers(request, app_name, model_name):
    # Ottieni il modello dal nome
    
    try:
        model = apps.get_model(app_name, model_name)
        
    except LookupError:
        print("Eccomi LookupError")
        return JsonResponse({'error': 'Modello non trovato'}, status=400)
    
    
    if request.method == 'POST':
        
        data = json.loads(request.body)
        data_list = data['data']
        
        # Itera sui dati ricevuti e aggiorna i record nel database
        for item in data_list:            
            pk = item['pk']
            new_numero_riga = item['numero_riga']
            try:
                instance = model.objects.get(pk=pk)
                
            except model.DoesNotExist:
                return JsonResponse({'error': 'Oggetto non trovato'}, status=400)
            instance.numero_riga = new_numero_riga
            instance.save()
        
        return JsonResponse({'message': 'Numeri di riga aggiornati con successo'}, status=200)
    
    else:        
        return JsonResponse({'error': 'Richiesta non valida'}, status=400)



# Questa funzione serve a controllare i duplicati anche se sono scritti 
# con maiuscole e minuscole diverse
# Uso:
# importare nel file models.py in cui è presente il campo da controllare la funzione
# from core.utils import no_duplicates_validator
# nel modello interessato inserire la funzione
# def clean(self):
#        no_duplicates_validator(
#            self.my_field,
#            'my_field',
#            self
#        )

def no_duplicates_validator(value, field_name, model_instance):
    model_class = model_instance.__class__
    field_lookup = {f'{field_name}__iexact': value}
    if model_class.objects.filter(**field_lookup).exclude(pk=model_instance.pk).exists():
        raise ValidationError('Questo valore è già presente.')
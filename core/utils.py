from datetime import date, timedelta
from django.db.models import Q



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

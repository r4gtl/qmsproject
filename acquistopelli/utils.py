from datetime import datetime
from django.db.models import Count
from .models import Lotto

# def filtro_lotti(data_inizio, data_fine):
#     lotti_filtrati = Lotto.objects.filter(data_acquisto__range=[data_inizio, data_fine])
#     return lotti_filtrati


def filtro_lotti(data_inizio, data_fine):
    lotti_filtrati = (
        Lotto.objects
        .filter(data_acquisto__range=[data_inizio, data_fine])
        .values('fk_fornitore', 'data_acquisto', 'identificativo', 'fk_tipoanimale', 'fk_tipogrezzo')
        .annotate(numero_lotti=Count('pk'))
        .order_by('fk_fornitore')
    )
    return lotti_filtrati
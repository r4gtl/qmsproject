from datetime import datetime
from .models import Lotto

def filtro_lotti(data_inizio, data_fine):
    lotti_filtrati = Lotto.objects.filter(data_acquisto__range=[data_inizio, data_fine])
    return lotti_filtrati
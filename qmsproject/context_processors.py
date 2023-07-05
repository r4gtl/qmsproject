from anagrafiche.models import Facility
from human_resources.models import Ward

def nome_sito(request):
    facility = Facility.objects.first()  # Scegli la Facility corretta o utilizza la logica di scelta desiderata
    return {'nome_sito': facility.nome_sito if facility else ''}


# questa funzione restituisce un elenco preso dal modello Wards e aggiunge "Tutti"
# Inizialmente usato per il modal che renderizza la stampa dei piani di manutenzione e taratura
def fk_ward_records(request):
    wards = Ward.objects.all()
    ward_records = [('tutti', 'Tutti')] + [(ward.pk, ward.description) for ward in wards]
    #for ward in ward_records:
     #   print(str(ward[0] + ' ' + str(ward[1])))
    return {'fk_ward_records': ward_records}
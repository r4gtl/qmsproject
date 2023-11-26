from anagrafiche.models import Facility
from human_resources.models import Ward
from core.configuration_apps import get_app_icons

def nome_sito(request):
    facility = Facility.objects.first()  # Scegli la Facility corretta o utilizza la logica di scelta desiderata
    return {'nome_sito': facility.nome_sito if facility else ''}

def logo_sito(request):
    facility = Facility.objects.first()  # Scegli la Facility corretta o utilizza la logica di scelta desiderata
    return {'logo_sito': facility.logo if facility else ''}


# questa funzione restituisce un elenco preso dal modello Wards e aggiunge "Tutti"
# Inizialmente usato per il modal che renderizza la stampa dei piani di manutenzione e taratura
def fk_ward_records(request):
    wards = Ward.objects.all()
    ward_records = [('tutti', 'Tutti')] + [(ward.pk, ward.description) for ward in wards]
    #for ward in ward_records:
     #   print(str(ward[0] + ' ' + str(ward[1])))
    return {'fk_ward_records': ward_records}



# mappa delle icone delle app
def app_icons(request):
    '''
    app_icons = {
        'chem_man': 'bi bi-moisture',
        'manutenzioni': 'bi bi-house-check',
        'tarature': 'bi bi-house-check',
        'autorizzazioni': 'bi bi-file-check',
        'risorse umane': 'bi bi-person-workspace',
        # Aggiungi altre app e icone come necessario
    }
    print('app_icons: ' + str(app_icons))
    '''
    app_icons = get_app_icons()
    return {'app_icons': app_icons}
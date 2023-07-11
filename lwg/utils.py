from datetime import date
from autorizzazioni.models import DettaglioScadenzaAutorizzazione
from manutenzioni.models import Taratura, ManutenzioneOrdinaria
from human_resources.models import DettaglioRegistroFormazione


def get_scadenzario_completo():
    today = date.today()
    scadenzario = []
    scadenze_autorizzazioni = DettaglioScadenzaAutorizzazione.objects.filter(scadenza_rinnovo__gte=today).filter(is_rinnovata=False)
    for scadenza in scadenze_autorizzazioni:
        scadenzario.append({
            'scadenza': scadenza.scadenza_rinnovo,
            'descrizione': scadenza.fk_autorizzazione.descrizione,
            'nomemodello': 'autorizzazioni',
            'url': "autorizzazioni:autorizzazioni_home"
        })

    scadenze_manutenzioni = ManutenzioneOrdinaria.objects.filter(prossima_scadenza__gte=today)
    for scadenza in scadenze_manutenzioni:
        scadenzario.append({
            'scadenza': scadenza.prossima_scadenza,
            'descrizione': scadenza.descrizione,
            'nomemodello': 'manutenzioni',
            'url': "manutenzioni:dashboard_manutenzioni"
        })

    scadenze_tarature = Taratura.objects.filter(prossima_scadenza__gte=today)
    for scadenza in scadenze_tarature:
        scadenzario.append({
            'scadenza': scadenza.prossima_scadenza,
            'descrizione': scadenza.fk_attrezzatura.descrizione,
            'nomemodello': 'tarature',
            'url': "manutenzioni:dashboard_manutenzioni"
        })
    
    scadenze_risorse_umane = DettaglioRegistroFormazione.objects.filter(prossima_scadenza__gte=today)
    for scadenza in scadenze_risorse_umane:
        scadenzario.append({
            'scadenza': scadenza.prossima_scadenza,
            'descrizione': str(scadenza.fk_hr) + ", " + str(scadenza.fk_registro_formazione.fk_corso.descrizione),
            'nomemodello': 'risorse umane',
            'url': "human_resources:human_resources"
        })

    

    scadenzario = sorted(scadenzario, key=lambda s: s['scadenza'])  # Ordina per data di scadenza
    

    return scadenzario
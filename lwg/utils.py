from datetime import date
from autorizzazioni.models import DettaglioScadenzaAutorizzazione
from manutenzioni.models import Taratura, ManutenzioneOrdinaria


def get_scadenzario_completo():
    today = date.today()
    scadenzario = []
    scadenze_autorizzazioni = DettaglioScadenzaAutorizzazione.objects.filter(scadenza_rinnovo__gte=today).filter(is_rinnovata=False)
    for scadenza in scadenze_autorizzazioni:
        scadenzario.append({
            'scadenza': scadenza.scadenza_rinnovo,
            'descrizione': scadenza.fk_autorizzazione.descrizione,
            'nomemodello': 'autorizzazioni',
        })

    scadenze_manutenzioni = ManutenzioneOrdinaria.objects.filter(prossima_scadenza__gte=today)
    for scadenza in scadenze_manutenzioni:
        scadenzario.append({
            'scadenza': scadenza.prossima_scadenza,
            'descrizione': scadenza.descrizione,
            'nomemodello': 'manutenzioni',
        })
    scadenzario = sorted(scadenzario, key=lambda s: s['scadenza'])  # Ordina per data di scadenza
    

    return scadenzario
# Generated manually for data migration
# human_resources 0042

from django.db import migrations
from dateutil.relativedelta import relativedelta


def migrate_prossima_scadenza_to_scadenza_override(apps, schema_editor):
    """
    Migra i dati esistenti:
    1. Copia prossima_scadenza → scadenza_override (se valorizzata)
    2. Calcola scadenza_calcolata = data_formazione + validita_mesi

    NOTA: prossima_scadenza viene mantenuto nel DB per sicurezza,
    ma non sarà più usato dal codice applicativo.
    """
    DettaglioRegistroFormazione = apps.get_model(
        'human_resources', 'DettaglioRegistroFormazione'
    )

    # Itera su tutti i dettagli esistenti
    for dettaglio in DettaglioRegistroFormazione.objects.select_related(
        'fk_registro_formazione',
        'fk_registro_formazione__fk_corso'
    ).all():
        updated = False

        # 1. Migra prossima_scadenza → scadenza_override (se valorizzata)
        if dettaglio.prossima_scadenza and not dettaglio.scadenza_override:
            dettaglio.scadenza_override = dettaglio.prossima_scadenza
            updated = True

        # 2. Calcola scadenza_calcolata se possibile
        registro = dettaglio.fk_registro_formazione
        if registro and registro.data_formazione and registro.fk_corso:
            validita_mesi = registro.fk_corso.validita_mesi or 12
            scadenza_calc = registro.data_formazione + relativedelta(
                months=validita_mesi
            )
            if dettaglio.scadenza_calcolata != scadenza_calc:
                dettaglio.scadenza_calcolata = scadenza_calc
                updated = True

        if updated:
            dettaglio.save(update_fields=[
                'scadenza_override',
                'scadenza_calcolata'
            ])


def reverse_migration(apps, schema_editor):
    """
    Rollback: non facciamo nulla perché i dati originali
    sono stati preservati in prossima_scadenza.
    """
    pass


class Migration(migrations.Migration):
    """
    Data migration per migrare prossima_scadenza ai nuovi campi.

    Decisione: mantenere prossima_scadenza nel DB per compatibilità.
    - I dati esistenti vengono copiati in scadenza_override
    - scadenza_calcolata viene popolata per tutti i record
    - prossima_scadenza resta come backup, ma deprecato
    """

    dependencies = [
        ('human_resources', '0041_formazione_scadenza_fields'),
    ]

    operations = [
        migrations.RunPython(
            migrate_prossima_scadenza_to_scadenza_override,
            reverse_migration,
        ),
    ]

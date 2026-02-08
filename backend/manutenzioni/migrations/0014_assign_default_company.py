# Generated manually - Assign default company to existing records

from django.db import migrations


def assign_default_company(apps, schema_editor):
    """
    Assign the default company to all existing manutenzioni records.
    """
    Company = apps.get_model('accounts', 'Company')
    Attrezzatura = apps.get_model('manutenzioni', 'Attrezzatura')
    ManutenzioneStraordinaria = apps.get_model('manutenzioni', 'ManutenzioneStraordinaria')
    ManutenzioneOrdinaria = apps.get_model('manutenzioni', 'ManutenzioneOrdinaria')
    Taratura = apps.get_model('manutenzioni', 'Taratura')
    ControlloPeriodico = apps.get_model('manutenzioni', 'ControlloPeriodico')

    # Get the default company
    try:
        default_company = Company.objects.get(slug='default-company')
    except Company.DoesNotExist:
        print("⚠️  Default company not found. Creating it...")
        default_company = Company.objects.create(
            name='Default Company',
            slug='default-company',
            is_active=True,
            subscription_plan='free',
            country='IT'
        )
        print(f"✓ Created default company: {default_company.name}")

    # Update all attrezzature without a company
    attrezzature_updated = Attrezzatura.objects.filter(company__isnull=True).update(
        company=default_company
    )
    print(f"✓ Updated {attrezzature_updated} Attrezzature with default company")

    # Update all manutenzioni straordinarie without a company
    ms_updated = ManutenzioneStraordinaria.objects.filter(company__isnull=True).update(
        company=default_company
    )
    print(f"✓ Updated {ms_updated} Manutenzioni Straordinarie with default company")

    # Update all manutenzioni ordinarie without a company
    mo_updated = ManutenzioneOrdinaria.objects.filter(company__isnull=True).update(
        company=default_company
    )
    print(f"✓ Updated {mo_updated} Manutenzioni Ordinarie with default company")

    # Update all tarature without a company
    tarature_updated = Taratura.objects.filter(company__isnull=True).update(
        company=default_company
    )
    print(f"✓ Updated {tarature_updated} Tarature with default company")

    # Update all controlli periodici without a company
    cp_updated = ControlloPeriodico.objects.filter(company__isnull=True).update(
        company=default_company
    )
    print(f"✓ Updated {cp_updated} Controlli Periodici with default company")


def reverse_migration(apps, schema_editor):
    """
    Set company to null for all records
    """
    Attrezzatura = apps.get_model('manutenzioni', 'Attrezzatura')
    ManutenzioneStraordinaria = apps.get_model('manutenzioni', 'ManutenzioneStraordinaria')
    ManutenzioneOrdinaria = apps.get_model('manutenzioni', 'ManutenzioneOrdinaria')
    Taratura = apps.get_model('manutenzioni', 'Taratura')
    ControlloPeriodico = apps.get_model('manutenzioni', 'ControlloPeriodico')

    Attrezzatura.objects.all().update(company=None)
    ManutenzioneStraordinaria.objects.all().update(company=None)
    ManutenzioneOrdinaria.objects.all().update(company=None)
    Taratura.objects.all().update(company=None)
    ControlloPeriodico.objects.all().update(company=None)


class Migration(migrations.Migration):

    dependencies = [
        ('manutenzioni', '0013_add_company_field'),
        ('accounts', '0008_create_default_company'),
    ]

    operations = [
        migrations.RunPython(assign_default_company, reverse_migration),
    ]

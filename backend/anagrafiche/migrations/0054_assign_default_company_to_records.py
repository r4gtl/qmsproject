# Generated automatically

from django.db import migrations


def assign_default_company(apps, schema_editor):
    """
    Assign the default company to all existing Cliente and Fornitore records.
    """
    Company = apps.get_model('accounts', 'Company')
    Cliente = apps.get_model('anagrafiche', 'Cliente')
    Fornitore = apps.get_model('anagrafiche', 'Fornitore')

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

    # Update all clienti without a company
    clienti_updated = Cliente.objects.filter(company__isnull=True).update(
        company=default_company
    )
    print(f"✓ Updated {clienti_updated} Clienti with default company")

    # Update all fornitori without a company
    fornitori_updated = Fornitore.objects.filter(company__isnull=True).update(
        company=default_company
    )
    print(f"✓ Updated {fornitori_updated} Fornitori with default company")


def reverse_migration(apps, schema_editor):
    """
    Set company to null for all records
    """
    Cliente = apps.get_model('anagrafiche', 'Cliente')
    Fornitore = apps.get_model('anagrafiche', 'Fornitore')

    Cliente.objects.all().update(company=None)
    Fornitore.objects.all().update(company=None)


class Migration(migrations.Migration):

    dependencies = [
        ('anagrafiche', '0053_cliente_company_fornitore_company'),
        ('accounts', '0008_create_default_company'),
    ]

    operations = [
        migrations.RunPython(assign_default_company, reverse_migration),
    ]

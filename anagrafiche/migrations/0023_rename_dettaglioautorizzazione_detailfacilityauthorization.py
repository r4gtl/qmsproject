# Generated by Django 4.2.1 on 2023-12-12 10:37

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('anagrafiche', '0022_facilityauthorization_dettaglioautorizzazione'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DettaglioAutorizzazione',
            new_name='DetailFacilityAuthorization',
        ),
    ]
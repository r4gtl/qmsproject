# Generated by Django 4.2.1 on 2023-12-12 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anagrafiche', '0023_rename_dettaglioautorizzazione_detailfacilityauthorization'),
    ]

    operations = [
        migrations.AddField(
            model_name='detailfacilityauthorization',
            name='is_rinnovata',
            field=models.BooleanField(default=False),
        ),
    ]
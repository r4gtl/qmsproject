# Generated by Django 4.2.1 on 2023-07-25 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chem_man", "0013_acquistoprodottochimico_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="dettaglioacquistoprodottochimico",
            name="solvente",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]

# Generated by Django 4.2.1 on 2023-11-28 16:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articoli', '0014_dettaglioprocedura_is_interna_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dettaglioprocedura',
            options={'ordering': ['numero_riga'], 'verbose_name_plural': 'dettaglio procedure'},
        ),
    ]
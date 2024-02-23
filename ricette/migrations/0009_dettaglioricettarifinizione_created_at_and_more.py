# Generated by Django 4.2.1 on 2024-02-23 13:41

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import ricette.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('articoli', '0015_alter_dettaglioprocedura_options'),
        ('chem_man', '0023_alter_prodottochimico_options'),
        ('ricette', '0008_alter_dettaglioricettarifinizione_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='dettaglioricettarifinizione',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='RicettaColoreRifinizione',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_ricetta', models.IntegerField(blank=True, null=True)),
                ('data_ricetta', models.DateField(default=datetime.date.today)),
                ('numero_revisione', models.IntegerField(blank=True, null=True)),
                ('data_revisione', models.DateField(default=datetime.date.today)),
                ('note', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ricette_colore_rifinizione', to=settings.AUTH_USER_MODEL)),
                ('fk_articolo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ricette_colore_rifinizione', to='articoli.articolo')),
                ('fk_colore', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ricette_colore_rifinizione', to='articoli.colore')),
            ],
            options={
                'ordering': ['-data_ricetta'],
            },
        ),
        migrations.CreateModel(
            name='DettaglioRicettaColoreRifinizione',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_riga', models.IntegerField()),
                ('quantity', models.DecimalField(decimal_places=4, max_digits=8)),
                ('note', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dettaglio_colore_rifinizione', to=settings.AUTH_USER_MODEL)),
                ('fk_operazione_ricette', models.ForeignKey(limit_choices_to=ricette.models.DettaglioRicettaColoreRifinizione.get_choices_operations, on_delete=django.db.models.deletion.CASCADE, related_name='dettaglio_colore_rifinizione', to='ricette.operazionericette')),
                ('fk_prodotto_chimico', models.ForeignKey(limit_choices_to=ricette.models.DettaglioRicettaColoreRifinizione.get_choices_chemical, on_delete=django.db.models.deletion.CASCADE, related_name='dettaglio_colore_rifinizione', to='chem_man.prodottochimico')),
                ('fk_ricetta_colore_rifinizione', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dettaglio_colore_rifinizione', to='ricette.ricettacolorerifinizione')),
            ],
            options={
                'ordering': ['numero_riga'],
            },
        ),
    ]
# Generated by Django 4.2.1 on 2023-06-20 07:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Autorizzazione',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descrizione', models.CharField(help_text='Descrizione', max_length=100)),
                ('rilasciata_da', models.CharField(help_text='Rilasciata da', max_length=100)),
                ('n_autorizzazione', models.CharField(blank=True, help_text='Identificativo', max_length=100, null=True)),
                ('data_autorizzazione', models.DateField(blank=True, null=True)),
                ('frequenza_scadenza', models.CharField(blank=True, help_text='Frequenza', max_length=50, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='autorizzazioni', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-data_autorizzazione'],
            },
        ),
        migrations.CreateModel(
            name='DettaglioScadenzaAutorizzazione',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('n_rinnovo', models.CharField(blank=True, help_text='numero autorizzazione', max_length=100, null=True)),
                ('data_rinnovo', models.DateField(blank=True, null=True)),
                ('scadenza_rinnovo', models.DateField(blank=True, null=True)),
                ('is_rinnovata', models.BooleanField(default=False)),
                ('documento', models.FileField(blank=True, null=True, upload_to='autorizzazioni/')),
                ('note', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dettaglio_scadenze_autorizzazioni', to=settings.AUTH_USER_MODEL)),
                ('fk_autorizzazione', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autorizzazioni.autorizzazione')),
            ],
            options={
                'ordering': ['-data_rinnovo'],
                'get_latest_by': ['data_rinnovo'],
            },
        ),
    ]
# Generated by Django 4.2.1 on 2023-12-12 10:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('anagrafiche', '0021_facility_logo'),
    ]

    operations = [
        migrations.CreateModel(
            name='FacilityAuthorization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descrizione', models.CharField(help_text='Oggetto autorizzazione', max_length=500)),
                ('purpose', models.CharField(blank=True, help_text='Finalità autorizzazione', max_length=500, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='facility_authorization', to=settings.AUTH_USER_MODEL)),
                ('fk_facility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='facility_authorization', to='anagrafiche.facility')),
                ('fk_fornitore', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='facility_authorization', to='anagrafiche.fornitore')),
            ],
            options={
                'ordering': ['descrizione'],
            },
        ),
        migrations.CreateModel(
            name='DettaglioAutorizzazione',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(help_text='Numero/Protocollo', max_length=100)),
                ('data_autorizzazione', models.DateField()),
                ('prossima_scadenza', models.DateField(blank=True, null=True)),
                ('documento', models.FileField(blank=True, null=True, upload_to='autorizzazioni_facility/')),
                ('note', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='detail_facility_authorization', to=settings.AUTH_USER_MODEL)),
                ('fk_facility_authorization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detail_facility_authorization', to='anagrafiche.facilityauthorization')),
            ],
            options={
                'ordering': ['-data_autorizzazione'],
            },
        ),
    ]

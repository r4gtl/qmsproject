# Generated by Django 4.2.1 on 2023-06-09 08:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('anagrafiche', '0006_alter_transfervalue_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lotto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_acquisto', models.DateField()),
                ('identificativo', models.CharField(max_length=10)),
                ('origine', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('documento', models.CharField(blank=True, max_length=10, null=True)),
                ('is_lwg', models.BooleanField(default=False)),
                ('pezzi', models.IntegerField(blank=True, null=True)),
                ('prezzo_unitario', models.DecimalField(decimal_places=3, max_digits=8)),
                ('spese_accessorie', models.DecimalField(decimal_places=3, max_digits=10)),
                ('note', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lotto', to=settings.AUTH_USER_MODEL)),
                ('fk_fornitore', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='anagrafiche.fornitore')),
            ],
            options={
                'verbose_name_plural': 'Lotti',
                'ordering': ['-data_acquisto'],
            },
        ),
        migrations.CreateModel(
            name='Scelta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descrizione', models.CharField(max_length=50)),
                ('note', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='scelta', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'scelta',
                'ordering': ['descrizione'],
            },
        ),
        migrations.CreateModel(
            name='TipoGrezzo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descrizione', models.CharField(max_length=10)),
                ('note', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='grezzo', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'tipi grezzo',
                'ordering': ['descrizione'],
            },
        ),
        migrations.CreateModel(
            name='TipoAnimale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descrizione', models.CharField(max_length=10)),
                ('note', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='animale', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'tipi animale',
                'ordering': ['descrizione'],
            },
        ),
        migrations.CreateModel(
            name='SceltaLotto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pezzi', models.IntegerField(blank=True, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sceltalotto', to=settings.AUTH_USER_MODEL)),
                ('fk_lotto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='acquistopelli.lotto')),
                ('fk_scelta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='acquistopelli.scelta')),
            ],
        ),
        migrations.AddField(
            model_name='lotto',
            name='fk_tipoanimale',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='acquistopelli.tipoanimale'),
        ),
        migrations.AddField(
            model_name='lotto',
            name='fk_tipogrezzo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='acquistopelli.tipogrezzo'),
        ),
    ]

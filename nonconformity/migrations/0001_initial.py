# Generated by Django 4.2.1 on 2023-06-28 07:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('anagrafiche', '0007_alter_fornitore_created_by'),
        ('human_resources', '0014_alter_registroorelavoro_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RapportoNC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_nc', models.PositiveIntegerField(editable=False)),
                ('data_nc', models.DateField()),
                ('tipo_nc', models.CharField(choices=[('NC di Sistema', 'NC di Sistema'), ('NC di Produzione', 'NC di Produzione'), ('NC da Cliente', 'NC da Cliente'), ('NC a Fornitore', 'NC a Fornitore'), ('NC Aspetti Ambientali', 'NC Aspetti Ambientali'), ('Commento', 'Commento')], max_length=50)),
                ('segnalato_da', models.CharField(choices=[('Cliente', 'Cliente'), ('Fornitore', 'Fornitore'), ('Interno', 'Interno')], max_length=50)),
                ('descrizione', models.CharField(blank=True, max_length=240, null=True)),
                ('causa_radice', models.CharField(blank=True, max_length=240, null=True)),
                ('settore_responsabile', models.CharField(blank=True, max_length=100, null=True)),
                ('decisioni_immediate', models.CharField(choices=[('Accettare', 'Accettare'), ('Rilavorare', 'Rilavorare'), ('Scartare', 'Scartare'), ('Sostituire', 'Sostituire'), ('Altro', 'Altro')], max_length=50)),
                ('note_decisioni_immediate', models.TextField(blank=True, null=True)),
                ('responsabile_decisione_immediata', models.CharField(blank=True, max_length=50, null=True)),
                ('data_limite_decisione_immediata', models.DateField()),
                ('is_ac_necessaria', models.BooleanField(default=False)),
                ('descrizione_ac', models.TextField(blank=True, null=True)),
                ('responsabile_ac', models.CharField(blank=True, max_length=50, null=True)),
                ('data_limite_ac', models.DateField()),
                ('is_ac_completa', models.BooleanField(default=False)),
                ('is_ac_efficace', models.BooleanField(default=False)),
                ('altre_decisioni_ac', models.TextField(blank=True, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('compilato_da', models.ForeignKey(blank=True, limit_choices_to={'datadimissioni__isnull': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='human_resources.humanresource')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rapportornc', to=settings.AUTH_USER_MODEL)),
                ('fk_cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='anagrafiche.cliente')),
                ('fk_fornitore', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='anagrafiche.fornitore')),
            ],
            options={
                'ordering': ['-data_nc'],
            },
        ),
    ]

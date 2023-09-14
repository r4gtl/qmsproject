# Generated by Django 4.2.1 on 2023-09-14 09:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('antincendio', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Idrante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_posizione', models.IntegerField()),
                ('tipo_idrante', models.CharField(choices=[('idrante a parete', 'Interno'), ('Idrante soprasuolo', 'Idrante soprasuolo'), ('Idrante a colonna soprasuolo', 'Idrante a colonna soprasuolo'), ('Gruppo fisso schiuma', 'Gruppo fisso schiuma'), ('Gruppo mobile schiuma', 'Gruppo mobile schiuma'), ('Attacco autopompa VVF', 'Attacco autopompa VVF'), ('Alimentazione acquedotto', 'Alimentazione acquedotto'), ('Alimentazione con pompe', 'Alimentazione con pompe'), ('Evacuatori di fumo', 'Evacuatori di fumo'), ('Naspo', 'Naspo')], max_length=35)),
                ('uni', models.CharField(blank=True, max_length=4, null=True)),
                ('metri', models.CharField(blank=True, max_length=4, null=True)),
                ('anno', models.CharField(max_length=4)),
                ('data_dismissione', models.DateField(blank=True, null=True)),
                ('scadenza_schiuma', models.DateField(blank=True, null=True)),
                ('scadenza_collaudo', models.DateField()),
                ('ubicazione', models.CharField(max_length=200)),
                ('note', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='idrante', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['numero_posizione'],
            },
        ),
    ]
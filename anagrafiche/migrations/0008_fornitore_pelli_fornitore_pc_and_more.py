# Generated by Django 4.2.1 on 2023-07-25 13:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('anagrafiche', '0007_alter_fornitore_created_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fornitore_Pelli',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prova', models.CharField(blank=True, max_length=50, null=True)),
                ('fornitore', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='fornitore_pelli', to='anagrafiche.fornitore')),
            ],
        ),
        migrations.CreateModel(
            name='Fornitore_PC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prova', models.CharField(blank=True, max_length=50, null=True)),
                ('fornitore', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='fornitore_pc', to='anagrafiche.fornitore')),
            ],
        ),
        migrations.CreateModel(
            name='Fornitore_Lavorazioni_Servizi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prova', models.CharField(blank=True, max_length=50, null=True)),
                ('fornitore', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='fornitore_servizi', to='anagrafiche.fornitore')),
            ],
        ),
        migrations.CreateModel(
            name='Fornitore_Lavorazioni_Esterne',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prova', models.CharField(blank=True, max_length=50, null=True)),
                ('fornitore', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='fornitore_lavorazioni', to='anagrafiche.fornitore')),
            ],
        ),
    ]

# Generated by Django 4.2.1 on 2025-05-26 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendite', '0005_schedalavorazione_xrscelteschede'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedalavorazione',
            name='metri_quadrati_finali',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Inserisci la superficie in metri quadrati', max_digits=10, null=True, verbose_name='Superficie (m²)'),
        ),
        migrations.AlterField(
            model_name='schedalavorazione',
            name='tot_pelli',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='schedalavorazione',
            name='tot_pelli_finale',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]

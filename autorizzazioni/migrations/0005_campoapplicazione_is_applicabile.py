# Generated by Django 4.2.1 on 2023-06-20 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autorizzazioni', '0004_campoapplicazione_dettagliocampoapplicazione'),
    ]

    operations = [
        migrations.AddField(
            model_name='campoapplicazione',
            name='is_applicabile',
            field=models.BooleanField(default=False),
        ),
    ]
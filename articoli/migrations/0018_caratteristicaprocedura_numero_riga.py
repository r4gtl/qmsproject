# Generated by Django 4.2.1 on 2024-03-15 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articoli', '0017_alter_caratteristicaprocedura_valore'),
    ]

    operations = [
        migrations.AddField(
            model_name='caratteristicaprocedura',
            name='numero_riga',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
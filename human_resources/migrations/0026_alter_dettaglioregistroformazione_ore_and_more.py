# Generated by Django 4.2.1 on 2024-01-26 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('human_resources', '0025_alter_registroorelavoro_entry_month_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dettaglioregistroformazione',
            name='ore',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='registroformazione',
            name='ore',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, null=True),
        ),
    ]

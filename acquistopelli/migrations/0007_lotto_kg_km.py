# Generated by Django 4.2.1 on 2024-02-07 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("acquistopelli", "0006_lotto_peso_totale"),
    ]

    operations = [
        migrations.AddField(
            model_name="lotto",
            name="kg_km",
            field=models.DecimalField(
                blank=True, decimal_places=0, max_digits=10, null=True
            ),
        ),
    ]

# Generated by Django 4.2.1 on 2024-02-07 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "acquistopelli",
            "0005_alter_lotto_fk_fornitore_alter_lotto_fk_tipoanimale_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="lotto",
            name="peso_totale",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=8, null=True
            ),
        ),
    ]
# Generated manually on 2026-02-06
# Increases max_digits for Gas and Energia DecimalFields to support larger values

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoraggi', '0009_datoproduzione_fk_tipoanimale'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monitoraggiogas',
            name='mc_in',
            field=models.DecimalField(decimal_places=3, max_digits=12),
        ),
        migrations.AlterField(
            model_name='monitoraggioenergiaelettrica',
            name='kwh_in',
            field=models.DecimalField(decimal_places=3, max_digits=12),
        ),
    ]

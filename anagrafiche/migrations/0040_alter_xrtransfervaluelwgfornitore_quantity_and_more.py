# Generated by Django 4.2.1 on 2024-12-14 21:46

import anagrafiche.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anagrafiche', '0039_alter_xrdocumentitrasportatore_fornitore_rifiuti'),
    ]

    operations = [
        migrations.AlterField(
            model_name='xrtransfervaluelwgfornitore',
            name='quantity',
            field=models.DecimalField(decimal_places=8, max_digits=10, validators=[anagrafiche.models.validate_positive_quantity]),
        ),
        migrations.AddConstraint(
            model_name='xrtransfervaluelwgfornitore',
            constraint=models.UniqueConstraint(fields=('fk_lwgcertificato', 'fk_transfervalue'), name='unique_lwgcertificato_transfervalue'),
        ),
    ]
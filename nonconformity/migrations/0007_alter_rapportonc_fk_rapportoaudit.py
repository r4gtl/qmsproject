# Generated by Django 4.2.1 on 2023-06-28 13:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nonconformity', '0006_alter_rapportonc_data_limite_ac_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rapportonc',
            name='fk_rapportoaudit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='nonconformity.rapportoaudit'),
        ),
    ]

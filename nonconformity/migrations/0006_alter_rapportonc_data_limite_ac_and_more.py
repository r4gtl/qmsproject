# Generated by Django 4.2.1 on 2023-06-28 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nonconformity', '0005_processoaudit_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rapportonc',
            name='data_limite_ac',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='rapportonc',
            name='data_limite_decisione_immediata',
            field=models.DateField(blank=True, null=True),
        ),
    ]
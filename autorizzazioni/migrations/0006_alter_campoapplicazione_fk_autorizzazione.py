# Generated by Django 4.2.1 on 2023-06-21 07:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('autorizzazioni', '0005_campoapplicazione_is_applicabile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campoapplicazione',
            name='fk_autorizzazione',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='autorizzazioni.autorizzazione'),
        ),
    ]
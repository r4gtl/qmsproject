# Generated by Django 4.2.1 on 2023-06-05 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('human_resources', '0003_areaformazione_corsoformazione_registroformazione_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dettaglioregistroformazione',
            name='fk_registro_formazione',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='human_resources.registroformazione'),
        ),
    ]
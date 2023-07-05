# Generated by Django 4.2.1 on 2023-07-04 13:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('human_resources', '0015_alter_registroorelavoro_entry_month'),
        ('manutenzioni', '0006_alter_attrezzatura_modello_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='attrezzatura',
            name='fk_ward',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='attrezzatura', to='human_resources.ward'),
        ),
    ]
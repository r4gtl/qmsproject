# Generated by Django 4.2.1 on 2024-12-14 14:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('anagrafiche', '0037_remove_fornitorerifiuti_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='xrdocumentitrasportatore',
            name='fornitore_rifiuti',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documenti_trasportatore', to='anagrafiche.fornitorerifiuti', to_field='fornitore_ptr_id'),
        ),
    ]

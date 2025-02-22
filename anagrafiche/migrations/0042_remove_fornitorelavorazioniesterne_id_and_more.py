# Generated by Django 4.2.1 on 2024-12-16 19:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('anagrafiche', '0041_remove_fornitoreservizi_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fornitorelavorazioniesterne',
            name='id',
        ),
        migrations.RemoveField(
            model_name='fornitoreprodottichimici',
            name='id',
        ),
        migrations.AlterField(
            model_name='fornitorelavorazioniesterne',
            name='fornitore_ptr',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='fornitore_ptr_lavorazioniesterne', serialize=False, to='anagrafiche.fornitore'),
        ),
        migrations.AlterField(
            model_name='fornitoreprodottichimici',
            name='fornitore_ptr',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='fornitore_ptr_prodottichimici', serialize=False, to='anagrafiche.fornitore'),
        ),
    ]

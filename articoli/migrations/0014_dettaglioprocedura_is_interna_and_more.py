# Generated by Django 4.2.1 on 2023-11-26 20:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("anagrafiche", "0021_facility_logo"),
        ("articoli", "0013_dettaglioprocedura_fk_fornitore_lavorazioneesterna"),
    ]

    operations = [
        migrations.AddField(
            model_name="dettaglioprocedura",
            name="is_interna",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="dettaglioprocedura",
            name="fk_fornitore",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="anagrafiche.fornitore",
            ),
        ),
    ]

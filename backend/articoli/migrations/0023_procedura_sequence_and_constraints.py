# Generated manually for Procedure system

from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Migration per il sistema Procedure:
    1. Crea sequence Postgres per nr_procedura (race-free)
    2. Aggiunge related_name alle FK
    3. Aggiunge UniqueConstraint per integrità dati
    """

    dependencies = [
        ("articoli", "0022_listinocliente"),
    ]

    operations = [
        # 1. Crea la sequence Postgres per nr_procedura
        migrations.RunSQL(
            sql="CREATE SEQUENCE IF NOT EXISTS procedura_nr_seq START 1;",
            reverse_sql="DROP SEQUENCE IF EXISTS procedura_nr_seq;",
        ),

        # 1b. Sincronizza la sequence con dati esistenti (race-free)
        migrations.RunSQL(
            sql="""
                SELECT setval('procedura_nr_seq',
                    COALESCE((SELECT MAX(nr_procedura) FROM articoli_procedura), 0) + 1,
                    false
                );
            """,
            reverse_sql="SELECT 1;",  # No-op per reverse
        ),

        # 2. Aggiorna Procedura: related_name su fk_articolo
        migrations.AlterField(
            model_name="procedura",
            name="fk_articolo",
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE,
                related_name="procedure",
                to="articoli.articolo",
            ),
        ),

        # 3. Aggiorna Procedura: related_name su created_by (evita clash)
        migrations.AlterField(
            model_name="procedura",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.deletion.SET_NULL,
                related_name="procedure_create",
                to="auth.user",
            ),
        ),

        # 4. Aggiorna DettaglioProcedura: related_name su fk_procedura
        migrations.AlterField(
            model_name="dettaglioprocedura",
            name="fk_procedura",
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE,
                related_name="dettagli",
                to="articoli.procedura",
            ),
        ),

        # 5. Aggiorna DettaglioProcedura: related_name su fk_faselavoro
        migrations.AlterField(
            model_name="dettaglioprocedura",
            name="fk_faselavoro",
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE,
                related_name="dettagli_procedura",
                to="articoli.faselavoro",
            ),
        ),

        # 6. Aggiorna DettaglioProcedura: related_name su fk_fornitore (legacy)
        migrations.AlterField(
            model_name="dettaglioprocedura",
            name="fk_fornitore",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.deletion.CASCADE,
                related_name="dettagli_procedura_legacy",
                to="anagrafiche.fornitore",
            ),
        ),

        # 7. Aggiorna CaratteristicaProcedura: related_name su fk_dettaglio_procedura
        migrations.AlterField(
            model_name="caratteristicaprocedura",
            name="fk_dettaglio_procedura",
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE,
                related_name="caratteristiche",
                to="articoli.dettaglioprocedura",
            ),
        ),

        # 8. Aggiorna CaratteristicaProcedura: related_name su fk_fornitore
        migrations.AlterField(
            model_name="caratteristicaprocedura",
            name="fk_fornitore",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.deletion.CASCADE,
                related_name="caratteristiche_procedura",
                to="anagrafiche.fornitore",
            ),
        ),

        # 9. Aggiorna CaratteristicaProcedura: related_name su fk_lavorazione_esterna
        migrations.AlterField(
            model_name="caratteristicaprocedura",
            name="fk_lavorazione_esterna",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.deletion.CASCADE,
                related_name="caratteristiche_procedura",
                to="articoli.lavorazioneesterna",
            ),
        ),

        # 10. Aggiorna CaratteristicaProcedura: related_name su fk_dettaglio_fase_lavoro
        migrations.AlterField(
            model_name="caratteristicaprocedura",
            name="fk_dettaglio_fase_lavoro",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.deletion.CASCADE,
                related_name="caratteristiche_procedura",
                to="articoli.dettagliofaselavoro",
            ),
        ),

        # 11. Aggiungi UniqueConstraint su Procedura
        migrations.AddConstraint(
            model_name="procedura",
            constraint=models.UniqueConstraint(
                fields=["fk_articolo", "nr_procedura", "nr_revisione"],
                name="ux_procedura_articolo_nr_rev",
            ),
        ),

        # 12. Aggiungi UniqueConstraint su DettaglioProcedura
        migrations.AddConstraint(
            model_name="dettaglioprocedura",
            constraint=models.UniqueConstraint(
                fields=["fk_procedura", "numero_riga"],
                name="ux_dettaglio_procedura_riga",
            ),
        ),

        # 13. Aggiungi UniqueConstraint su CaratteristicaProcedura
        migrations.AddConstraint(
            model_name="caratteristicaprocedura",
            constraint=models.UniqueConstraint(
                fields=["fk_dettaglio_procedura", "numero_riga"],
                name="ux_caratteristica_procedura_riga",
            ),
        ),
    ]

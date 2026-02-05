"""
Migration: Aggiunge LwgRegione, LwgSubregione, Nazione, LottoOrigine.
Migra created_by da User diretto a settings.AUTH_USER_MODEL.
"""
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
import django.db.models.functions


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("acquistopelli", "0011_alter_lotto_fk_macello"),
    ]

    operations = [
        # ------------------------------------------------------------------
        # Migra created_by esistenti a settings.AUTH_USER_MODEL
        # ------------------------------------------------------------------
        migrations.AlterField(
            model_name="tipoanimale",
            name="created_by",
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="animale",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="tipogrezzo",
            name="created_by",
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="grezzo",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="scelta",
            name="created_by",
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="scelta",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="lotto",
            name="created_by",
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="lotto",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="sceltalotto",
            name="created_by",
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="sceltalotto",
                to=settings.AUTH_USER_MODEL,
            ),
        ),

        # ------------------------------------------------------------------
        # LwgRegione
        # ------------------------------------------------------------------
        migrations.CreateModel(
            name="LwgRegione",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("codice_m49", models.IntegerField(blank=True, null=True, unique=True)),
                ("nome_regione", models.CharField(max_length=255, unique=True)),
            ],
            options={
                "verbose_name_plural": "regioni LWG",
                "ordering": ["nome_regione"],
                "db_table": "lwg_regioni",
            },
        ),

        # ------------------------------------------------------------------
        # LwgSubregione
        # ------------------------------------------------------------------
        migrations.CreateModel(
            name="LwgSubregione",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("codice_m49", models.IntegerField(blank=True, null=True, unique=True)),
                ("nome_subregione", models.CharField(max_length=255, unique=True)),
                (
                    "regione",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="subregioni",
                        to="acquistopelli.lwgregione",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "subregioni LWG",
                "ordering": ["nome_subregione"],
                "db_table": "lwg_subregioni",
            },
        ),
        migrations.AddIndex(
            model_name="lwgsubregione",
            index=models.Index(fields=["regione"], name="idx_subregione_regione"),
        ),

        # ------------------------------------------------------------------
        # Nazione
        # ------------------------------------------------------------------
        migrations.CreateModel(
            name="Nazione",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("sigla_estesa", models.CharField(blank=True, max_length=255, null=True)),
                ("descrizione", models.CharField(blank=True, max_length=255, null=True)),
                ("sigla", models.CharField(blank=True, max_length=255, null=True)),
                ("codice_m49", models.IntegerField(blank=True, null=True)),
                (
                    "regione",
                    models.ForeignKey(
                        blank=True, null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="nazioni",
                        to="acquistopelli.lwgregione",
                    ),
                ),
                (
                    "subregione",
                    models.ForeignKey(
                        blank=True, null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="nazioni",
                        to="acquistopelli.lwgsubregione",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True, null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="nazione",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name_plural": "nazioni",
                "ordering": ["descrizione"],
                "db_table": "tbl_Nazioni",
            },
        ),
        migrations.AddIndex(
            model_name="nazione",
            index=models.Index(fields=["regione"], name="idx_nazione_regione"),
        ),
        migrations.AddIndex(
            model_name="nazione",
            index=models.Index(fields=["subregione"], name="idx_nazione_subregione"),
        ),
        migrations.AddConstraint(
            model_name="nazione",
            constraint=models.UniqueConstraint(
                django.db.models.functions.Lower("sigla"),
                name="ux_nazione_iso2_lower",
            ),
        ),
        migrations.AddConstraint(
            model_name="nazione",
            constraint=models.UniqueConstraint(
                django.db.models.functions.Upper("sigla_estesa"),
                name="ux_nazione_iso3_upper",
            ),
        ),

        # ------------------------------------------------------------------
        # LottoOrigine
        # ------------------------------------------------------------------
        migrations.CreateModel(
            name="LottoOrigine",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("quota_percentuale", models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ("qta_stimata", models.DecimalField(blank=True, decimal_places=3, max_digits=12, null=True)),
                ("livello_rischio", models.CharField(blank=True, max_length=20, null=True)),
                ("fonte_dato", models.TextField(blank=True, null=True)),
                ("note", models.TextField(blank=True, null=True)),
                (
                    "livello_precisione",
                    models.CharField(
                        choices=[("country", "country"), ("region", "region"), ("subregion", "subregion")],
                        default="country",
                        max_length=20,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "lotto",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="origini",
                        to="acquistopelli.lotto",
                    ),
                ),
                (
                    "nazione",
                    models.ForeignKey(
                        blank=True, null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="acquistopelli.nazione",
                    ),
                ),
                (
                    "regione",
                    models.ForeignKey(
                        blank=True, null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="acquistopelli.lwgregione",
                    ),
                ),
                (
                    "subregione",
                    models.ForeignKey(
                        blank=True, null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="acquistopelli.lwgsubregione",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True, null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="lottoorigine",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "origini lotto",
                "db_table": "lot_origini",
            },
        ),
        migrations.AddIndex(
            model_name="lottoorigine",
            index=models.Index(fields=["lotto"], name="idx_lottoorigine_lotto"),
        ),
        migrations.AddIndex(
            model_name="lottoorigine",
            index=models.Index(fields=["nazione"], name="idx_lottoorigine_nazione"),
        ),
        migrations.AddIndex(
            model_name="lottoorigine",
            index=models.Index(fields=["regione"], name="idx_lottoorigine_regione"),
        ),
        migrations.AddIndex(
            model_name="lottoorigine",
            index=models.Index(fields=["subregione"], name="idx_lottoorigine_subreg"),
        ),
        migrations.AddConstraint(
            model_name="lottoorigine",
            constraint=models.CheckConstraint(
                check=models.Q(("nazione__isnull", False))
                | models.Q(("regione__isnull", False))
                | models.Q(("subregione__isnull", False)),
                name="chk_lottoorigine_valid",
            ),
        ),
    ]

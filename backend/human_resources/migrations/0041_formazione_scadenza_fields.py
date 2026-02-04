# Generated manually for formazione scadenza fields
# human_resources 0041

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    """
    Migrazione per aggiungere:
    - validita_mesi a CorsoFormazione
    - scadenza_calcolata, scadenza_override, created_by a DettaglioRegistroFormazione
    - Indice per lookup (hr, registro)
    """

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('human_resources', '0040_hr_safety_idx_hr_safety_lookup'),
    ]

    operations = [
        # Aggiungi validita_mesi a CorsoFormazione
        migrations.AddField(
            model_name='corsoformazione',
            name='validita_mesi',
            field=models.PositiveIntegerField(
                default=12,
                help_text='Validità del corso in mesi (es. 12, 24, 36)'
            ),
        ),

        # Aggiungi scadenza_calcolata a DettaglioRegistroFormazione
        migrations.AddField(
            model_name='dettaglioregistroformazione',
            name='scadenza_calcolata',
            field=models.DateField(
                blank=True,
                null=True,
                help_text='Calcolata automaticamente: data_formazione + validita_mesi del corso'
            ),
        ),

        # Aggiungi scadenza_override a DettaglioRegistroFormazione
        migrations.AddField(
            model_name='dettaglioregistroformazione',
            name='scadenza_override',
            field=models.DateField(
                blank=True,
                null=True,
                help_text='Scadenza manuale che sovrascrive il calcolo automatico'
            ),
        ),

        # Aggiungi created_by a DettaglioRegistroFormazione
        migrations.AddField(
            model_name='dettaglioregistroformazione',
            name='created_by',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='dettaglio_registro_formazione',
                to=settings.AUTH_USER_MODEL,
            ),
        ),

        # Aggiungi created_at a DettaglioRegistroFormazione
        migrations.AddField(
            model_name='dettaglioregistroformazione',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),

        # Aggiungi updated_at a DettaglioRegistroFormazione
        migrations.AddField(
            model_name='dettaglioregistroformazione',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),

        # Aggiungi indice per lookup (hr, registro)
        migrations.AddIndex(
            model_name='dettaglioregistroformazione',
            index=models.Index(
                fields=['fk_hr', 'fk_registro_formazione'],
                name='idx_dettaglio_hr_registro'
            ),
        ),

        # Aggiungi related_name a fk_registro_formazione se non presente
        migrations.AlterField(
            model_name='dettaglioregistroformazione',
            name='fk_registro_formazione',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='dettagli',
                to='human_resources.registroformazione',
            ),
        ),

        # Aggiungi related_name a fk_hr se non presente
        migrations.AlterField(
            model_name='dettaglioregistroformazione',
            name='fk_hr',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='dettagli_formazione',
                to='human_resources.humanresource',
            ),
        ),
    ]

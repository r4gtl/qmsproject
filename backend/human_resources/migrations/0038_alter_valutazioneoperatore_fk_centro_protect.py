# Generated manually - Change FK on_delete from CASCADE to PROTECT

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('human_resources', '0037_valutazioneoperatore_ux_valutazione_hr_centro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='valutazioneoperatore',
            name='fk_centro_di_lavoro',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to='human_resources.centrodilavoro'
            ),
        ),
    ]

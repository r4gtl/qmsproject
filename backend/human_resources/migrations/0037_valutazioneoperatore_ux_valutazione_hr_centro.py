# Generated manually for UniqueConstraint on ValutazioneOperatore

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('human_resources', '0036_alter_registroorelavoro_entry_month'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='valutazioneoperatore',
            constraint=models.UniqueConstraint(
                fields=['fk_hr', 'fk_centro_di_lavoro'],
                name='ux_valutazione_hr_centro'
            ),
        ),
    ]

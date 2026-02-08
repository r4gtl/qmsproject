# Generated manually - Add company field to manutenzioni models

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_create_default_company'),
        ('manutenzioni', '0012_attrezzatura_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='attrezzatura',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_set', to='accounts.company', verbose_name='Azienda'),
        ),
        migrations.AddField(
            model_name='manutenzionestraordinaria',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_set', to='accounts.company', verbose_name='Azienda'),
        ),
        migrations.AddField(
            model_name='manutenzioneordinaria',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_set', to='accounts.company', verbose_name='Azienda'),
        ),
        migrations.AddField(
            model_name='taratura',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_set', to='accounts.company', verbose_name='Azienda'),
        ),
        migrations.AddField(
            model_name='controlloperiodico',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_set', to='accounts.company', verbose_name='Azienda'),
        ),
    ]

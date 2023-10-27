# Generated by Django 4.2.1 on 2023-10-26 13:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('air_emissions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrocontrolloanalitico',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='registrocontrolloanalitico',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='registro_controllo_analitico', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='registrocontrolloanalitico',
            name='note',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='registrocontrolloanalitico',
            name='prossima_scadenza',
            field=models.DateField(blank=True, null=True),
        ),
    ]
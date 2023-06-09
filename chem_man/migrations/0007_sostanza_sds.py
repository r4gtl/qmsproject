# Generated by Django 4.2.1 on 2023-07-12 14:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chem_man', '0006_schedasicurezza_simbologhs_sds_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sostanza_SDS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('concentrazione', models.CharField(max_length=50)),
                ('note', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sostanza_sds', to=settings.AUTH_USER_MODEL)),
                ('fk_sds', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sostanza_sds', to='chem_man.schedasicurezza')),
                ('fk_sostanza', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sostanza_sds', to='chem_man.sostanza')),
            ],
        ),
    ]

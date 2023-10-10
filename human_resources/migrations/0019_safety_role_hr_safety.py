# Generated by Django 4.2.1 on 2023-09-20 12:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('human_resources', '0018_alter_registroorelavoro_entry_month'),
    ]

    operations = [
        migrations.CreateModel(
            name='Safety_Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descrizione', models.CharField(max_length=100)),
                ('note', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='safety_role', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HR_Safety',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_inizio_incarico', models.DateField()),
                ('data_fine_incarico', models.DateField(blank=True, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hr_safety', to=settings.AUTH_USER_MODEL)),
                ('fk_hr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hr_safety', to='human_resources.humanresource')),
                ('fk_safety_role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hr_safety', to='human_resources.safety_role')),
            ],
            options={
                'ordering': ['fk_hr'],
            },
        ),
    ]
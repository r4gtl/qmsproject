# Generated by Django 4.2.1 on 2023-11-15 14:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('antincendio', '0008_estintore_certificato_conf_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attrezzaturaantincendio',
            options={'ordering': ['descrizione'], 'verbose_name_plural': 'Attrezzature Antincendio'},
        ),
        migrations.AlterModelOptions(
            name='estintore',
            options={'ordering': ['numero_posizione'], 'verbose_name_plural': 'Estintori'},
        ),
        migrations.AlterModelOptions(
            name='idrante',
            options={'ordering': ['numero_posizione'], 'verbose_name_plural': 'Idranti'},
        ),
        migrations.AlterModelOptions(
            name='impiantospegnimento',
            options={'ordering': ['numero_posizione'], 'verbose_name_plural': 'Impianti Spegnimento'},
        ),
        migrations.AlterModelOptions(
            name='portauscita',
            options={'ordering': ['numero_posizione'], 'verbose_name_plural': 'Porte Uscita'},
        ),
    ]

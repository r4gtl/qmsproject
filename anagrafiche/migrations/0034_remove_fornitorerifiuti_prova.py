# Generated by Django 4.2.1 on 2024-10-04 14:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anagrafiche', '0033_xrdocumentigestore_data_documento_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fornitorerifiuti',
            name='prova',
        ),
    ]

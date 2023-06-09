# Generated by Django 4.2.1 on 2023-06-05 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("human_resources", "0006_alter_humanresource_immagine"),
    ]

    operations = [
        migrations.AlterField(
            model_name="humanresource",
            name="immagine",
            field=models.ImageField(
                blank=True,
                default="avatar.png",
                null=True,
                upload_to="operator_pictures",
            ),
        ),
    ]

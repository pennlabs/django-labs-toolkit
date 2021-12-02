# Generated by Django 2.1.2 on 2018-10-28 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Url",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("long_url", models.TextField()),
                ("short_id", models.TextField()),
            ],
        )
    ]

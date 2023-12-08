# Generated by Django 4.2.3 on 2023-09-06 09:54

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("booking", "0009_alter_contactreply_reply_date"),
    ]

    operations = [
        migrations.CreateModel(
            name="Holiday",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "date",
                    models.DateField(
                        default=datetime.datetime.now, unique=True
                    ),
                ),
            ],
            options={
                "ordering": ["-date"],
            },
        ),
    ]
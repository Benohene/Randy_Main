# Generated by Django 4.2.3 on 2023-09-05 00:18

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("booking", "0005_contact_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contact",
            name="date",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]

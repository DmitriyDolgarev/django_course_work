# Generated by Django 5.1 on 2024-09-24 05:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0006_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cars.country'),
        ),
    ]

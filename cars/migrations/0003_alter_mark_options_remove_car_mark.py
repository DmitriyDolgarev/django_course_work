# Generated by Django 5.1 on 2024-09-10 04:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0002_mark_alter_car_options_alter_car_mark_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mark',
            options={'verbose_name': 'Марка автомобиля', 'verbose_name_plural': 'Марки автомобилей'},
        ),
        migrations.RemoveField(
            model_name='car',
            name='mark',
        ),
    ]

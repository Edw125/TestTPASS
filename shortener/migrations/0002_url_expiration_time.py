# Generated by Django 3.2.15 on 2022-08-20 19:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='url',
            name='expiration_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 21, 19, 4, 26, 43835)),
        ),
    ]

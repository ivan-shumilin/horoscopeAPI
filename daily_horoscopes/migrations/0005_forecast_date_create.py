# Generated by Django 4.0.3 on 2022-03-23 09:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daily_horoscopes', '0004_remove_forecast_day_forecast_sing'),
    ]

    operations = [
        migrations.AddField(
            model_name='forecast',
            name='date_create',
            field=models.DateField(default=datetime.date.today),
        ),
    ]

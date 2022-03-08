import json

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.dateparse import parse_date

from daily_horoscopes.models import Forecast


class Command(BaseCommand):  # https://docs.djangoproject.com/en/4.0/howto/custom-management-commands/
    help = 'Load forecast to db'

    @transaction.atomic  # инструмент управления транзакциями базы данных
    def handle(self, *args, **options):
        Forecast.objects.all().delete()  # очищаем базу данных перед тем как заполнить таблицу

        with open('daily_horoscopes/fixtures/forecast.json') as file:
            forecasts = json.load(file)  # метод считывает файл в формате JSON и возвращает объекты Python

        to_create = []  # плохая практика обращатьтся к базе в цикле.
        for forecast in forecasts:
            to_create.append(Forecast(
                forecast=forecast['forecast'],
                ))
        Forecast.objects.bulk_create(to_create)  # одним действием отправляем все в базу
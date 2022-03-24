import json

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.dateparse import parse_date

from daily_horoscopes.models import Forecast

import fake_useragent
import requests
from bs4 import BeautifulSoup


def parsing():
    """ Парсинг гороскопа  """
    # меняем каждый раз user agent
    user = fake_useragent.UserAgent().random
    header = {'user-agent': user}
    link = 'https://www.astrocentr.ru/index.php?przd=horoe&str=index'
    forecast_item = {}
    forecasts = []
    response = requests.get(link, headers=header).text
    soup = BeautifulSoup(response, 'lxml')
    # парсим общий прогноз для всез знаков
    block = soup.find('div', class_="main_text")
    forecast_item['sing'] = 'general'
    forecast_item['description'] = block.find('p').get_text()
    forecasts.append(forecast_item.copy())

    # парсим ежедневный прогноз для каждого знака зодиака
    for i in range(1, 13):
        id = 'horo' + str(i)
        desc = soup.find('div', id=id)
        forecast_item['sing'] = desc.find('legend', class_="uv_legend").get_text()
        forecast_item['description'] = desc.find('p').get_text()
        forecasts.append(forecast_item.copy())
    return forecasts

class Command(BaseCommand):  # https://docs.djangoproject.com/en/4.0/howto/custom-management-commands/
    help = 'Load forecast to db'

    @transaction.atomic  # инструмент управления транзакциями базы данных
    def handle(self, *args, **options):
        Forecast.objects.all().delete()  # очищаем базу данных перед тем как заполнить таблицу
        forecasts = parsing()
        print(forecasts)
        to_create = []  # плохая практика обращатьтся к базе в цикле.
        for forecast in forecasts:
            to_create.append(Forecast(
                sing=forecast['sing'],
                description=forecast['description'],
                ))
        Forecast.objects.bulk_create(to_create)  # одним действием отправляем все в базу
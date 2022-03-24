from django.shortcuts import render
from django.http import HttpResponse
from .models import Forecast

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ForecastSerializer
import calendar, datetime

import json


from django.db import transaction
from django.utils.dateparse import parse_date


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



@transaction.atomic  # инструмент управления транзакциями базы данных
def load_forecast():
    Forecast.objects.all().delete()  # очищаем базу данных перед тем как заполнить таблицу
    forecasts = parsing()
    print(forecasts)
    to_create = []  # плохая практика обращатьтся к базе в цикле.
    for forecast in forecasts:
        to_create.append(Forecast(
            sing=forecast['sing'],
            description=forecast['description'],
        ))
    Forecast.objects.bulk_create(to_create)


# Представление на основе класса ListCreateAPIView
# class GetForecastInfoView(generics.ListCreateAPIView):
#     queryset = Forecast.objects.all()
#     serializer_class = ForecastSerializer

# Представление на основе класса APIView
class GetForecastInfoView(APIView):

    def get(self, request):
        # если в базе есть запись созданная сегодня берем данные с модели
        # если нет парсим и записываем новые данные в модель
        date_last_parse = Forecast.objects.all()[0].date_create
        if datetime.date.today() == date_last_parse:
            queryset = Forecast.objects.all()
        else:
            # парсим и записываем
            load_forecast()
            queryset = Forecast.objects.all()
        # Сериализуем данныеа
        serializer_for_queryset = ForecastSerializer(queryset, many=True).data
        return Response(serializer_for_queryset)


def index(request):
    """
    Функция для отображения на главной странице списка всех записей.
    """
    today = str.lower(calendar.day_name[datetime.datetime.today().isoweekday()])
    list_of_forecast = Forecast.objects.all()
    context = {'list_of_forecast': list_of_forecast,
               'today': datetime.date.today(),
              }
    return render(
        request=request,
        template_name='daily_horoscopes/index.html',
        context=context
    )

# Какой сегодня день недели
# calendar.day_name[datetime.datetime.today().isoweekday()]

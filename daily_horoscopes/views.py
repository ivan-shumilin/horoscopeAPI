from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Forecast
from .forms import UserRegistrationForm


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

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from django.views.decorators.csrf import csrf_exempt  # потом убрать


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
    list_of_forecast = Forecast.objects.all()
    context = {'list_of_forecast': list_of_forecast,
               'today': datetime.date.today(),
               'tokens': tokens,
               }
    return render(
        request=request,
        template_name='index.html',
        context=context
    )


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            url = 'http://127.0.0.1:8000/api/v1/auth/users/'
            headers = {'content-type': 'application/json'}
            payload = {
                'email': user_form.cleaned_data['email'],
                'username': user_form.cleaned_data['username'],
                'password': user_form.cleaned_data['password'],
            }
            requests.post(url, headers=headers, json=payload)
            return render(request, 'registration/register_done.html', {'new_user': user_form.cleaned_data})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})

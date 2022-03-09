from django.shortcuts import render
from django.http import HttpResponse
from .models import Forecast

from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ForecastSerializer
import calendar, datetime


# Create your views here.
class GetForecastInfoView(APIView):
    def get(self, request):
        # Извлекаем набор всех записей из таблицы Forecast
        today = str.lower(calendar.day_name[datetime.datetime.today().isoweekday()])
        # queryset = Forecast.objects.get(day=today)
        queryset = Forecast.objects.filter(day=today)
        # Создаём сериалайзер для извлечённого наборa записей
        serializer_for_queryset = ForecastSerializer(
            instance=queryset,  # Передаём набор записей
            many=True
        )
        return Response(serializer_for_queryset.data)


def index(request):
    """
    Контроллер для отображения на главной странице списка всех записей.
    """
    today = str.lower(calendar.day_name[datetime.datetime.today().isoweekday()])
    list_of_forecast = Forecast.objects.get(day=today)
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

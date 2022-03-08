from django.urls import path

from . import views

urlpatterns = [
    path('api/forecast/', views.GetForecastInfoView.as_view()),
    path('', views.index, name='index'),
]

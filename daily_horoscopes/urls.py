from django.urls import path, re_path, include


from . import views

urlpatterns = [
    path('api/forecast/', views.GetForecastInfoView.as_view()),
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
]

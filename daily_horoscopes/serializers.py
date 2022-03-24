import io

from rest_framework import serializers
from .models import Forecast


class ForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forecast
        fields = ("sing", "description", "date_create")

# class ForecastSerializer(serializers.Serializer):
#     sing = serializers.CharField(max_length=5000)
#     description = serializers.CharField(max_length=5000)

from rest_framework import serializers


class ForecastSerializer(serializers.Serializer):
    a = serializers.CharField(source='forecast', max_length=5000)

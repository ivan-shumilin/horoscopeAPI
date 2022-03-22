from rest_framework import serializers


class ForecastSerializer(serializers.Serializer):
    sing = serializers.CharField(max_length=5000)
    description = serializers.CharField(max_length=5000)

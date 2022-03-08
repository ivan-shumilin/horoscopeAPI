from django.db import models

# Create your models here.
class Forecast(models.Model):
    forecast = models.CharField(max_length=5000)

    def __str__(self):
        return self.forecast

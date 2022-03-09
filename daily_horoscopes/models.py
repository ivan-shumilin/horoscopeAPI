from django.db import models

# Create your models here.
class Forecast(models.Model):
    # forecast = models.CharField(max_length=5000)
    day = models.CharField(max_length=5000, null=True)
    description = models.CharField(max_length=5000, null=True)

    def __str__(self):
        return f'{self.day} - {self.description}'

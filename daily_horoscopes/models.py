from django.db import models
from datetime import date

# Create your models here.
class Forecast(models.Model):
    # forecast = models.CharField(max_length=5000)
    sing = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=5000, null=True)
    date_create = models.DateField(default=date.today)

    def __str__(self):
        return f'{self.sing} - {self.description}'

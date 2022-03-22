from django.db import models

# Create your models here.
class Forecast(models.Model):
    # forecast = models.CharField(max_length=5000)
    sing = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=5000, null=True)

    def __str__(self):
        return f'{self.sing} - {self.description}'

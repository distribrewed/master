from django.db import models


class TemperatureSchedule(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class TemperatureTime(models.Model):
    schedule = models.ForeignKey(TemperatureSchedule, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    temperature = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return '{} : {}°C'.format(self.timestamp, self.temperature)

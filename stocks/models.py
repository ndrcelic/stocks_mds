from django.db import models

class Stock(models.Model):
    name = models.CharField(max_length=100)
    date_of_creation = models.DateTimeField(auto_now_add=True)
    abbreviation = models.CharField(max_length=5)

    def __str__(self):
        return self.name


class DatesValues(models.Model):
    date = models.DateField()
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    adj_close = models.FloatField()
    volume = models.BigIntegerField()
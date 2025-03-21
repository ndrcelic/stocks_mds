from django.db import models

class Stock(models.Model):
    name = models.CharField(max_length=100, unique=True)
    date_of_creation = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    abbreviation = models.CharField(max_length=5, blank=True, null=True)

    def __str__(self):
        return self.name


class DatesValues(models.Model):
    date = models.DateField()
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    open = models.FloatField(blank=True, null=True)
    high = models.FloatField(blank=True, null=True)
    low = models.FloatField(blank=True, null=True)
    close = models.FloatField(blank=True, null=True)
    adj_close = models.FloatField(blank=True, null=True)
    volume = models.BigIntegerField(blank=True, null=True)

    class Meta:
        unique_together = ('date', 'stock')
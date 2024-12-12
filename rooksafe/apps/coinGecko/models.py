from django.db import models

# Create your models here.
class Cryptocurrency(models.Model):
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=10)
    price = models.FloatField()
    change_1h = models.FloatField()
    change_24h = models.FloatField()
    change_7d = models.FloatField()
    market_cap = models.BigIntegerField()
    volume_24h = models.BigIntegerField()
    icon_url = models.URLField()
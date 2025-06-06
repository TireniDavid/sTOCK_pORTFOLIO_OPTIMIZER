from django.db import models
import yfinance as yf
from django.contrib.auth.models import User



class Stock_Group(models.Model):
    name = models.CharField(max_length=100)  # e.g., Dow30, S&P500, etc

class Stock(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    sector = models.CharField(max_length=10)

    # Many-to-many relationship with StockGroup
    groups = models.ManyToManyField(Stock_Group, related_name="stocks")

class Portfolio(models.Model):
    name = models.CharField(max_length=100)
    drag_percentage = models.FloatField(default=0)
    rebalance_frequency = models.CharField(max_length=10, choices=[
            ('Yearly', 'Yearly'),
            ('Quarterly', 'Quarterly'),
            ('Monthly', 'Monthly')
        ], default='Yearly')
    total_return = models.BooleanField(default=False)
    rebalance_bands = models.BooleanField(default=False)
    ticker = models.CharField(max_length=100)
    allocation = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_default:
            Portfolio.objects.exclude(id=self.id).update(is_default=False)
        super(Portfolio, self).save(*args, **kwargs)

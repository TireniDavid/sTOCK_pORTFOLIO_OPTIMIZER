from django.db import models
import yfinance as yf



class Stock_Group(models.Model):
    name = models.CharField(max_length=100)  # e.g., Dow30, S&P500, etc

class Stock(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    sector = models.CharField(max_length=10)

    # Many-to-many relationship with StockGroup
    groups = models.ManyToManyField(Stock_Group, related_name="stocks")



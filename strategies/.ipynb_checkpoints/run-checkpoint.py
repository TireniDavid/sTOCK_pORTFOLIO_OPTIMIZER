#Price,Adj Close,Close,High,Low,Open,Volume
import os, sys, argparse
import pandas as pd
import backtrader as bt


cerebro= bt.Cerebro()
cerebro.broker.setcash(10000)


numeric_columns = ['Price', 'Adj Close', 'Close', 'High', 'Low', 'Open', 'Volume']
spy_prices[numeric_columns] = spy_prices[numeric_columns].apply(pd.to_numeric, errors='coerce')

feed = bt.feeds.PandasData(dataname=spy_prices)

cerebro.adddata(feed)
#implementing the golden cross strategy 
#specifically when a 50-day moving average crosses over the 200 day moving average
#buying when the 50-day moving average crosses over the 200 moving average upwardly
#selling when the 200-day moving average crosses down the 50-day moving average downwardly

import yfinance as yf
import os, sys, argparse
import pandas as pd
import backtrader as bt
import math

# Download SPY data
data = yf.download('SPY', start='1993-01-01', end='2020-02-16')
print(data.head())

# Get Rid of ticker columnn
if isinstance(data.columns, pd.MultiIndex):
    # Flatten the MultiIndex by using the second level as column names
    data.columns = data.columns.get_level_values(0)
    print(data.head())

# Resetting the index (so that date column is in the proper place)
data.reset_index(inplace=True)
print(data.head())

# Reorder the columns to match the desired order
data = data[['Date', 'Open', 'High', 'Low', 'Adj Close', 'Volume']]
print(data.head())




class GoldenCross(bt.Strategy):
    params = (('fast',50),('slow',200), ('order_percentage',0.95),('ticker', 'SPY'))
    
    #initialize indicators
    def __init__(self):
        #50-day moving average
        self.fast_moving_average = bt.indicators.SMA(
            self.data.close, period = self.params.fast, plotname = '50 day moving average'
        )
        
        #200-day moving average
        self.slow_moving_average = bt.indicators.SMA(
            self.data.close, period =self.params.slow, plotname='200 day moving average'
        )
       
        #Crossover indicator                      50-ma crosses above 200-ma
        self.crossover =bt.indicators.CrossOver(self.fast_moving_average, self.slow_moving_average)
    
    def next(self):
        pass


parsed_data= bt.feeds.PandasData(dataname=data, 
    datetime='Date',  # Name of the Date column
    open='Open',      # Name of the Open column
    high='High',      # Name of the High column
    low='Low',        # Name of the Low column
    close='Adj Close',# Name of the Adjusted Close column
    volume='Volume',  # Name of the Volume column
    openinterest=-1)

cerebro= bt.Cerebro()
cerebro.broker.setcash(10000)

cerebro.adddata(parsed_data)

cerebro.run()
cerebro.plot()
























'''
#50-day moving average
data['ma_50'] = data['Close'].rolling(window=50).mean()

#200-day moving average
data['ma_200'] = data['Close'].rolling(window=200).mean()
'''

'''
with open('/Users/tireniadekoya/desktop/ai-trader/my_app/data/SPY_data.csv') as f:
    content=f.readlines()
    for line in content:
        tokens= line.split(',')
        close = tokens[2]
        closing_price_sum +=float(close)
        print(close)
        print(line)
    print(f"closing_price_sum: {closing_price_sum}")
    print(f"closing_price_200_average: {closing_price_sum/200}")
'''
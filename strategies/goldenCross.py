#implementing the golden cross strategy 
#specifically when a 50-day moving average crosses over the 200 day moving average
#buying when the 50-day moving average crosses over the 200 moving average upwardly
#selling when the 200-day moving average crosses down the 50-day moving average downwardly

import yfinance as yf
import os, sys, argparse
import pandas as pd
import backtrader as bt
import math
import json


# Download SPY data
data = yf.download('SPY', start='1993-01-01', end='2020-02-16')


# Get Rid of ticker columnn
if isinstance(data.columns, pd.MultiIndex):
    # Flatten the MultiIndex by using the second level as column names
    data.columns = data.columns.get_level_values(0)
    

# Resetting the index (so that date column is in the proper place)
data.reset_index(inplace=True)


# Reorder the columns to match the desired order
data = data[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
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

        # To store data for export
        self.data_to_export = []

    
    def next(self):
        # Save OHLC and indicators for each bar
        bar_data = {
            'date': self.data.datetime.date(0).isoformat(),  # Get the date of the bar
            'open': self.data.open[0],  # Open price
            'high': self.data.high[0],  # High price
            'low': self.data.low[0],    # Low price
            'close': self.data.close[0],  # Close price
            'sma_50': self.fast_moving_average[0],  # 50-day SMA
            'sma_200': self.slow_moving_average[0]  # 200-day SMA
        }

        # Save data for each bar 
        self.data_to_export.append(bar_data)
        
        
        #Existing Logic

        # If faster ma crosses upward
        # check position size
        if self.position.size == 0:
            if self.crossover > 0:
                # only buy up to 95% of portfolio
                amount_to_invest = (self.params.order_percentage * self.broker.cash)
                #share size
                self.size = math.floor(amount_to_invest / self.data.close[0])
                
                # closing price of the the current bar: self.data.close[0]
                print(f"Buy {self.size} shares of {self.params.ticker} at {self.data.close[0]}")

                # Execute the buy order
                self.buy(size=self.size)
        
        # If faster ma crosses downward
        if self.position.size > 0:
            if self.crossover < 0:
                print(f"Position size: {self.position.size}")
                print(f"Sell {self.size} shares of {self.params.ticker} at {self.data.close[0]} money-worth: {self.size * self.data.close[0]} ")
                self.close() # Close the position (sell all shares)
    
    # at the end of the backtesting process
    def stop(self):
        # Save the collected data as a JSON file
        os.makedirs('static/data', exist_ok=True)

        with open('static/data/golden_cross_data.json', 'w') as f:
            json.dump(self.data_to_export, f, indent=4)
        print("Exported data to 'static/data/golden_cross_data.json'")



parsed_data= bt.feeds.PandasData(dataname=data, 
    datetime='Date',  # Name of the Date column
    open='Open',      # Name of the Open column
    high='High',      # Name of the High column
    low='Low',        # Name of the Low column
    close='Close',    # Name of the Close column
    volume='Volume',  # Name of the Volume column
    openinterest=-1)

cerebro= bt.Cerebro()
cerebro.broker.setcash(100000)

cerebro.adddata(parsed_data)
cerebro.addstrategy(GoldenCross)

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
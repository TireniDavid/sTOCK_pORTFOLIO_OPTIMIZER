import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import StringIO

'''
def download_n_clean_data(symbol, start_date, end_date):
    """
    Downloads and cleans historical stock data for a given symbol and date range.

    Parameters:
        symbol (str): Stock symbol (default is 'SPY').
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.

    Returns:
        pd.DataFrame: Cleaned stock data.
    """
    # Download SPY data
    data = yf.download(symbol, start=start_date, end=end_date)
    
    # Get Rid of ticker columnn
    if isinstance(data.columns, pd.MultiIndex):
        # Flatten the MultiIndex by using the second level as column names
        data.columns = data.columns.get_level_values(0)
        
    # Resetting the index (so that date column has its own index)
    data.reset_index(inplace=True)
    
    # Reorder the columns to match the desired order
    data = data[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]

    data['Date'] = pd.to_datetime(data['Date'])  # Ensure Date is in datetime format

    #convert timestamp time to unix time
    #data['Date'] = data['Date'].apply(lambda x: x.timestamp())

    return data
#print(download_n_clean_data('SPY', '1993-01-01', '2020-02-16'))




def backtest():
    # Set the symbol and date range
    symbol = 'SPY'
    start_date = '1993-01-01'
    end_date = '2020-02-16'
    
    # Get the cleaned data
    clean_data = download_n_clean_data(symbol, start_date, end_date)
    
    # Pass the data to the template
    context = {'data': clean_data.to_dict(orient='records')}  # Convert DataFrame to a dictionary

    

    # Pass the data to the template
    #return render(request, 'backtest.html', context)
    return context
print(backtest())
'''
url= 'https://www.dogsofthedow.com/dow-jones-industrial-average-companies.htm'

# Send HTTP request to get the page content
response = requests.get(url)

if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, "lxml")

    # Find the table with the Dow 30 components
    table = soup.find('table', {'class': 'tablepress tablepress-id-42 tablepress-responsive'})

    pulled_df = pd.read_html(str(table))[0]

    print(pulled_df)

    # Access a specific column by its name
    column_data = pulled_df[['Company','Symbol']]
    print(column_data)

    my_dict1 = {}

    list_st = []

   
    my_dict1['Dow Jones 30'] = list_st

    

    for index, row in column_data.iterrows():
        my_dict2= {}
        company = row['Company']
        symbol = row['Symbol']
        my_dict2['name'] = company
        my_dict2['symbol'] = symbol

        list_st.append(my_dict2)
    print(my_dict1)




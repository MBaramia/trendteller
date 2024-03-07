import requests
import pandas as pd

def fetch_historic_data(symbol, api_key, timeframe):
    function_mapping = {
        'intraday': 'TIME_SERIES_INTRADAY',
        'daily': 'TIME_SERIES_DAILY',
        'weekly': 'TIME_SERIES_WEEKLY',
        'monthly': 'TIME_SERIES_MONTHLY'
    }
    interval = '60min'  # Adjust if necessary for intraday
    function = function_mapping.get(timeframe)
    url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={api_key}"
    if timeframe == 'intraday':
        url += f"&interval={interval}"

    response = requests.get(url)
    data = response.json()
    data_key = list(data.keys())[1]
    df = pd.DataFrame(data[data_key]).T
    df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    df.index = pd.to_datetime(df.index)
    df = df.sort_index(ascending=True)
    
    return df

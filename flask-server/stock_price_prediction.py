import requests
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense
import numpy as np

def fetch_stock_prediction(company_id, timeframe):
    def build_model(input_shape):
        model = Sequential()
        model.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))
        model.add(LSTM(units=50))
        model.add(Dense(5))  # Predicting 5 values: open, high, low, close, volume
        model.compile(optimizer='adam', loss='mean_squared_error')
        return model

    def create_sequences(data, sequence_length):
        xs, ys = [], []
        for i in range(len(data) - sequence_length):
            x = data[i:(i + sequence_length)]
            y = data[i + sequence_length]
            xs.append(x)
            ys.append(y)
        return np.array(xs), np.array(ys)

    def fetch_stock_data(symbol, api_key, timeframe):
        function_mapping = {
            'intraday': 'TIME_SERIES_INTRADAY',
            'daily': 'TIME_SERIES_DAILY',
            'weekly': 'TIME_SERIES_WEEKLY',
            'monthly': 'TIME_SERIES_MONTHLY'
        }
        function = function_mapping.get(timeframe, 'TIME_SERIES_INTRADAY')
        interval = '60min' if timeframe == 'intraday' else ''
        url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}{f'&interval={interval}' if interval else ''}&outputsize=full&apikey={api_key}"
        response = requests.get(url)
        data = response.json()
        if not data or len(data.keys()) < 2:
            print("Error fetching data or data not in expected format:", data)
            return pd.DataFrame()  
        key = list(data.keys())[1]
        df = pd.DataFrame(data[key]).T
        df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        df = df.astype(float)
        df.index = pd.to_datetime(df.index)
        df = df.sort_index(ascending=True)
        return df


    company_symbols = {
    0: 'AAPL',   # Apple
    1: 'AMZN',   # Amazon
    2: 'GOOGL',  # Alphabet Inc. (Google)
    3: 'MSFT',   # Microsoft
    4: 'TSLA',   # Tesla
    5: 'JPM',    # JPMorgan Chase
    6: 'WMT',    # Walmart
    7: 'KO',     # Coca-Cola
    8: 'PFE',    # Pfizer
    9: 'NFLX'    # Netflix
}

    symbol = company_symbols.get(company_id)
    api_key = '8WATTBIUUCY9LFYZ'
    stock_data = fetch_stock_data(symbol, api_key, timeframe)

    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(stock_data)
    sequence_length = 10
    X, _ = create_sequences(scaled_data, sequence_length)

    model = build_model((sequence_length, X.shape[2]))

    current_batch = X[-1:].reshape(1, sequence_length, X.shape[2])
    predicted = []
    for _ in range(7):
        predicted_step = model.predict(current_batch)[0]
        predicted.append(predicted_step)
        predicted_step = np.reshape(predicted_step, (1, 1, predicted_step.shape[0]))
        current_batch = np.append(current_batch[:, 1:, :], predicted_step, axis=1)
    
    predicted_prices = scaler.inverse_transform(predicted)
    predicted_prices[:, 4] = np.abs(predicted_prices[:, 4])
    predicted_prices[:, :4] = np.abs(predicted_prices[:, :4])
    # Print the predictions
    return predicted_prices

# Example usage
# company_id = 3  # This would be passed as a parameter
# timeframe = 'daily'  # This would be passed as a parameter
# predictions = fetch_stock_prediction(company_id, timeframe)

import requests
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense
import numpy as np
from datetime import timedelta

def fetch_stock_prediction(company_id, timeframe):
    def build_model(input_shape):
        model = Sequential()
        model.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))
        model.add(LSTM(units=50))
        model.add(Dense(units=5))  # Predicting 5 values: open, high, low, close, volume
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

    # Map of company IDs to stock symbols
    company_symbols = {
        0: 'AAPL', 1: 'AMZN', 2: 'GOOGL', 3: 'MSFT', 4: 'TSLA',
        5: 'JPM', 6: 'WMT', 7: 'KO', 8: 'PFE', 9: 'NFLX'
    }

    symbol = company_symbols.get(company_id)
    api_key = '8WATTBIUUCY9LFYZ'  # Replace 'YOUR_API_KEY' with your actual API key
    stock_data = fetch_stock_data(symbol, api_key, timeframe)

    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(stock_data[['Open', 'High', 'Low', 'Close', 'Volume']])
    sequence_length = 10
    X, _ = create_sequences(scaled_data, sequence_length)

    model = build_model((sequence_length, X.shape[2]))

    # Generate predictions
    current_batch = X[-1:].reshape(1, sequence_length, X.shape[2])
    predicted = []
    for i in range(7):
        predicted_step = model.predict(current_batch)[0]
        predicted.append(predicted_step)
        predicted_step = np.reshape(predicted_step, (1, 1, predicted_step.shape[0]))
        current_batch = np.append(current_batch[:, 1:, :], predicted_step, axis=1)

    predicted_prices = scaler.inverse_transform(predicted)

    # Dates for the predictions
    last_date = stock_data.index[-1]
    prediction_dates = []
    for i in range(1, 8):
        if timeframe == 'daily':
            delta = timedelta(days=i)
        elif timeframe == 'weekly':
            delta = timedelta(weeks=i)
        elif timeframe == 'monthly':
            # Approximating a month with 30 days; for precise calculation, use dateutil or similar library
            delta = timedelta(days=30 * i)
        else:
            delta = timedelta(days=i)  # Default to daily if timeframe is unrecognized

        prediction_dates.append(last_date + delta)

    predicted_prices = np.hstack((np.array(prediction_dates).reshape(-1, 1), predicted_prices))
    return predicted_prices

# Example usage
# company_id = 3  # Microsoft
# timeframe = 'daily'
# predictions = fetch_stock_prediction(company_id, timeframe)

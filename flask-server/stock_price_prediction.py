import requests
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from keras.callbacks import EarlyStopping
import numpy as np

def fetch_stock_prediction(company_id, timeframe):
    def build_model(input_shape):
        model = Sequential()
        model.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))
        model.add(Dropout(0.2))
        model.add(LSTM(units=50, return_sequences=False))
        model.add(Dropout(0.2))
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
        0: 'AAPL', 1: 'AMZN', 2: 'GOOGL', 3: 'MSFT', 4: 'TSLA', 5: 'JPM',
        6: 'WMT', 7: 'KO', 8: 'PFE', 9: 'NFLX'
    }
    symbol = company_symbols.get(company_id)
    api_key = '8WATTBIUUCY9LFYZ'
    stock_data = fetch_stock_data(symbol, api_key, timeframe)
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(stock_data[['Open', 'High', 'Low', 'Close', 'Volume']])
    sequence_length = 20  # Changed from 10 to 20
    X, y = create_sequences(scaled_data, sequence_length)
    model = build_model((sequence_length, X.shape[2]))
    early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
    # Assuming X and y are defined properly from the preprocessed dataset
    model.fit(X, y, epochs=100, batch_size=32, validation_split=0.1, callbacks=[early_stopping])
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
    return predicted_prices

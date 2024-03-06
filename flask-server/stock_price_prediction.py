import requests
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense
import numpy as np

def fetch_stock_prediction(company_id):
    # Function to create sequences from the dataset
    def create_sequences(data, sequence_length):
        xs, ys = [], []
        for i in range(len(data) - sequence_length):
            x = data[i:(i + sequence_length)]
            y = data[i + sequence_length]
            xs.append(x)
            ys.append(y)
        return np.array(xs), np.array(ys)

    # Function to fetch stock data from Alpha Vantage
    def fetch_stock_data(symbol, api_key):
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=60min&outputsize=full&apikey={api_key}"
        response = requests.get(url)
        data = response.json()
        
        # Parse the JSON data into a DataFrame
        df = pd.DataFrame(data[f'Time Series (60min)']).T
        df = df.rename(columns={
            '1. open': 'Open', 
            '2. high': 'High', 
            '3. low': 'Low', 
            '4. close': 'Close', 
            '5. volume': 'Volume'
        })
        for col in df.columns:
            df[col] = df[col].astype(float)
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()
        return df

    # Map of company IDs to stock symbols
    company_symbols = {0: 'AAPL', 1: 'IBM', 2: 'MSFT'}

    # Fetching the stock data
    symbol = company_symbols.get(company_id)
    api_key = '8WATTBIUUCY9LFYZ'
    stock_data = fetch_stock_data(symbol, api_key)

    # Preprocessing
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(stock_data)
    sequence_length = 10
    X, y = create_sequences(scaled_data, sequence_length)

    # Splitting the dataset
    split = int(0.8 * len(X))
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    # Building the LSTM model
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
    model.add(LSTM(units=50))
    model.add(Dense(5))  # Output layer

    # Compiling the model
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Training the model
    model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.1)

    # Predicting the next 7 time steps
    predicted = []
    current_batch = X_test[-1:].reshape(1, sequence_length, X_test.shape[2])

    for i in range(7):
        predicted_step = model.predict(current_batch)[0]
        predicted.append(predicted_step)
        predicted_step = np.reshape(predicted_step, (1, 1, predicted_step.shape[0]))
        current_batch = np.append(current_batch[:, 1:, :], predicted_step, axis=1)

    # Inverse transform to get the actual predictions
    predicted_prices = scaler.inverse_transform(predicted)

    return predicted_prices

# Example usage
# company_id = 1  # This would be passed as a parameter
# predictions = fetch_stock_prediction(company_id)
# print(predictions)

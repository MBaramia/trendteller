import requests
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense
import numpy as np
from db_schema import db, Prediction

def fetch_stock_prediction(company_id, timeframe):
    # Dummy LSTM model for testing
    def build_model(input_shape):
        model = Sequential()
        model.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))
        model.add(LSTM(units=50))
        model.add(Dense(5))  # Predicting: open, high, low, close, volume
        model.compile(optimizer='adam', loss='mean_squared_error')
        return model

    # Helper function to create sequences
    def create_sequences(data, sequence_length):
        xs, ys = [], []
        for i in range(len(data) - sequence_length):
            x = data[i:(i + sequence_length)]
            y = data[i + sequence_length]
            xs.append(x)
            ys.append(y)
        return np.array(xs), np.array(ys)

    # Fetch stock data (for testing, ensure you have a valid API key and the URL is correct)
    def fetch_stock_data(symbol, api_key, timeframe):
        # Simulate fetched data (for actual use, replace with API call and data extraction)
        dates = pd.date_range(end=pd.Timestamp.today(), periods=100)
        data = {
            'Open': np.random.rand(100) * 100,
            'High': np.random.rand(100) * 100,
            'Low': np.random.rand(100) * 100,
            'Close': np.random.rand(100) * 100,
            'Volume': np.random.rand(100) * 1000
        }
        df = pd.DataFrame(data, index=dates)
        return df

    # Assuming predefined company symbols
    company_symbols = {0: 'AAPL', 1: 'IBM', 2: 'MSFT'}
    symbol = company_symbols.get(company_id)
    api_key = '8WATTBIUUCY9LFYZ'
    stock_data = fetch_stock_data(symbol, api_key, timeframe)

    # Data preprocessing
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(stock_data)
    sequence_length = 10
    X, _ = create_sequences(scaled_data, sequence_length)

    # Define and build the LSTM model (dummy for demonstration)
    model = build_model((sequence_length, X.shape[2]))

    # Generate predictions (replace this with the actual model prediction logic)
    current_batch = X[-1:].reshape(1, sequence_length, X.shape[2])
    predicted = []
    for _ in range(7):
        predicted_step = np.random.rand(5)  # Dummy predictions
        predicted.append(predicted_step)
        predicted_step = np.reshape(predicted_step, (1, 1, len(predicted_step)))
        current_batch = np.append(current_batch[:, 1:, :], predicted_step, axis=1)

    predicted_prices = scaler.inverse_transform(predicted)
    for prediction in predicted_prices:
        new_prediction = Prediction(
            companyID=company_id,
            close=prediction[0],
            volume=prediction[1],
            open=prediction[2],
            high=prediction[3],
            low=prediction[4]
        )
        db.session.add(new_prediction)

    db.session.commit()
    # Print the 7 predictions
    for i, prediction in enumerate(predicted_prices, start=1):
        print(f"Prediction {i}: Open: {prediction[0]:.2f}, High: {prediction[1]:.2f}, Low: {prediction[2]:.2f}, Close: {prediction[3]:.2f}, Volume: {prediction[4]:.2f}")

    return predicted_prices

# Example usage
# predictions = fetch_stock_prediction(1, 'daily')  # Example: IBM, daily timeframe

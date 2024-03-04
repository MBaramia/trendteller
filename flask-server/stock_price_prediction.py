from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense
import numpy as np
import pandas as pd

# Load your dataset
data = pd.read_csv(r"C:\Users\Mohammed Baramia\OneDrive - University of Warwick\CS261\data.csv")

# Preprocess the data
data['Date'] = pd.to_datetime(data['Date'])
for col in ['Close', 'Open', 'High', 'Low']:
    data[col] = data[col].str.replace('$', '', regex=False).astype(float)
data.set_index('Date', inplace=True)
data.sort_index(inplace=True)

# Function to create sequences
def create_sequences(data, sequence_length):
    xs, ys = [], []
    for i in range(len(data) - sequence_length - 1):
        x = data[i:(i + sequence_length)]
        y = data[i + sequence_length]
        xs.append(x)
        ys.append(y)
    return np.array(xs), np.array(ys)

# Data normalization
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(data)

# Creating sequences
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
current_batch = X_test[-1:]  # Start with the last batch

for i in range(7):
    predicted_step = model.predict(current_batch)[0]
    predicted.append(predicted_step)
    # Reshape predicted_step to match the dimensions of current_batch
    predicted_step = np.reshape(predicted_step, (1, 1, predicted_step.shape[0]))
    current_batch = np.append(current_batch[:, 1:, :], predicted_step, axis=1)

# Inverse transform to get the actual predictions
predicted_prices = scaler.inverse_transform(predicted)

print(predicted_prices)

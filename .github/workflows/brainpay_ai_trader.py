import tensorflow as tf
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
import ccxt  # Crypto Exchange API

app = Flask(__name__)

# Load Market Data
data = pd.read_csv("crypto_prices.csv")
X = data[["open", "high", "low", "volume"]]
y = data["future_price"]

# Train AI Model
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(16, activation="relu", input_shape=(4,)),
    tf.keras.layers.Dense(8, activation="relu"),
    tf.keras.layers.Dense(1, activation="linear")
])

model.compile(optimizer="adam", loss="mse")
model.fit(X, y, epochs=50, verbose=0)

# Crypto Exchange API (Binance)
exchange = ccxt.binance()

@app.route("/predict", methods=["POST"])
def predict():
    request_data = request.json
    market_data = np.array([[request_data["open"], request_data["high"], request_data["low"], request_data["volume"]]])
    predicted_price = model.predict(market_data)[0][0]
    return jsonify({"predicted_price": predicted_price})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5008)

import tensorflow as tf
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Fetch Real Blockchain Data
def fetch_live_transactions():
    url = "https://mempool.space/api/mempool/recent"
    try:
        response = requests.get(url)
        transactions = response.json()
        return transactions
    except Exception as e:
        print("Error fetching live transactions:", e)
        return []

# Prepare AI Model Training Data
def prepare_data():
    transactions = fetch_live_transactions()
    data = []
    labels = []

    for tx in transactions:
        amount = tx['value'] / 1e8  # Convert Satoshis to BTC
        fee = tx['fee'] / 1e8  # Convert Satoshis to BTC
        is_fraud = 1 if amount > 10 else 0  # Example condition for fraud

        data.append([amount, fee])
        labels.append(is_fraud)

    return np.array(data), np.array(labels)

# Train AI Model
X, y = prepare_data()
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(10, activation="relu", input_shape=(2,)),
    tf.keras.layers.Dense(5, activation="relu"),
    tf.keras.layers.Dense(1, activation="sigmoid")
])

model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
model.fit(X, y, epochs=50, verbose=1)

@app.route("/analyze", methods=["POST"])
def analyze():
    tx = request.json
    risk_score = model.predict(np.array([[tx["amount"], tx["fee"]]]))[0][0]
    risk_label = "HIGH RISK" if risk_score > 0.7 else "LOW RISK"
    return jsonify({"txid": tx["txid"], "risk": risk_label, "risk_score": risk_score})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5006)

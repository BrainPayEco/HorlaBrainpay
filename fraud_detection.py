import requests
import time
from flask import Flask, jsonify

app = Flask(__name__)

BLOCKCHAIR_BTC_API = "https://api.blockchair.com/bitcoin/mempool"
ETHERSCAN_API = "https://api.etherscan.io/api?module=account&action=txlist"
SOLANA_API = "https://api.solana.com"

# Function to fetch latest transactions
def get_transactions():
    btc_txs = requests.get(BLOCKCHAIR_BTC_API).json()["data"]
    eth_txs = requests.get(ETHERSCAN_API).json()["result"]
    sol_txs = requests.get(SOLANA_API).json()["result"]

    return btc_txs, eth_txs, sol_txs

# Run AI-based fraud detection on live transactions
def analyze_live_txs():
    btc_txs, eth_txs, sol_txs = get_transactions()

    suspicious_txs = []

    for tx in btc_txs + eth_txs + sol_txs:
        risk_score = analyze_transaction(tx)  # AI model function
        if risk_score > 75:
            suspicious_txs.append(tx)
            send_alerts(tx, risk_score)

    return suspicious_txs

@app.route('/run-tests', methods=['GET'])
def run_tests():
    flagged_txs = analyze_live_txs()
    return jsonify({"flagged_transactions": flagged_txs})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

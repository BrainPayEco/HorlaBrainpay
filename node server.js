require("dotenv").config();
const express = require("express");
const axios = require("axios");

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

// Webhook Endpoint for Anomaly Detection
app.post("/webhook", async (req, res) => {
    try {
        console.log("🔔 Webhook received:", req.body);

        const { event, transaction_id, status, amount } = req.body;
        const message = `🚨 *Anomaly Detected!* 🚨\n\n🔍 Event: ${event}\n💰 Amount: ${amount} BTC\n📌 Status: ${status}\n🔗 TXID: ${transaction_id}`;

        // Send Telegram alert
        await axios.post(`https://api.telegram.org/bot${process.env.TELEGRAM_BOT_TOKEN}/sendMessage`, {
            chat_id: process.env.TELEGRAM_CHAT_ID,
            text: message,
            parse_mode: "Markdown"
        });

        res.status(200).json({ success: true, message: "Alert sent!" });
    } catch (error) {
        console.error("❌ Error:", error.message);
        res.status(500).json({ success: false, error: error.message });
    }
});

// Start server
app.listen(PORT, () => {
    console.log(`✅ Webhook server running on port ${PORT}`);
});

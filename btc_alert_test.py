import requests
from datetime import datetime
import pytz

# === CONFIG TELEGRAM ===
TELEGRAM_TOKEN = "8377953846:AAFRwVdYG-P0bUb4wB-zY2I-uYgNhOejZYI"
TELEGRAM_CHAT_ID = "1610942867"

# === FUNZIONE ALERT TELEGRAM ===
def send_telegram_alert(symbol, timeframe, timestamp_ms):
    dt = datetime.fromtimestamp(timestamp_ms / 1000, pytz.timezone("Europe/Rome"))
    formatted_time = dt.strftime("%d/%m/%Y %H:%M:%S")
    chart_link = f"https://www.bitget.com/it/spot/{symbol}"

    message = f"""
📢 *Segnale rilevato!*
🔹 Coppia: `{symbol}`
🕒 Timeframe: `{timeframe}`
📅 Data/Ora: `{formatted_time}`
📈 Grafico: [Apri TradingView]({chart_link})
"""

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("✅ Alert Telegram inviato.")
    else:
        print(f"❌ Errore Telegram: {response.text}")

# === FUNZIONE PRINCIPALE ===
def run_btc_alert():
    symbol = "BTCUSDT"
    timeframe = "1min"
    url = f"https://api.bitget.com/api/v2/spot/market/candles?symbol={symbol}&granularity={timeframe}&limit=1"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json().get("data", [])
        if len(data) == 0:
            print("❌ Nessuna candela ricevuta.")
            return

        candle = data[0]
        timestamp, open_, _, _, close, _ = candle[:6]

        if float(close) > float(open_):
            send_telegram_alert(symbol, timeframe, int(timestamp))
        else:
            print("ℹ️ Nessun segnale: candela non verde.")

    except Exception as e:
        print(f"❌ Errore fetch BTC: {e}")

if __name__ == "__main__":
    run_btc_alert()

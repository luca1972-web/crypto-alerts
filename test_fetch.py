import requests

def fetch_bitget(symbol="BTCUSDT", granularity="1h", limit=5):
    url = f"https://api.bitget.com/api/v2/spot/market/candles?symbol={symbol}&granularity={granularity}&limit={limit}"
    try:
        response = requests.get(url)
        print("📡 Raw response:", response.text)
        response.raise_for_status()
        data = response.json().get("data", [])
        if len(data) == 0:
            print("❌ Nessun dato ricevuto.")
            return
        for item in data:
            print({
                "time": item[0],
                "open": item[1],
                "high": item[2],
                "low": item[3],
                "close": item[4],
                "volume": item[5]
            })
    except Exception as e:
        print(f"❌ Errore: {e}")

if __name__ == "__main__":
    fetch_bitget()

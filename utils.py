import os
import krakenex
import requests

API_KEY = os.getenv("KRAKEN_API_KEY")
API_SECRET = os.getenv("KRAKEN_API_SECRET")

k = krakenex.API()
k.key = API_KEY
k.secret = API_SECRET

def get_balance(asset):
    try:
        balance = k.query_private('Balance')["result"]
        return float(balance.get(asset, 0.0))
    except Exception as e:
        print(f"Erreur get_balance : {e}")
        return 0.0

def get_price(pair):
    try:
        url = f"https://api.kraken.com/0/public/Ticker?pair={pair.replace('/', '')}"
        response = requests.get(url)
        data = response.json()
        result = data.get("result")
        if result:
            first_key = list(result.keys())[0]
            price = float(result[first_key]["c"][0])
            return price
    except Exception as e:
        print(f"Erreur get_price : {e}")
    return None

def get_indicators(pair):
    try:
        rsi_value = 50
        moving_average = 200
        return {"RSI": rsi_value, "MovingAverage": moving_average}
    except Exception as e:
        print(f"Erreur get_indicators : {e}")
        return {"RSI": 50, "MovingAverage": 200}

def buy_crypto(pair, quantity):
    print(f"Achat simulé de {quantity} {pair}")

def sell_crypto(pair, quantity):
    print(f"Vente simulée de {quantity} {pair}")

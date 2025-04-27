import os
import krakenex
import requests
from dotenv import load_dotenv

# Charge les variables d'environnement depuis .env
load_dotenv()

# Affiche en log que les clés sont bien chargées
print("🔑 Loaded KRAKEN_API_KEY:", bool(os.getenv("KRAKEN_API_KEY")))
print("🔑 Loaded KRAKEN_API_SECRET:", bool(os.getenv("KRAKEN_API_SECRET")))

# Initialise l'API Kraken
api = krakenex.API()
api.key = os.getenv("KRAKEN_API_KEY")
api.secret = os.getenv("KRAKEN_API_SECRET")

def get_balance(asset):
    try:
        res = api.query_private('Balance')
        result = res.get('result', {})
        return float(result.get(asset, 0.0))
    except Exception as e:
        print(f"Erreur get_balance : {e}")
        return 0.0

def get_price(pair):
    try:
        resp = requests.get(f"https://api.kraken.com/0/public/Ticker?pair={pair.replace('/', '')}")
        data = resp.json().get('result', {})
        first = list(data.values())[0]
        return float(first['c'][0])
    except Exception as e:
        print(f"Erreur get_price : {e}")
        return None

def buy_crypto(pair, volume):
    try:
        order = {
            'pair': pair.replace('/', ''),
            'type': 'buy',
            'ordertype': 'market',
            'volume': str(volume)
        }
        response = api.query_private('AddOrder', order)
        print("📝 buy_crypto response:", response)
        return response
    except Exception as e:
        print(f"Erreur buy_crypto : {e}")
        return None

def sell_crypto(pair, volume):
    try:
        order = {
            'pair': pair.replace('/', ''),
            'type': 'sell',
            'ordertype': 'market',
            'volume': str(volume)
        }
        response = api.query_private('AddOrder', order)
        print("📝 sell_crypto response:", response)
        return response
    except Exception as e:
        print(f"Erreur sell_crypto : {e}")
        return None

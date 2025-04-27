import requests
import os

KRAKEN_API_KEY = os.getenv('KRAKEN_API_KEY')
KRAKEN_API_SECRET = os.getenv('KRAKEN_API_SECRET')

# Seuils minimums d'achat (en quantité de crypto)
MINIMUMS = {
    "BTC/EUR": 0.0001,
    "ETH/EUR": 0.0015,
    "XRP/EUR": 10,
    "SOL/EUR": 0.02,
    "MATIC/EUR": 5,
    "AVAX/EUR": 0.3,
    "ADA/EUR": 15,
    "LINK/EUR": 0.3
}

def get_balance(asset):
    try:
        # Simulation Kraken : retourne un solde fictif
        return 0.0
    except Exception as e:
        print(f"Erreur get_balance : {str(e)}")
        return 0.0

def get_price(pair):
    try:
        url = f"https://api.kraken.com/0/public/Ticker?pair={pair.replace('/', '')}"
        response = requests.get(url)
        data = response.json()
        result = data['result']
        price = list(result.values())[0]['c'][0]
        return float(price)
    except Exception as e:
        print(f"Erreur get_price : {str(e)}")
        return None

def get_indicators(asset):
    try:
        return {"RSI": 50, "MovingAverage": 200}
    except Exception as e:
        print(f"Erreur get_indicators : {str(e)}")
        return {"RSI": 0, "MovingAverage": 0}

def buy_crypto(pair, quantity):
    try:
        # Vérification du minimum
        if quantity < MINIMUMS.get(pair, 0):
            print(f"Quantité {quantity} inférieure au minimum requis pour {pair}. Pas d'achat.")
            return {"error": "Volume minimum non atteint"}
        
        print(f"Ordre d'achat simulé : {quantity} {pair}")
        return {"success": True}
    except Exception as e:
        print(f"Erreur buy_crypto : {str(e)}")
        return {"error": str(e)}

import krakenex
import requests
import os

# Connexion Kraken API
api = krakenex.API()
api_key = os.getenv("KRAKEN_API_KEY")
api_secret = os.getenv("KRAKEN_API_SECRET")
api.load_key = lambda *args, **kwargs: None
api.key = api_key
api.secret = api_secret

def get_balance(asset):
    try:
        response = api.query_private('Balance')
        balance = response['result'].get(asset, 0)
        return float(balance)
    except Exception as e:
        print(f"[ERREUR] get_balance: {e}")
        return 0.0

def get_price(pair):
    try:
        url = f"https://api.kraken.com/0/public/Ticker?pair={pair}"
        response = requests.get(url)
        data = response.json()
        price = list(data['result'].values())[0]['c'][0]  # prix actuel
        return float(price)
    except Exception as e:
        print(f"[ERREUR] get_price: {e}")
        return None

def buy_crypto(pair, volume_eur):
    try:
        # On récupère le prix actuel
        price = get_price(pair)
        if price is None:
            print(f"[ERREUR] Prix introuvable pour {pair}")
            return

        # Calcul du volume en crypto
        volume = round(volume_eur / price, 8)

        order = {
            'pair': pair,
            'type': 'buy',
            'ordertype': 'market',
            'volume': str(volume),
        }
        response = api.query_private('AddOrder', order)
        print(f"Réponse achat : {response}")
        return response
    except Exception as e:
        print(f"[ERREUR] buy_crypto: {e}")
        return None

def sell_crypto(pair, volume_crypto):
    try:
        order = {
            'pair': pair,
            'type': 'sell',
            'ordertype': 'market',
            'volume': str(volume_crypto),
        }
        response = api.query_private('AddOrder', order)
        print(f"Réponse vente : {response}")
        return response
    except Exception as e:
        print(f"[ERREUR] sell_crypto: {e}")
        return None

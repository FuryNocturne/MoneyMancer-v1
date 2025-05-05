import krakenex
import requests
import os

# Connexion à l'API Kraken
api = krakenex.API()
api_key = os.getenv('KRAKEN_API_KEY')
api_secret = os.getenv('KRAKEN_API_SECRET')
api.load_key = lambda *args, **kwargs: None
api.key = api_key
api.secret = api_secret

# Obtenir le solde d’un actif
def get_balance(asset):
    try:
        response = api.query_private('Balance')['result']
        balance = response.get(asset, 0)
        return float(balance)
    except Exception as e:
        print(f"[ERREUR] get_balance : {e}")
        return 0.0

# Obtenir le prix actuel d’une paire
def get_price(pair):
    try:
        url = f'https://api.kraken.com/0/public/Ticker?pair={pair}'
        response = requests.get(url)
        data = response.json()
        price = list(data['result'].values())[0]['c'][0]
        return float(price)
    except Exception as e:
        print(f"[ERREUR] get_price : {e}")
        return None

# Acheter une crypto
def buy_crypto(pair, volume_eur):
    try:
        price = get_price(pair)
        if price is None:
            print(f"[ERREUR] Prix introuvable pour {pair}")
            return None

        volume = round(volume_eur / price, 8)

        order = {
            'pair': pair,
            'type': 'buy',
            'ordertype': 'market',
            'volume': str(volume),
            'oflags': 'viqc'
        }

        response = api.query_private('AddOrder', order)
        print(f"[ACHAT] Réponse : {response}")
        return response
    except Exception as e:
        print(f"[ERREUR] buy_crypto : {e}")
        return None

# Vendre une crypto
def sell_crypto(pair, volume_crypto):
    try:
        order = {
            'pair': pair,
            'type': 'sell',
            'ordertype': 'market',
            'volume': str(volume_crypto),
            'oflags': 'viqc'
        }

        response = api.query_private('AddOrder', order)
        print(f"[VENTE] Réponse : {response}")
        return response
    except Exception as e:
        print(f"[ERREUR] sell_crypto : {e}")
        return None

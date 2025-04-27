import krakenex
from config import API_KEY, API_SECRET, MODE

api = krakenex.API()
api.key = API_KEY
api.secret = API_SECRET

def buy_asset(asset, quantity):
    try:
        if MODE == "TEST":
            print(f"[TEST] Achat simulé de {quantity} {asset}")
            return True
        pair = f"{asset}EUR"
        response = api.query_private('AddOrder', {
            'pair': pair,
            'type': 'buy',
            'ordertype': 'market',
            'volume': quantity
        })
        if response['error']:
            print(f"Erreur lors de l'achat de {asset} : {response['error']}")
            return False
        return True
    except Exception as e:
        print(f"Erreur inattendue lors de l'achat de {asset} : {e}")
        return False

def sell_asset(asset, quantity):
    try:
        if MODE == "TEST":
            print(f"[TEST] Vente simulée de {quantity} {asset}")
            return True
        pair = f"{asset}EUR"
        response = api.query_private('AddOrder', {
            'pair': pair,
            'type': 'sell',
            'ordertype': 'market',
            'volume': quantity
        })
        if response['error']:
            print(f"Erreur lors de la vente de {asset} : {response['error']}")
            return False
        return True
    except Exception as e:
        print(f"Erreur inattendue lors de la vente de {asset} : {e}")
        return False

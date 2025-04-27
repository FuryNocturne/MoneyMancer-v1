import krakenex
import os
from dotenv import load_dotenv

load_dotenv()

k = krakenex.API()
k.key = os.getenv('KRAKEN_API_KEY')
k.secret = os.getenv('KRAKEN_API_SECRET')

def get_balance(asset):
    try:
        balance = k.query_private('Balance')
        return float(balance['result'].get(asset, 0))
    except Exception as e:
        print(f"Erreur get_balance : {e}")
        return 0

def get_price(pair):
    try:
        ticker = k.query_public('Ticker', {'pair': pair})
        return float(ticker['result'][list(ticker['result'].keys())[0]]['c'][0])
    except Exception as e:
        print(f"Erreur get_price : {e}")
        return 0

def buy_crypto(pair, volume):
    try:
        response = k.query_private('AddOrder', {
            'pair': pair,
            'type': 'buy',
            'ordertype': 'market',
            'volume': volume,
        })
        return response
    except Exception as e:
        print(f"Erreur buy_crypto : {e}")
        return None

def sell_crypto(pair, volume):
    try:
        response = k.query_private('AddOrder', {
            'pair': pair,
            'type': 'sell',
            'ordertype': 'market',
            'volume': volume,
        })
        return response
    except Exception as e:
        print(f"Erreur sell_crypto : {e}")
        return None

import requests
import krakenex
import os

# Connexion Kraken API avec variables d'environnement
api = krakenex.API()
api.key = os.getenv('KRAKEN_API_KEY')
api.secret = os.getenv('KRAKEN_API_SECRET')

def get_balance(asset):
    try:
        response = api.query_private('Balance')
        if response['error']:
            print(f"Erreur de récupération du solde : {response['error']}")
            return 0
        balance = response['result'].get(asset, 0)
        return float(balance)
    except Exception as e:
        print(f"Erreur de récupération du solde : {e}")
        return 0

def get_prices(pair):
    try:
        url = f"https://api.kraken.com/0/public/Ticker?pair={pair}"
        response = requests.get(url)
        data = response.json()
        result = list(data['result'].values())[0]
        price = float(result['c'][0])
        return price
    except Exception as e:
        print(f"Erreur de récupération du prix : {e}")
        return None

def get_indicators(pair):
    try:
        # Dummy indicators pour l'exemple
        rsi_value = 50  # Remplacer par du vrai RSI plus tard
        moving_average = 200  # Idem pour la moyenne mobile
        return {
            'RSI': rsi_value,
            'MovingAverage': moving_average
        }
    except Exception as e:
        print(f"Erreur de calcul des indicateurs : {e}")
        return None

def execute_trade(pair, side, volume):
    try:
        order = {
            'pair': pair,
            'type': side,
            'ordertype': 'market',
            'volume': str(volume)
        }
        response = api.query_private('AddOrder', order)

        if response['error']:
            print(f"Erreur de trading pour {pair} : {response['error']}")
        else:
            print(f"Trade exécuté pour {pair} : {side.upper()} {volume}")
    except Exception as e:
        print(f"Erreur lors de l'exécution du trade : {e}")

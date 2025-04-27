import requests
import numpy as np

def get_balance():
    url = "https://api.kraken.com/0/private/Balance"
    response = requests.post(url)
    return response.json()

def get_prices(asset):
    url = f"https://api.kraken.com/0/public/Ticker?pair={asset}EUR"
    response = requests.get(url)
    data = response.json()
    return float(data['result'][list(data['result'].keys())[0]]['c'][0])

def get_indicators(asset, prices):
    moving_average_window = 5
    if len(prices) < moving_average_window:
        return None, None

    moving_average = np.mean(prices[-moving_average_window:])
    rsi = 50  # Valeur fictive pour l'instant
    return moving_average, rsi

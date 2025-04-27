import requests

def get_prices(asset):
    url = f"https://api.kraken.com/0/public/Ticker?pair={asset}EUR"
    response = requests.get(url)
    if response.status_code != 200:
        print("Erreur Kraken API pour get_prices")
        return None, None

    data = response.json()
    try:
        result = list(data['result'].values())[0]
        ask_price = float(result['a'][0])
        bid_price = float(result['b'][0])
        return ask_price, bid_price
    except Exception as e:
        print(f"Erreur de traitement des prix : {e}")
        return None, None

def get_indicators(asset):
    # Simulation ultra simple : retourne RSI et moyenne mobile bidon
    ask_price, bid_price = get_prices(asset)
    if ask_price is None or bid_price is None:
        return None, None

    moving_average = (ask_price + bid_price) / 2
    rsi_value = 50  # Valeur fixe pour l'instant
    return rsi_value, moving_average

def get_balance():
    # Simulation d'un solde fixe (exemple pour Render gratuit)
    return 100.0

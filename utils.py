import requests

# Fonctions utilitaires corrigées

def get_prices(asset):
    try:
        url = f"https://api.kraken.com/0/public/Ticker?pair={asset}USD"
        response = requests.get(url)
        data = response.json()
        result = data["result"]
        first_key = list(result.keys())[0]
        price = result[first_key]["c"][0]
        return float(price)
    except Exception as e:
        print(f"Erreur dans get_prices: {e}")
        return None

def get_balance(asset):
    try:
        # Simulation balance (à remplacer par ton vrai appel API si besoin)
        return 1.0  # Balance fictive pour éviter crash
    except Exception as e:
        print(f"Erreur dans get_balance: {e}")
        return None

def get_indicators(asset):
    try:
        # Simulation d'indicateurs
        return {"RSI": 50, "MovingAverage": 200}
    except Exception as e:
        print(f"Erreur dans get_indicators: {e}")
        return None

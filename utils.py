import requests

def get_indicators(asset):
    url = f"https://api.kraken.com/0/public/Ticker?pair={asset}"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Erreur API Kraken pour {asset}")
        return None, None

    data = response.json()

    try:
        result = list(data["result"].values())[0]
        
        # Exemple simplifié : je récupère les prix d'achat et de vente (bid et ask)
        ask_price = float(result["a"][0])  # prix d'achat
        bid_price = float(result["b"][0])  # prix de vente
        
        # Simulons un RSI et une MA simple ici, pour éviter de complexifier
        rsi_value = (ask_price / bid_price) * 50  # Pas un vrai RSI mais ça suffit pour l’exemple
        moving_average = (ask_price + bid_price) / 2
        
        return rsi_value, moving_average

    except Exception as e:
        print(f"Erreur de traitement de {asset} : {e}")
        return None, None

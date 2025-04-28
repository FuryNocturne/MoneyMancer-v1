import time
import krakenex
import requests
import json
import os

# Variables d'environnement
KRAKEN_API_KEY = os.getenv('KRAKEN_API_KEY')
KRAKEN_API_SECRET = os.getenv('KRAKEN_API_SECRET')

# Config de l'achat
MIN_PURCHASE_EUR = 5  # Montant minimum pour éviter les erreurs

# Connexion Kraken
api = krakenex.API(key=KRAKEN_API_KEY, secret=KRAKEN_API_SECRET)
print("MoneyMancer connecté à Kraken | Démarrage du trading automatique...")

# Conversion des symboles Kraken
symbol_map = {
    'XXBTZEUR': 'BTC/EUR',
    'XETHZEUR': 'ETH/EUR',
    'XXRPZEUR': 'XRP/EUR',
    'XLINKZEUR': 'LINK/EUR',
    'XMATICEUR': 'MATIC/EUR',
    'SOL/EUR': 'SOL/EUR',
    'ADA/EUR': 'ADA/EUR',
    'AVAX/EUR': 'AVAX/EUR'
}

# Fonction récupérer le prix actuel
def get_price(pair):
    try:
        response = api.query_public('Ticker', {'pair': pair})
        price = float(response['result'][list(response['result'].keys())[0]]['c'][0])
        return price
    except Exception as e:
        print(f"Erreur get_price : {e}")
        return None

# Fonction acheter
def buy_crypto(pair, amount_eur):
    try:
        order = api.query_private('AddOrder', {
            'pair': pair,
            'type': 'buy',
            'ordertype': 'market',
            'volume': str(amount_eur),
            'oflags': 'viqc'
        })
        print(f"Réponse achat : {order}")
    except Exception as e:
        print(f"Erreur achat : {e}")

# Boucle principale
while True:
    for symbol in symbol_map.keys():
        print(f"\nAnalyse de {symbol}...")

        # Prix
        price = get_price(symbol)
        if price:
            print(f"Prix actuel de {symbol} : {price} €")

            # Solde disponible
            balance_response = api.query_private('Balance')
            balance = balance_response['result'].get('ZEUR', 0)
            print(f"Solde EUR disponible : {balance}")

            if float(balance) >= MIN_PURCHASE_EUR:
                print(f"Condition remplie : Achat de {symbol_map[symbol]} pour {MIN_PURCHASE_EUR}€")
                buy_crypto(symbol, MIN_PURCHASE_EUR)
            else:
                print(f"Pas assez de solde pour acheter {symbol_map[symbol]}")
    
    print("\nPause de 10 minutes avant prochain scan...")
    time.sleep(600)  # 10 minutes

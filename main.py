import os
import time
from krakenex import API
from pykrakenapi import KrakenAPI

# Récupération sécurisée des clés API depuis les variables d'environnement
api_key = os.getenv('KRAKEN_API_KEY')
api_sec = os.getenv('KRAKEN_API_SECRET')

api = API(key=api_key, secret=api_sec)
k = KrakenAPI(api)

# Cryptos à trader
cryptos = ['ADA', 'SOL', 'AVAX', 'LINK', 'XRP', 'MATIC']

# Paramètres du bot
achat_par_crypto_eur = 5.0  # montant d'achat par crypto en EUR
stop_loss_percent = 5  # Pourcentage de stop-loss

def get_balance(asset):
    try:
        balances = k.get_account_balance()
        balance = balances.loc[asset]['vol']
        return float(balance)
    except Exception as e:
        print(f"Erreur récupération balance {asset} : {e}")
        return 0.0

def get_price(pair):
    try:
        ohlc, _ = k.get_ohlc_data(pair, interval=5)
        last_close = ohlc['close'].iloc[-1]
        return float(last_close)
    except Exception as e:
        print(f"Erreur récupération prix {pair} : {e}")
        return None

def buy_crypto(pair, amount_eur):
    try:
        response = api.query_private('AddOrder', {
            'pair': pair,
            'type': 'buy',
            'ordertype': 'market',
            'volume': str(amount_eur),
            'oflags': 'fcib'  # force maker pour réduire les frais
        })
        print(f"Réponse achat {pair}: {response}")
    except Exception as e:
        print(f"Erreur achat {pair} : {e}")

print("MoneyMancer connecté à Kraken | Démarrage du trading automatique...")

while True:
    try:
        for crypto in cryptos:
            pair = f"{crypto}EUR"
            print(f"\nAnalyse de {pair}...")

            price = get_price(pair)
            if price is None:
                continue

            balance_eur = get_balance('ZEUR')
            balance_crypto = get_balance(f"X{crypto}")

            print(f"Prix actuel : {price}€")
            print(f"Solde EUR disponible : {balance_eur}€")
            print(f"Solde {crypto} disponible : {balance_crypto}")

            # Achat si conditions remplies
            if balance_eur >= achat_par_crypto_eur:
                print(f"Condition remplie : Achat de {crypto} pour {achat_par_crypto_eur}€")
                buy_crypto(pair, achat_par_crypto_eur)
            else:
                print(f"Pas assez d'EUR pour acheter {crypto}.")

        print("\nPause de 10 minutes avant prochain scan...\n")
        time.sleep(600)

    except Exception as e:
        print(f"Erreur globale : {e}")
        time.sleep(60)

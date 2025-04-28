import os
import time
import krakenex

# Connexion API Kraken
api = krakenex.API()
api.load_key('')

api_key = os.getenv('KRAKEN_API_KEY')
api_secret = os.getenv('KRAKEN_API_SECRET')
api.key = api_key
api.secret = api_secret

# Cryptos surveillées
assets = ['XRP', 'LINK', 'SOL', 'AVAX', 'ADA', 'MATIC']
fiat = 'EUR'

# Paramètres achat
montant_achat_eur = 5  # Montant par achat en EUR
interval_scan = 600  # 10 minutes en secondes

def get_balance(asset):
    try:
        balance = api.query_private('Balance')
        return float(balance['result'].get(asset, 0))
    except Exception as e:
        print(f"Erreur récupération solde pour {asset} : {e}")
        return 0

def get_price(pair):
    try:
        ticker = api.query_public('Ticker', {'pair': pair})
        result = list(ticker['result'].values())[0]
        price = float(result['c'][0])
        return price
    except Exception as e:
        print(f"Erreur récupération prix pour {pair} : {e}")
        return None

def buy_crypto(pair, volume):
    try:
        response = api.query_private('AddOrder', {
            'pair': pair,
            'type': 'buy',
            'ordertype': 'market',
            'volume': volume,
        })
        print(f"Réponse achat : {response}")
        return response
    except Exception as e:
        print(f"Erreur commande achat pour {pair} : {e}")
        return None

def trading_loop():
    print("MoneyMancer connecté à Kraken ! Début du trading automatique...")
    while True:
        for asset in assets:
            print(f"\n--- Analyse de {asset}/{fiat} ---")
            balance = get_balance(asset)
            pair = f'X{asset}Z{fiat}' if asset != 'BTC' else f'XXBTZ{fiat}'
            price = get_price(pair)

            if price is None:
                print(f"Prix de {asset} non récupéré, skip.")
                continue

            print(f"Prix actuel de {asset} : {price} {fiat}")
            print(f"Solde disponible : {balance} {asset}")

            if balance == 0:
                # Définir volume à acheter
                volume = montant_achat_eur / price
                volume = round(volume, 6)  # 6 décimales max

                if volume > 0:
                    print(f"Condition remplie : Achat de {asset} pour {montant_achat_eur} {fiat}")
                    buy_crypto(pair, volume)
                else:
                    print("Montant calculé trop faible pour achat.")
            else:
                print(f"Déjà des {asset} en portefeuille. Aucun achat effectué.")

        print(f"\n⏳ Pause de {interval_scan // 60} minutes avant nouveau scan...")
        time.sleep(interval_scan)

if __name__ == "__main__":
    trading_loop()

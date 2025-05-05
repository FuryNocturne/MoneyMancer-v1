import time
import krakenex
import os

# Connexion Kraken API
KRAKEN_API_KEY = os.getenv('KRAKEN_API_KEY')
KRAKEN_API_SECRET = os.getenv('KRAKEN_API_SECRET')

api = krakenex.API(key=KRAKEN_API_KEY, secret=KRAKEN_API_SECRET)
print("MoneyMancer connecté à Kraken | Démarrage du trading automatique...")

# Config
cryptos = ['ADA', 'SOL', 'AVAX', 'LINK', 'XRP', 'MATIC']
min_purchase_eur = 5.0
take_profit = 0.05   # +5%
stop_loss = -0.05    # -5%
xp = 0

# Dictionnaire pour suivre les prix d'achat
achat_prix = {}

# Fonction obtenir le prix actuel
def get_price(pair):
    try:
        response = api.query_public('Ticker', {'pair': pair})
        price = float(response['result'][list(response['result'].keys())[0]]['c'][0])
        return price
    except Exception as e:
        print(f"Erreur récupération prix {pair} : {e}")
        return None

# Fonction acheter une crypto
def buy_crypto(pair, amount_eur):
    try:
        response = api.query_private('AddOrder', {
            'pair': pair,
            'type': 'buy',
            'ordertype': 'market',
            'volume': str(amount_eur),
            'oflags': 'viqc'
        })
        print(f"Achat réussi {pair} : {response}")
        return True
    except Exception as e:
        print(f"Erreur achat {pair} : {e}")
        return False

# Fonction vendre une crypto
def sell_crypto(pair, volume):
    try:
        response = api.query_private('AddOrder', {
            'pair': pair,
            'type': 'sell',
            'ordertype': 'market',
            'volume': str(volume),
            'oflags': 'viqc'
        })
        print(f"Vente réussie {pair} : {response}")
        return True
    except Exception as e:
        print(f"Erreur vente {pair} : {e}")
        return False

# Fonction pour surveiller les positions
def check_positions():
    global xp
    balances = api.query_private('Balance')['result']
    
    for crypto in cryptos:
        asset_code = f'X{crypto}'
        if asset_code not in balances:
            continue

        quantity = float(balances.get(asset_code, 0))
        if quantity <= 0:
            continue

        pair = f'{crypto}EUR'
        price_now = get_price(pair)
        if not price_now:
            continue

        prix_achat = achat_prix.get(crypto)
        if not prix_achat:
            continue

        variation = (price_now - prix_achat) / prix_achat

        if variation >= take_profit:
            print(f"[+ PROFIT] {crypto} : +{variation*100:.2f}% → Vente automatique !")
            if sell_crypto(pair, quantity):
                xp += 1
                achat_prix.pop(crypto)
        elif variation <= stop_loss:
            print(f"[- PERTE] {crypto} : {variation*100:.2f}% → Vente automatique pour limiter les pertes.")
            if sell_crypto(pair, quantity):
                xp += 1
                achat_prix.pop(crypto)

# Fonction principale
while True:
    try:
        check_positions()

        balance_eur = float(api.query_private('Balance')['result'].get('ZEUR', 0))
        print(f"Solde EUR disponible : {balance_eur}€")

        for crypto in cryptos:
            pair = f'{crypto}EUR'
            if balance_eur >= min_purchase_eur and crypto not in achat_prix:
                print(f"Achat de {crypto} en cours pour {min_purchase_eur}€...")
                if buy_crypto(pair, min_purchase_eur):
                    prix_achat = get_price(pair)
                    if prix_achat:
                        achat_prix[crypto] = prix_achat
                        print(f"Prix d'achat enregistré pour {crypto} : {prix_achat}€")
        
        print(f"\nXP actuel : {xp}")
        print("Pause de 10 minutes...\n")
        time.sleep(600)

    except Exception as e:
        print(f"Erreur globale : {e}")
        time.sleep(60)

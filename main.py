import time
import krakenex
import os

# Connexion à l'API Kraken avec les clés des variables d'environnement Railway
KRAKEN_API_KEY = os.getenv('KRAKEN_API_KEY')
KRAKEN_API_SECRET = os.getenv('KRAKEN_API_SECRET')

api = krakenex.API(key=KRAKEN_API_KEY, secret=KRAKEN_API_SECRET)
print("MoneyMancer connecté à Kraken | Démarrage du trading automatique...")

# Paramètres de configuration
cryptos = ['ADA', 'SOL', 'AVAX', 'LINK', 'XRP', 'MATIC']
min_purchase_eur = 5.0
take_profit = 0.05    # +5%
stop_loss = -0.05     # -5%
xp = 0
achat_prix = {}       # Historique des prix d'achat

# Obtenir le prix actuel d'une paire (ex: ADAXEUR)
def get_price(pair):
    try:
        response = api.query_public('Ticker', {'pair': pair})
        price = float(list(response['result'].values())[0]['c'][0])
        return price
    except Exception as e:
        print(f"[ERREUR] Prix {pair} : {e}")
        return None

# Achat automatique
def buy_crypto(pair, amount_eur):
    try:
        response = api.query_private('AddOrder', {
            'pair': pair,
            'type': 'buy',
            'ordertype': 'market',
            'volume': str(amount_eur),
            'oflags': 'viqc'
        })
        print(f"[ACHAT] {pair} : {response}")
        return True
    except Exception as e:
        print(f"[ERREUR ACHAT] {pair} : {e}")
        return False

# Vente automatique
def sell_crypto(pair, volume):
    try:
        response = api.query_private('AddOrder', {
            'pair': pair,
            'type': 'sell',
            'ordertype': 'market',
            'volume': str(volume),
            'oflags': 'viqc'
        })
        print(f"[VENTE] {pair} : {response}")
        return True
    except Exception as e:
        print(f"[ERREUR VENTE] {pair} : {e}")
        return False

# Vérifie les variations et déclenche les ventes
def check_positions():
    global xp
    try:
        balances = api.query_private('Balance')['result']
        for crypto in cryptos:
            asset_code = f'X{crypto}'
            if asset_code not in balances:
                continue

            quantity = float(balances[asset_code])
            if quantity <= 0:
                continue

            pair = f'{crypto}EUR'
            current_price = get_price(pair)
            if not current_price:
                continue

            buy_price = achat_prix.get(crypto)
            if not buy_price:
                continue

            variation = (current_price - buy_price) / buy_price
            if variation >= take_profit:
                print(f"[+ PROFIT] {crypto} +{variation*100:.2f}% : VENTE")
                if sell_crypto(pair, quantity):
                    xp += 1
                    achat_prix.pop(crypto)
            elif variation <= stop_loss:
                print(f"[- PERTE] {crypto} {variation*100:.2f}% : VENTE")
                if sell_crypto(pair, quantity):
                    xp += 1
                    achat_prix.pop(crypto)
    except Exception as e:
        print(f"[ERREUR POSITION] : {e}")

# Boucle principale de trading automatique
while True:
    try:
        check_positions()

        balance_eur = float(api.query_private('Balance')['result'].get('ZEUR', 0))
        print(f"[SOLDE] EUR dispo : {balance_eur:.2f}€")

        for crypto in cryptos:
            pair = f'{crypto}EUR'
            if balance_eur >= min_purchase_eur and crypto not in achat_prix:
                print(f"[SCAN] Achat de {crypto} pour {min_purchase_eur}€...")
                if buy_crypto(pair, min_purchase_eur):
                    prix = get_price(pair)
                    if prix:
                        achat_prix[crypto] = prix
                        print(f"[ENREGISTRÉ] Prix {crypto} : {prix}€")

        print(f"[XP] Total : {xp} | Pause de 10 minutes...\n")
        time.sleep(600)  # 10 min

    except Exception as e:
        print(f"[ERREUR GÉNÉRALE] : {e}")
        time.sleep(60)

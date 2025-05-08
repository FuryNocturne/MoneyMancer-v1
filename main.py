import time
import os
import json
import krakenex

# === Connexion Kraken ===
KRAKEN_API_KEY = os.getenv('KRAKEN_API_KEY')
KRAKEN_API_SECRET = os.getenv('KRAKEN_API_SECRET')
api = krakenex.API(key=KRAKEN_API_KEY, secret=KRAKEN_API_SECRET)

print("\nMONEYMANCER EN MARCHE !\n")

# === Paramètres ===
cryptos = ['BTC', 'ETH', 'SOL', 'AVAX', 'LINK', 'XRP', 'MATIC', 'ADA']
min_purchase_eur = 5.0
take_profit = 0.05
stop_loss = -0.05
xp = 0
achat_prix_file = 'achat_prix.json'

# === Chargement des prix d'achat sauvegardés ===
if os.path.exists(achat_prix_file):
    with open(achat_prix_file, 'r') as f:
        achat_prix = json.load(f)
else:
    achat_prix = {}

# === Fonction: Enregistrement du prix d'achat ===
def sauvegarder_achat_prix():
    with open(achat_prix_file, 'w') as f:
        json.dump(achat_prix, f)

# === Fonction: Obtenir le prix actuel ===
def get_price(pair):
    try:
        response = api.query_public('Ticker', {'pair': pair})
        return float(response['result'][list(response['result'].keys())[0]]['c'][0])
    except Exception as e:
        print(f"Erreur prix {pair} : {e}")
        return None

# === Fonction: Acheter une crypto ===
def buy_crypto(pair, amount_eur):
    try:
        response = api.query_private('AddOrder', {
            'pair': pair,
            'type': 'buy',
            'ordertype': 'market',
            'volume': str(amount_eur),
            'oflags': 'viqc'
        })
        print(f"Achat {pair} : {response}")
        return True
    except Exception as e:
        print(f"Erreur achat {pair} : {e}")
        return False

# === Fonction: Vendre une crypto ===
def sell_crypto(pair, volume):
    try:
        response = api.query_private('AddOrder', {
            'pair': pair,
            'type': 'sell',
            'ordertype': 'market',
            'volume': str(volume),
            'oflags': 'viqc'
        })
        print(f"Vente {pair} : {response}")
        return True
    except Exception as e:
        print(f"Erreur vente {pair} : {e}")
        return False

# === Fonction: Analyse portefeuille ===
def check_positions():
    global xp
    balances = api.query_private('Balance')['result']

    for crypto in cryptos:
        asset_code = f'X{crypto}' if f'X{crypto}' in balances else crypto
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
            print(f"{crypto} => Quantité: {quantity:.4f} | Prix d'achat: Non défini")
            continue

        variation = (price_now - prix_achat) / prix_achat

        if variation >= take_profit:
            print(f"[+ PROFIT] {crypto} : +{variation*100:.2f}% → Vente automatique")
            if sell_crypto(pair, quantity):
                xp += 1
                achat_prix.pop(crypto)
                sauvegarder_achat_prix()

        elif variation <= stop_loss:
            print(f"[- PERTE] {crypto} : {variation*100:.2f}% → Vente pour limiter les pertes")
            if sell_crypto(pair, quantity):
                xp += 1
                achat_prix.pop(crypto)
                sauvegarder_achat_prix()
        else:
            print(f"{crypto} => Quantité: {quantity:.4f} | Prix d'achat: {prix_achat} | Actuel: {price_now:.4f}")

# === Boucle principale ===
while True:
    try:
        print("\n======= MONEYMANCER DASHBOARD =======")
        balance_eur = float(api.query_private('Balance')['result'].get('ZEUR', 0))
        print(f"Solde disponible : {balance_eur:.2f} €")
        print(f"XP actuelle : {xp}")
        print(f"Mise actuelle : {min_purchase_eur:.2f} €")

        check_positions()

        for crypto in cryptos:
            if crypto in achat_prix:
                continue
            if balance_eur < min_purchase_eur:
                continue

            pair = f'{crypto}EUR'
            print(f"Achat de {crypto} pour {min_purchase_eur}€ en cours...")
            if buy_crypto(pair, min_purchase_eur):
                price = get_price(pair)
                if price:
                    achat_prix[crypto] = price
                    sauvegarder_achat_prix()
                    print(f"Prix d'achat {crypto} : {price:.4f}")

        print("[Pause de 10 minutes avant la prochaine analyse...]")
        time.sleep(600)

    except Exception as e:
        print(f"[ERREUR GLOBALE] : {e}")
        time.sleep(60)

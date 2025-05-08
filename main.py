import time
import krakenex
import os

# Connexion Kraken API
KRAKEN_API_KEY = os.getenv('KRAKEN_API_KEY')
KRAKEN_API_SECRET = os.getenv('KRAKEN_API_SECRET')

api = krakenex.API(key=KRAKEN_API_KEY, secret=KRAKEN_API_SECRET)
print("MONEYMANCER EN MARCHE !")

# Config
cryptos = ['BTC', 'ETH', 'SOL', 'AVAX', 'LINK', 'XRP', 'MATIC', 'ADA']
crypto_symbols = {
    'BTC': 'XXBT',
    'ETH': 'XETH',
    'SOL': 'SOL',
    'AVAX': 'AVAX',
    'LINK': 'LINK',
    'XRP': 'XXRP',
    'MATIC': 'MATIC',
    'ADA': 'ADA'
}
min_purchase_eur = 5.0
take_profit = 0.05
stop_loss = -0.05
xp = 0
achat_prix = {}

# Obtenir le prix actuel
def get_price(pair):
    try:
        response = api.query_public('Ticker', {'pair': pair})
        price = float(response['result'][list(response['result'].keys())[0]]['c'][0])
        return price
    except Exception as e:
        print(f"Erreur prix {pair} : {e}")
        return None

# Achat

def buy_crypto(pair, amount_eur):
    try:
        response = api.query_private('AddOrder', {
            'pair': pair,
            'type': 'buy',
            'ordertype': 'market',
            'volume': str(amount_eur),
            'oflags': 'viqc'
        })
        print(f"[ACHAT OK] {pair} : {response}")
        return True
    except Exception as e:
        print(f"[ERREUR ACHAT] {pair} : {e}")
        return False

# Vente

def sell_crypto(pair, volume):
    try:
        response = api.query_private('AddOrder', {
            'pair': pair,
            'type': 'sell',
            'ordertype': 'market',
            'volume': str(volume),
            'oflags': 'viqc'
        })
        print(f"[VENTE OK] {pair} : {response}")
        return True
    except Exception as e:
        print(f"[ERREUR VENTE] {pair} : {e}")
        return False

# Vérifier les positions
def check_positions():
    global xp
    balances = api.query_private('Balance')['result']
    print("===== MONEYMANCER DASHBOARD =====")
    balance_eur = float(balances.get('ZEUR', 0))
    print(f"Solde disponible : {balance_eur:.2f} ")
    print(f"XP actuelle : {xp}")
    print(f"Mise actuelle : {min_purchase_eur:.2f} ")
    print("\n----- Portefeuille en suivi -----")

    for crypto in cryptos:
        asset_code = crypto_symbols.get(crypto, crypto)
        quantity = float(balances.get(asset_code, 0))
        pair = f"{crypto}EUR"

        if quantity > 0:
            prix_achat = achat_prix.get(crypto)
            prix_actuel = get_price(pair)
            if prix_achat:
                variation = (prix_actuel - prix_achat) / prix_achat
                print(f"{crypto} ➔ Quantité: {quantity:.4f} | Prix d'achat: {prix_achat:.2f} | Variation: {variation*100:.2f}%")
                if variation >= take_profit:
                    print(f"[+ PROFIT] {crypto} vendu automatiquement")
                    if sell_crypto(pair, quantity):
                        xp += 1
                        achat_prix.pop(crypto)
                elif variation <= stop_loss:
                    print(f"[- PERTE] {crypto} vendu automatiquement")
                    if sell_crypto(pair, quantity):
                        xp += 1
                        achat_prix.pop(crypto)
            else:
                print(f"{crypto} ➔ Quantité: {quantity:.4f} | Prix d'achat: Non défini")
        else:
            print(f"{crypto} ➔ Non acheté")

# Boucle principale
while True:
    try:
        check_positions()
        print("\n[Pause de 10 minutes avant la prochaine analyse...]")
        time.sleep(600)
    except Exception as e:
        print(f"[ERREUR GLOBALE] {e}")
        time.sleep(60)

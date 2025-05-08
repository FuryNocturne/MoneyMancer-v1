import os
import time
import krakenex

# Connexion 
KRAKEN_API_KEY = os.getenv("KRAKEN_API_KEY")
KRAKEN_API_SECRET = os.getenv("KRAKEN_API_SECRET")
api = krakenex.API(key=KRAKEN_API_KEY, secret=KRAKEN_API_SECRET)

print("MONEYMANCER EN MARCHE !")

# Configuration
cryptos = ['BTC', 'ETH', 'SOL', 'AVAX', 'LINK', 'XRP', 'MATIC', 'ADA']
min_purchase_eur = 5.0
take_profit = 0.05
stop_loss = -0.05
xp = 0
achat_prix = {}

# Alias Kraken pour chaque crypto
kraken_aliases = {
    'BTC': ['XBT', 'XXBT', 'BTC'],
    'ETH': ['ETH', 'XETH'],
    'SOL': ['SOL'],
    'AVAX': ['AVAX'],
    'LINK': ['LINK', 'XLINK'],
    'XRP': ['XRP', 'XXRP'],
    'MATIC': ['MATIC', 'XMATIC'],
    'ADA': ['ADA', 'XADA']
}

def get_price(pair):
    try:
        response = api.query_public('Ticker', {'pair': pair})
        return float(response['result'][list(response['result'].keys())[0]]['c'][0])
    except:
        return None

def buy_crypto(pair, amount_eur):
    try:
        response = api.query_private('AddOrder', {
            'pair': pair,
            'type': 'buy',
            'ordertype': 'market',
            'volume': str(amount_eur),
            'oflags': 'viqc'
        })
        print(f"Achat de {pair} réussi !")
        return True
    except Exception as e:
        print(f"[ERREUR ACHAT] {pair} : {e}")
        return False

def sell_crypto(pair, volume):
    try:
        response = api.query_private('AddOrder', {
            'pair': pair,
            'type': 'sell',
            'ordertype': 'market',
            'volume': str(volume),
            'oflags': 'viqc'
        })
        print(f"Vente de {pair} réussie !")
        return True
    except Exception as e:
        print(f"[ERREUR VENTE] {pair} : {e}")
        return False

def check_positions():
    global xp
    balances = api.query_private('Balance')['result']

    print("\n================ MONEYMANCER DASHBOARD ================")
    balance_eur = float(balances.get('ZEUR', 0.0))
    print(f"Solde disponible : {balance_eur:.2f} €")
    print(f"XP actuelle : {xp}")
    print(f"Mise actuelle : {min_purchase_eur:.2f} €")
    print("\n----- Portefeuille en suivi -----")

    for crypto in cryptos:
        aliases = kraken_aliases.get(crypto, [crypto])
        found = False
        for alias in aliases:
            balance = float(balances.get(f'X{alias}', balances.get(f'{alias}', 0.0)))
            if balance > 0:
                found = True
                pair = f'{crypto}EUR'
                prix_achat = achat_prix.get(crypto, None)
                prix_now = get_price(pair)
                if prix_now and prix_achat:
                    variation = (prix_now - prix_achat) / prix_achat
                    print(f"{crypto} ➔ Quantité: {balance:.4f} | Prix d'achat: {prix_achat:.2f} | Prix actuel: {prix_now:.2f} | Variation: {variation*100:.2f}%")
                    if variation >= take_profit:
                        print(f"[+ PROFIT] Vente automatique de {crypto} !")
                        if sell_crypto(pair, balance):
                            xp += 1
                            achat_prix.pop(crypto, None)
                    elif variation <= stop_loss:
                        print(f"[- PERTE] Vente automatique de {crypto} pour limiter les pertes.")
                        if sell_crypto(pair, balance):
                            xp += 1
                            achat_prix.pop(crypto, None)
                else:
                    print(f"{crypto} ➔ Quantité: {balance:.4f} | Prix d'achat: Non défini")
                break
        if not found:
            print(f"{crypto} ➔ Non acheté")

while True:
    try:
        check_positions()
        print("\n[Pause de 10 minutes avant la prochaine analyse...]")
        time.sleep(600)
    except Exception as e:
        print(f"[ERREUR GLOBALE] {e}")
        time.sleep(60)

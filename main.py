
import time
import os
import krakenex

# Connexion API Kraken
KRAKEN_API_KEY = os.getenv("KRAKEN_API_KEY")
KRAKEN_API_SECRET = os.getenv("KRAKEN_API_SECRET")

api = krakenex.API(key=KRAKEN_API_KEY, secret=KRAKEN_API_SECRET)
print("MoneyMancer connecté à Kraken | Démarrage du trading automatique...")

# Config
cryptos = ["ADA", "SOL", "AVAX", "LINK", "XRP", "MATIC"]
min_purchase_eur = 5.0
take_profit = 0.05   # +5%
stop_loss = -0.05    # -5%
xp = 0

# Suivi des prix d'achat
achat_prix = {}

# Fonction : récupérer le prix actuel d’une paire
def get_price(pair):
    try:
        response = api.query_public("Ticker", {"pair": pair})
        return float(response["result"][list(response["result"].keys())[0]]["c"][0])
    except Exception as e:
        print(f"[ERREUR PRIX] {pair} : {e}")
        return None

# Fonction : acheter
def buy_crypto(pair, amount_eur):
    try:
        response = api.query_private("AddOrder", {
            "pair": pair,
            "type": "buy",
            "ordertype": "market",
            "volume": str(amount_eur),
            "oflags": "viqc"
        })
        print(f"[ACHAT] Réponse : {response}")
        return True
    except Exception as e:
        print(f"[ERREUR ACHAT] {pair} : {e}")
        return False

# Fonction : vendre
def sell_crypto(pair, volume):
    try:
        response = api.query_private("AddOrder", {
            "pair": pair,
            "type": "sell",
            "ordertype": "market",
            "volume": str(volume),
            "oflags": "viqc"
        })
        print(f"[VENTE] Réponse : {response}")
        return True
    except Exception as e:
        print(f"[ERREUR VENTE] {pair} : {e}")
        return False

# Analyse des positions ouvertes
def check_positions():
    global xp
    try:
        balances = api.query_private("Balance")["result"]
    except:
        print("[ERREUR] Impossible de récupérer les soldes.")
        return

    for crypto in cryptos:
        asset_code = f"X{crypto}"
        quantity = float(balances.get(asset_code, 0))
        if quantity <= 0:
            continue

        pair = f"{crypto}EUR"
        price_now = get_price(pair)
        if not price_now:
            continue

        prix_achat = achat_prix.get(crypto)
        if not prix_achat:
            continue

        variation = (price_now - prix_achat) / prix_achat
        print(f"[SUIVI] {crypto} | Achat : {prix_achat:.3f}€ | Actuel : {price_now:.3f}€ | Variation : {variation*100:.2f}%")

        if variation >= take_profit:
            print(f"[+ PROFIT] {crypto} → Vente automatique")
            if sell_crypto(pair, quantity):
                xp += 1
                achat_prix.pop(crypto)
        elif variation <= stop_loss:
            print(f"[- PERTE] {crypto} → Vente automatique pour limiter la perte")
            if sell_crypto(pair, quantity):
                xp += 1
                achat_prix.pop(crypto)

# Boucle principale
while True:
    try:
        check_positions()

        balance_eur = float(api.query_private("Balance")["result"].get("ZEUR", 0))
        print(f"[SOLDE] Quantité EUR : {balance_eur:.2f}€")

        for crypto in cryptos:
            pair = f"{crypto}EUR"
            if balance_eur >= min_purchase_eur and crypto not in achat_prix:
                price = get_price(pair)
                print(f"[ANALYSE] {crypto} → Prix actuel : {price}€")
                print(f"[DÉCLENCHEMENT] Achat de {crypto} pour {min_purchase_eur}€")
                if buy_crypto(pair, min_purchase_eur):
                    prix_achat = get_price(pair)
                    if prix_achat:
                        achat_prix[crypto] = prix_achat
                        print(f"[LOG] Prix d'achat {crypto} enregistré : {prix_achat}€")

        print(f"[XP] Total des actions : {xp} | Pause de 10 minutes...
")
        time.sleep(600)

    except Exception as e:
        print(f"[ERREUR GLOBALE] {e}")
        time.sleep(60)

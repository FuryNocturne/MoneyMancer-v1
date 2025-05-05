import os
import time
from utils import get_price, buy_crypto, sell_crypto, get_balances
from dashboard import afficher_dashboard

# === Configuration API ===
KRAKEN_API_KEY = os.getenv('KRAKEN_API_KEY')
KRAKEN_API_SECRET = os.getenv('KRAKEN_API_SECRET')

import krakenex
api = krakenex.API(key=KRAKEN_API_KEY, secret=KRAKEN_API_SECRET)

# === Configuration du bot ===
cryptos = ['BTC', 'ETH', 'SOL', 'AVAX', 'LINK', 'XRP', 'MATIC', 'ADA']
min_purchase_eur = 5.00
take_profit = 0.05    # +5%
stop_loss = -0.05     # -5%
xp = 0
mise_actuelle = min_purchase_eur
achat_prix = {}

# === Fonction principale ===
def trading_loop():
    global xp, mise_actuelle, achat_prix

    while True:
        try:
            balances = get_balances(api)
            solde_eur = float(balances.get('ZEUR', 0))

            # === Suivi et revente automatique ===
            for crypto in cryptos:
                asset_code = f'X{crypto}'
                if asset_code not in balances:
                    continue

                quantite = float(balances.get(asset_code, 0))
                if quantite <= 0:
                    continue

                pair = f'{crypto}EUR'
                prix_actuel = get_price(api, pair)
                prix_achat = achat_prix.get(crypto)

                if not prix_actuel or not prix_achat:
                    continue

                variation = (prix_actuel - prix_achat) / prix_achat

                if variation >= take_profit:
                    print(f"[+ PROFIT] {crypto} : +{variation*100:.2f}% → Vente automatique !")
                    if sell_crypto(api, pair, quantite):
                        xp += 1
                        achat_prix.pop(crypto)
                elif variation <= stop_loss:
                    print(f"[- PERTE] {crypto} : {variation*100:.2f}% → Vente automatique pour limiter les pertes.")
                    if sell_crypto(api, pair, quantite):
                        xp += 1
                        achat_prix.pop(crypto)

            # === Achats automatiques ===
            for crypto in cryptos:
                pair = f'{crypto}EUR'
                if solde_eur >= mise_actuelle and crypto not in achat_prix:
                    print(f"Achat de {crypto} pour {mise_actuelle} €...")
                    if buy_crypto(api, pair, mise_actuelle):
                        prix = get_price(api, pair)
                        if prix:
                            achat_prix[crypto] = prix
                            print(f"Prix d'achat enregistré pour {crypto} : {prix:.2f} €")
                        solde_eur -= mise_actuelle

            # === Affichage Dashboard ===
            afficher_dashboard(api, cryptos, achat_prix, xp, mise_actuelle)

            print("\n[Pause de 10 minutes avant la prochaine analyse...]\n")
            time.sleep(600)

        except Exception as e:
            print(f"[ERREUR GLOBALE] : {e}")
            time.sleep(60)

# === Lancement ===
if __name__ == "__main__":
    print("=== MONEYMANCER EN MARCHE ===")
    trading_loop()

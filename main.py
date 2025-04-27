import os
import time
from utils import get_balance, get_price, buy_crypto, sell_crypto

TRADING_PAIRS = ["XXBTZEUR", "XETHZEUR", "XLINKZEUR", "XXRPZEUR", "MATICZEUR", "ADA/EUR", "SOL/EUR", "AVAX/EUR"]

def main():
    print("MoneyMancer bot lancé !")
    while True:
        for pair in TRADING_PAIRS:
            try:
                # Récupère solde (spot) pour l'asset
                asset = pair.split('/')[0] if '/' in pair else pair.replace('ZEUR', '')
                balance = get_balance(asset)
                price = get_price(pair)

                print(f"\n--- {pair} ---")
                print(f"Solde disponible ({asset}): {balance}")
                print(f"Prix actuel : {price} EUR")

                # Exemple simple d'achat/vente sans indicateurs
                if balance == 0 and price and price < 1000:
                    print("Condition d'achat remplie, test d'ordre BUY")
                    buy_crypto(pair, 0.001)
                elif balance > 0:
                    print("Test d'ordre SELL")
                    sell_crypto(pair, balance)

            except Exception as e:
                print(f"Erreur de traitement {pair} : {e}")

        time.sleep(300)  # 5 minutes entre chaque round

if __name__ == "__main__":
    main()

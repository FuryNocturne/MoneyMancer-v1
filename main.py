import os
import time
from utils import get_balance, get_price, get_indicators, buy_crypto, sell_crypto

TRADING_PAIRS = ["XRP/EUR", "SOL/EUR", "ADA/EUR", "AVAX/EUR", "MATIC/EUR", "LINK/EUR", "BTC/EUR", "ETH/EUR"]

STOP_LOSS_PERCENTAGE = 5  # 5% de perte max avant de vendre
CHECK_INTERVAL = 60  # en secondes

def main():
    print("MoneyMancer bot lancé !")

    while True:
        for pair in TRADING_PAIRS:
            try:
                asset, quote = pair.split("/")
                balance = get_balance(asset)
                price = get_price(pair)

                if price is None:
                    print(f"Erreur get_price pour {pair}")
                    continue

                print(f"--- {asset} ---")
                print(f"Prix actuel : {price}")
                print(f"Solde disponible : {balance}")

                indicators = get_indicators(pair)

                print(f"Indicateurs : {indicators}")

                if indicators["RSI"] < 30:
                    quantity_to_buy = 1
                    buy_crypto(pair, quantity_to_buy)

                if indicators["RSI"] > 70:
                    if balance > 0:
                        sell_crypto(pair, balance)

            except Exception as e:
                print(f"Erreur globale pour {pair} : {e}")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()

from utils import get_balance, get_price, get_indicators, buy_crypto
import time

ASSETS = ["BTC/EUR", "ETH/EUR", "XRP/EUR", "SOL/EUR", "MATIC/EUR", "AVAX/EUR", "ADA/EUR", "LINK/EUR"]

def main():
    print("MoneyMancer Bot LANCÉ !")
    while True:
        for asset in ASSETS:
            print(f"--- {asset} ---")
            balance = get_balance(asset)
            print(f"Solde disponible ({asset.split('/')[0]}) : {balance}")
            price = get_price(asset)
            if price is None:
                continue
            print(f"Prix actuel : {price} EUR")
            indicators = get_indicators(asset)
            print(f"Indicateurs : {indicators}")
            
            if indicators["RSI"] < 30:
                print("Condition d'achat remplie, test d’ordre ACHETER")
                response = buy_crypto(asset, 5)  # on simule 5€ pour l'exemple
                print(f"buy_crypto réponse : {response}")
        time.sleep(60)  # pause 60 secondes entre chaque tour

if __name__ == "__main__":
    main()

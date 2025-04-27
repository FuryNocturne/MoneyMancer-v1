from services_publics import get_prices, get_balance, get_indicators
import time

# Liste des cryptos à surveiller
assets = ["BTC", "ETH", "LINK", "AVAX", "ADA", "SOL", "MATIC", "XRP"]

def main():
    print("MoneyMancer bot lancé !")
    while True:
        for asset in assets:
            try:
                price = get_prices(asset)
                balance = get_balance(asset)
                indicators = get_indicators(asset)

                print(f"\n--- {asset} ---")
                print(f"Prix actuel : {price}")
                print(f"Balance disponible : {balance}")
                print(f"Indicateurs : {indicators}")

            except Exception as e:
                print(f"Erreur de traitement {asset} : {e}")

        time.sleep(10)  # 10 secondes de pause entre chaque boucle

if __name__ == "__main__":
    main()

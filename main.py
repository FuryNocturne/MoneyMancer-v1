import time
from utils import get_balance, get_prices, get_indicators, execute_trade

# Liste des crypto à trader
assets = {
    'BTC': 'XXBTZEUR',
    'ETH': 'XETHZEUR',
    'SOL': 'SOL/EUR',
    'AVAX': 'AVAX/EUR',
    'ADA': 'ADA/EUR',
    'MATIC': 'MATIC/EUR',
    'XRP': 'XXRPZEUR'
}

def main():
    print("MoneyMancer bot lancé ! 🚀")
    while True:
        for asset, pair in assets.items():
            try:
                indicators = get_indicators(pair)
                price = get_prices(pair)
                balance = get_balance(asset)

                print(f"\n--- {asset} ---")
                print(f"Prix actuel : {price}")
                print(f"Solde disponible : {balance}")
                print(f"Indicateurs : {indicators}")

                # STRATÉGIE SIMPLE RSI :
                if indicators['RSI'] < 30:
                    print(f"RSI faible pour {asset}, ACHAT")
                    execute_trade(pair, 'buy', 0.001)
                elif indicators['RSI'] > 70:
                    print(f"RSI élevé pour {asset}, VENTE")
                    execute_trade(pair, 'sell', 0.001)

            except Exception as e:
                print(f"Erreur de traitement {asset} : {e}")

        time.sleep(300)  # Attendre 5 minutes entre chaque cycle

if __name__ == "__main__":
    main()

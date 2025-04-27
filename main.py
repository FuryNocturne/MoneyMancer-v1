from bot import buy_asset, sell_asset
from config import assets, investment_amount, stop_loss, take_profit, rsi_buy_threshold, moving_average_window
from dashboard import update_dashboard
from utils import get_balance, get_prices, get_indicators
import time

def main():
    print("MoneyMancer bot lancé !")
    while True:
        for asset in assets:
            try:
                rsi_value, moving_average = get_indicators(asset)

                if rsi_value is None or moving_average is None:
                    print(f"Erreur de traitement {asset} : Données invalides")
                    continue

                # Ici tu peux ajouter ta logique d'achat/vente selon RSI et MA
                if rsi_value < rsi_buy_threshold:
                    buy_asset(asset, investment_amount)
                else:
                    sell_asset(asset)

                update_dashboard(asset, rsi_value, moving_average)
                
            except Exception as e:
                print(f"Erreur globale pour {asset} : {e}")

        time.sleep(60)  # Attente 60 secondes avant de refaire une boucle

if __name__ == "__main__":
    main()

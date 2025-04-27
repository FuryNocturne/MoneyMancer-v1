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
                # Récupère le solde en euros
                balance_eur = get_balance()

                # Récupère les prix et historiques
                current_price, historical_prices = get_prices(asset)

                # Récupère les indicateurs RSI et Moving Average
                rsi, ma = get_indicators(historical_prices, moving_average_window)

                # Mise à jour du dashboard (facultatif mais conseillé)
                update_dashboard(asset, current_price, rsi, ma)

                # Stratégie d'achat
                if rsi < rsi_buy_threshold and balance_eur >= investment_amount:
                    buy_asset(asset, investment_amount)

                # Stratégie de vente
                sell_asset(asset, current_price, take_profit, stop_loss)

                time.sleep(1)  # Petite pause entre les analyses de chaque asset

            except Exception as e:
                print(f"Erreur lors du traitement de {asset} : {e}")

        time.sleep(60)  # Attendre 1 minute avant de refaire un tour complet

if __name__ == "__main__":
    main()

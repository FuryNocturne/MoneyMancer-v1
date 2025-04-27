import time
from config import assets, investment_amount, stop_loss, take_profit, rsi_buy_threshold, moving_average_window
from utils import get_balance, get_prices, get_indicators
from bot import buy_asset, sell_asset

def main():
    print("MoneyMancer bot lancé !")
    
    while True:
        for symbol in assets:
            try:
                price = get_prices(symbol)
                if price is None:
                    print(f"Prix introuvable pour {symbol}")
                    continue

                balance = get_balance(symbol)
                rsi_value, moving_average = get_indicators(symbol)

                if rsi_value is None or moving_average is None:
                    print(f"Indicateurs non disponibles pour {symbol}")
                    continue

                quantity = investment_amount / price

                if rsi_value < rsi_buy_threshold and balance == 0:
                    print(f"Achat de {quantity:.6f} {symbol}")
                    buy_asset(symbol, quantity)

                elif balance > 0:
                    entry_price = moving_average
                    current_price = price
                    pnl_percentage = (current_price - entry_price) / entry_price * 100

                    if pnl_percentage <= -stop_loss or pnl_percentage >= take_profit:
                        print(f"Vente de {balance:.6f} {symbol} avec PnL de {pnl_percentage:.2f}%")
                        sell_asset(symbol, balance)

            except Exception as e:
                print(f"Erreur de traitement {symbol} : {e}")

        time.sleep(300)

if __name__ == "__main__":
    main()

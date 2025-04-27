from config import assets, investment_amount, stop_loss, take_profit, rsi_buy_threshold, moving_average_window
from bot import buy_asset, sell_asset
from utils import get_balance, get_prices, get_indicators
from dashboard import display_dashboard
import time

def main():
    portfolio = {}
    balance = get_balance()
    print(f"Solde EUR : {balance:.2f} €")

    while True:
        prices = get_prices()
        indicators = get_indicators()

        for asset, price in prices.items():
            rsi = indicators[asset]['RSI']
            ma = indicators[asset]['MA']

            if asset not in portfolio and rsi < rsi_buy_threshold and price > ma:
                quantity = investment_amount / price
                success = buy_asset(asset, quantity)
                if success:
                    portfolio[asset] = {'buy_price': price, 'quantity': quantity}
                    balance -= investment_amount
                    print(f"Acheté {quantity:.6f} {asset} à {price:.2f} €")

            if asset in portfolio:
                bought_at = portfolio[asset]['buy_price']
                quantity = portfolio[asset]['quantity']
                variation = (price - bought_at) / bought_at

                if variation >= take_profit or variation <= -stop_loss:
                    success = sell_asset(asset, quantity)
                    if success:
                        balance += quantity * price
                        del portfolio[asset]
                        print(f"Vendu {quantity:.6f} {asset} à {price:.2f} €")

        display_dashboard(balance, portfolio, prices)
        print("⏳ Attente 60 secondes avant prochain scan...")
        time.sleep(60)

if __name__ == "__main__":
    main()

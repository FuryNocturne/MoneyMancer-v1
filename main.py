import time
import os
from utils import get_balance, get_price, buy_crypto, sell_crypto
from backtest import simulate_backtest, print_backtest_summary
from dotenv import load_dotenv

load_dotenv()

cryptos = ['XXBTZEUR', 'XETHZEUR', 'XLINKZEUR', 'XXRPZEUR', 'MATICZEUR', 'ADA/EUR', 'SOL/EUR', 'AVAX/EUR']
stop_loss_percent = 5

mode = os.getenv('MODE', 'live')

if mode == "backtest":
    print("Mode Backtest activé.")
    results = simulate_backtest(cryptos, stop_loss_percent)
    print_backtest_summary(results)

elif mode == "live":
    print("Mode Trading LIVE activé.")
    while True:
        for pair in cryptos:
            balance = get_balance(pair.split('Z')[0])  # Correction pour Kraken symboles
            price = get_price(pair)
            print(f"Balance {pair}: {balance} | Prix: {price}€")
            time.sleep(2)
        time.sleep(300)  # Attend 5 minutes entre chaque scan
else:
    print("Erreur: Mode inconnu.")

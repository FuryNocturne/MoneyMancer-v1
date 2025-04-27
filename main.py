# == MoneyMancer V7.0 - Golden Soul Overdrive ==

import time
from MoneyMancerV1.config import assets, investment_amount, stop_loss, take_profit, rsi_buy_threshold, moving_average_window
from MoneyMancerV1.bot import scan_market, buy_asset, sell_asset
from MoneyMancerV1.dashboard import display_dashboard
from MoneyMancerV1.utils import load_env_variables, get_balance
from flask import Flask
import threading

# Chargement des variables d'environnement (.env ou Render)
load_env_variables()

# === CONFIGURATION DU BOT ===
scan_interval = 60  # secondes entre chaque scan

# Dictionnaires pour suivre les prix d'achat et les positions
purchase_prices = {name: None for name in assets.keys()}
positions = {name: None for name in assets.keys()}

# === BOUCLE PRINCIPALE ===
def start_bot():
    while True:
        print("\n⚡️=== SCAN DES MARCHÉS EN COURS ===⚡️")
        balance = get_balance()
        print(f"💰 Solde EUR : {balance:.2f} €")

        for name, info in assets.items():
            price, rsi, ma = scan_market(info['pair'])
            if price is None:
                continue

            if positions[name] is None:
                if rsi <= rsi_buy_threshold and price >= ma:
                    print(f"📈 Achat détecté pour {name} à {price:.2f}€ !")
                    if balance >= investment_amount:
                        buy_asset(name, price, investment_amount)
                        purchase_prices[name] = price
                        positions[name] = True
                    else:
                        print(f"⚠️ Solde insuffisant pour acheter {name}.")
            else:
                entry_price = purchase_prices[name]
                variation = (price - entry_price) / entry_price

                if variation <= -stop_loss:
                    print(f"⚡️ Stop Loss atteint pour {name} : {variation*100:.2f}%")
                    sell_asset(name, price)
                    purchase_prices[name] = None
                    positions[name] = None
                elif variation >= take_profit:
                    print(f"⚡️ Take Profit atteint pour {name} : {variation*100:.2f}%")
                    sell_asset(name, price)
                    purchase_prices[name] = None
                    positions[name] = None

        display_dashboard(positions, purchase_prices)
        print("⏳ Attente 60 secondes avant prochain scan...")
        time.sleep(scan_interval)

# Serveur Flask pour Render (garder l'app en ligne)
app = Flask(__name__)

@app.route('/')
def home():
    return "MoneyMancer V7 est actif et prêt à tout exploser !"

# Lancement du bot et du serveur en parallèle
if __name__ == "__main__":
    threading.Thread(target=start_bot).start()
    app.run(host='0.0.0.0', port=10000)

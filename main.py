# == MoneyMancer V7.0 - Golden Soul Overdrive ==

import time
from config import assets, investment_amount, stop_loss, take_profit, rsi_buy_threshold, moving_average_window
from bot import scan_market, buy_asset, sell_asset
from dashboard import display_dashboard
from utils import load_env_variables, get_balance

# Chargement des variables d'environnement (.env ou Render)
load_env_variables()

# === CONFIGURATION DU BOT ===
scan_interval = 60  # secondes entre chaque scan

# Dictionnaires pour suivre les prix d'achat et les positions
purchase_prices = {name: None for name in assets.keys()}
positions = {name: None for name in assets.keys()}

# === BOUCLE PRINCIPALE ===
while True:
    print("\n⚡️=== SCAN DES MARCHÉS EN COURS ===⚡️")
    balance = get_balance()
    print(f"💰 Solde EUR : {balance:.2f} €")

    # Scanne chaque crypto
    for name, info in assets.items():
        price, rsi, ma = scan_market(info['pair'])
        if price is None:
            continue

        if positions[name] is None:
            # Achat
            if rsi <= rsi_buy_threshold and price >= ma:
                print(f"📈 Achat détecté pour {name} à {price:.2f}€ !")
                if balance >= investment_amount:
                    buy_asset(name, price, investment_amount)
                    purchase_prices[name] = price
                    positions[name] = True
                else:
                    print(f"⚠️ Solde insuffisant pour acheter {name}.")
        else:
            # Vente
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

    # Affiche un mini dashboard
    display_dashboard(positions, purchase_prices)

    print("⏳ Attente 60 secondes avant prochain scan...")
    time.sleep(scan_interval)

# == SERVER KEEP-ALIVE POUR RENDER ==
from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "MoneyMancer V7 est en ligne et prêt à faire fortune !"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

# Lance le serveur Flask en parallèle
thread = threading.Thread(target=run_flask)
thread.start()

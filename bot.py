import krakenex
import time
from config import API_KEY, API_SECRET, MODE, AUTOMATIC_TRADING, investment_amount, multiplier_intelligent, rsi_buy_threshold, moving_average_window, take_profit, stop_loss, assets
from utils import send_notification, calculate_rsi, calculate_moving_average

api = krakenex.API(key=API_KEY, secret=API_SECRET)

purchase_prices = {name: None for name in assets.keys()}
price_history = {name: [] for name in assets.keys()}

def get_market_price(pair):
    try:
        response = api.query_public('Ticker', {'pair': pair})
        return float(list(response['result'].values())[0]['c'][0])
    except Exception as e:
        print(f"Erreur récupération prix {pair} : {e}")
        return None

def place_market_order(pair, volume, type_order="buy"):
    try:
        response = api.query_private('AddOrder', {
            'pair': pair,
            'type': type_order,
            'ordertype': 'market',
            'volume': volume
        })
        return response
    except Exception as e:
        print(f"Erreur exécution ordre {type_order} : {e}")
        return None

def scan_market():
    print("\n⚡️ SCAN DES MARCHÉS EN COURS ⚡️")
    try:
        balance = api.query_private('Balance')
        euro_balance = float(balance['result'].get('ZEUR', 0.0))
        print(f"💰 Solde EUR : {euro_balance:.2f} €")
    except Exception as e:
        print(f"Erreur récupération solde : {e}")
        euro_balance = 0.0

    for name, infos in assets.items():
        pair = infos['pair']
        asset = infos['asset']
        price = get_market_price(pair)

        if price is None:
            continue

        price_history[name].append(price)
        if len(price_history[name]) > 100:
            price_history[name].pop(0)

        rsi = calculate_rsi(price_history[name])
        ma = calculate_moving_average(price_history[name])

        print(f"[{name}] Prix: {price:.2f} € | RSI: {rsi:.2f} | MA: {ma:.2f}")

        # Décision achat
        if rsi < rsi_buy_threshold and price > ma:
            if AUTOMATIC_TRADING and euro_balance >= investment_amount:
                volume = investment_amount / price

                if MODE == "intelligent":
                    if rsi < 20:
                        volume = (investment_amount * multiplier_intelligent) / price

                place_market_order(pair, round(volume, 6), type_order="buy")
                print(f"✅ Achat exécuté : {name} pour {round(volume, 6)} à {price:.2f} €")
                purchase_prices[name] = price
                euro_balance -= investment_amount

            else:
                print(f"⚠️ Signal achat détecté sur {name} - Mode observation seulement.")

        # Décision vente
        if purchase_prices[name]:
            entry_price = purchase_prices[name]
            variation = (price - entry_price) / entry_price

            if variation >= take_profit or variation <= stop_loss:
                try:
                    asset_balance = api.query_private('Balance')['result'].get(asset, 0)
                    if float(asset_balance) > 0:
                        place_market_order(pair, asset_balance, type_order="sell")
                        result = "Profit 💰" if variation >= take_profit else "Stop Loss 🚨"
                        print(f"🔔 {result} sur {name} à {price:.2f} € | Variation : {variation*100:.2f}%")
                        purchase_prices[name] = None
                except Exception as e:
                    print(f"Erreur vente automatique : {e}")

    print("\n⏳ Attente 60 secondes avant prochain scan...\n")
    time.sleep(60)

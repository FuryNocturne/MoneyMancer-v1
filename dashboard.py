from config import assets
from bot import price_history, purchase_prices

def show_dashboard():
    print("\n📊 --- MINI DASHBOARD MONEYMANCER --- 📊")

    total_cryptos = 0
    total_value = 0

    for name in assets.keys():
        if price_history[name]:
            latest_price = price_history[name][-1]
            entry_price = purchase_prices[name]

            if entry_price:
                variation = (latest_price - entry_price) / entry_price
                print(f"{name} ➔ Achat à {entry_price:.2f}€ ➔ Maintenant {latest_price:.2f}€ ➔ Variation : {variation*100:.2f}%")
                total_cryptos += 1
                total_value += latest_price
            else:
                print(f"{name} ➔ Pas encore acheté.")

    print(f"\n🎯 Total cryptos en position : {total_cryptos}")
    print(f"💰 Valeur actuelle estimée : {total_value:.2f}€")
    print("🚀 --- Fin du Dashboard --- 🚀\n")

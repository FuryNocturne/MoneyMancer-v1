def display_dashboard(positions, total_value):
    print("\n🚀 --- MINI DASHBOARD MONEYMANCER --- 🚀")
    for asset, data in positions.items():
        if data['quantity'] > 0:
            print(f"{asset} ➔ Achat à {data['buy_price']:.2f}€ ➔ Maintenant {data['current_price']:.2f}€ ➔ Variation : {data['variation']:.2f}%")
        else:
            print(f"{asset} ➔ Pas encore acheté.")
    print(f"\n🧩 Total cryptos en position : {sum(1 for d in positions.values() if d['quantity'] > 0)}")
    print(f"💎 Valeur actuelle estimée : {total_value:.2f}€")
    print("🚀 --- Fin du Dashboard --- 🚀\n")

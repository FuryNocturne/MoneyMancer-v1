# dashboard.py

def update_dashboard(asset, price, rsi, ma):
    """
    Met à jour l'affichage du tableau de bord avec les données du marché.
    
    :param asset: Le nom de l'actif (ex: BTC/EUR)
    :param price: Le prix actuel de l'actif
    :param rsi: La valeur actuelle du RSI
    :param ma: La valeur actuelle de la moyenne mobile
    """
    print("="*50)
    print(f"Actif       : {asset}")
    print(f"Prix actuel : {price:.2f} €")
    print(f"RSI         : {rsi:.2f}")
    print(f"Moyenne mob : {ma:.2f}")
    print("="*50)

import time
import utils

def afficher_dashboard(cryptos, achat_prix):
    print("========== DASHBOARD ==========")
    for crypto in cryptos:
        pair = f"{crypto}EUR"
        prix_actuel = utils.get_price(pair)
        balance = utils.get_balance(f'X{crypto}')
        prix_achat = achat_prix.get(crypto, None)

        print(f"Crypto : {crypto}")
        print(f" - Solde : {balance}")
        if prix_actuel:
            print(f" - Prix actuel : {prix_actuel:.2f}€")
        if prix_achat:
            variation = ((prix_actuel - prix_achat) / prix_achat) * 100
            print(f" - Prix achat : {prix_achat:.2f}€")
            print(f" - Variation : {variation:.2f}%")
        print("-----------------------------")

def start_dashboard(cryptos, achat_prix):
    while True:
        afficher_dashboard(cryptos, achat_prix)
        time.sleep(600)

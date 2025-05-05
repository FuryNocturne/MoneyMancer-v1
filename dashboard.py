import os
import time
from utils import get_balances

def afficher_dashboard(api, cryptos, achat_prix, xp, mise_actuelle):
    os.system('clear' if os.name == 'posix' else 'cls')

    print("========== MONEYMANCER DASHBOARD ==========\n")
    balances = get_balances(api)
    solde_eur = float(balances.get('ZEUR', 0))

    print(f"Solde disponible : {solde_eur:.2f} €")
    print(f"XP actuelle      : {xp}")
    print(f"Mise actuelle    : {mise_actuelle:.2f} €\n")

    print("----- Portefeuille en suivi -----")
    for crypto in cryptos:
        code = f"X{crypto}"
        if code in balances:
            montant = float(balances[code])
            prix = achat_prix.get(crypto, 'Non défini')
            print(f"{crypto} → Quantité: {montant:.4f} | Prix d’achat: {prix if isinstance(prix, float) else prix}")
        else:
            print(f"{crypto} → Non acheté")

    print("\n==========================================\n")

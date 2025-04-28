from utils import get_balance, get_price, buy_crypto, sell_crypto
import time

# Liste des paires qu'on trade
TRADING_PAIRS = ["XXBTZEUR", "XETHZEUR", "XXRPZEUR", "SOL/EUR", "MATIC/EUR", "AVAX/EUR", "ADA/EUR", "LINK/EUR"]

# Montant maximum en EUR par achat
MONTANT_ACHAT_EUR = 1.0

# Définir un solde minimum requis en EUR pour tenter un achat
SOLDE_MINIMUM_EUR = 1.0

def main():
    print("🔥 MoneyMancer connecté à Kraken ! Début du trading automatique...")

    while True:
        for pair in TRADING_PAIRS:
            print(f"\n--- Analyse de {pair} ---")
            try:
                # Lecture du solde EUR disponible
                balance_eur = get_balance('ZEUR')  # 'ZEUR' = euro sur Kraken

                if balance_eur < SOLDE_MINIMUM_EUR:
                    print(f"💰 Solde insuffisant ({balance_eur} EUR). Achat impossible.")
                    continue

                # Lecture du prix actuel de la crypto
                price = get_price(pair.replace("/", ""))
                if price is None:
                    print("❌ Impossible de récupérer le prix. On passe à la suivante.")
                    continue

                print(f"📈 Prix actuel de {pair} : {price} EUR")

                # Si le prix est bas (exemple bidon : moins de 1000€ pour acheter BTC), on achète
                if price < 1000:
                    print(f"📥 Condition remplie : Achat de {pair} pour {MONTANT_ACHAT_EUR} EUR")
                    buy_crypto(pair.replace("/", ""), MONTANT_ACHAT_EUR)
                else:
                    print(f"⏭️ Prix trop haut, pas d'achat pour {pair}")

            except Exception as e:
                print(f"⚠️ Erreur sur {pair} : {e}")

        print("\n⏳ Pause de 10 minutes avant nouveau scan...")
        time.sleep(600)  # 600 secondes = 10 minutes

if __name__ == "__main__":
    main()

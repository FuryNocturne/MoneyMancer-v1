import os
import krakenex

def test_kraken_api():
    api_key = os.getenv("KRAKEN_API_KEY")
    api_secret = os.getenv("KRAKEN_API_SECRET")

    if not api_key or not api_secret:
        print("[ERREUR] Clé API ou clé secrète manquante.")
        return

    api = krakenex.API(key=api_key, secret=api_secret)

    try:
        balance = api.query_private('Balance')
        if 'error' in balance and balance['error']:
            print(f"[ERREUR] API : {balance['error']}")
        else:
            print("[SUCCÈS] Connexion à l’API Kraken réussie.")
            print("[SOLDE] :", balance['result'])
    except Exception as e:
        print(f"[EXCEPTION] Problème de connexion : {e}")

if __name__ == "__main__":
    test_kraken_api()

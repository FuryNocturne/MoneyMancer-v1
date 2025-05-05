import krakenex

# === Initialisation Kraken ===
def init_api(key, secret):
    return krakenex.API(key=key, secret=secret)

# === Obtenir le prix actuel d'une paire (ex: SOL/EUR) ===
def get_price(api, pair):
    try:
        response = api.query_public('Ticker', {'pair': pair})
        return float(response['result'][list(response['result'].keys())[0]]['c'][0])
    except Exception as e:
        print(f"[ERREUR PRIX] {pair} : {e}")
        return None

# === Acheter une crypto via ordre "market" ===
def buy_crypto(api, pair, amount_eur):
    try:
        response = api.query_private('AddOrder', {
            'pair': pair,
            'type': 'buy',
            'ordertype': 'market',
            'volume': str(amount_eur),
            'oflags': 'viqc'
        })
        print(f"[ACHAT] {pair} : {response}")
        return True
    except Exception as e:
        print(f"[ERREUR ACHAT] {pair} : {e}")
        return False

# === Vendre une crypto via ordre "market" ===
def sell_crypto(api, pair, volume):
    try:
        response = api.query_private('AddOrder', {
            'pair': pair,
            'type': 'sell',
            'ordertype': 'market',
            'volume': str(volume),
            'oflags': 'viqc'
        })
        print(f"[VENTE] {pair} : {response}")
        return True
    except Exception as e:
        print(f"[ERREUR VENTE] {pair} : {e}")
        return False

# === Obtenir tous les soldes disponibles sur le compte Kraken ===
def get_balances(api):
    try:
        return api.query_private('Balance')['result']
    except Exception as e:
        print(f"[ERREUR SOLDE] : {e}")
        return {}

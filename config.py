import os
from dotenv import load_dotenv
from numpy import True_

load_dotenv()

# --- Récupération des clés API ---
API_KEY = os.getenv('KRAKEN_API_KEY')
API_SECRET = os.getenv('KRAKEN_API_SECRET')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')

# --- Choix des modes ---
MODE = "intelligent"  # normal ou intelligent
AUTOMATIC_TRADING = "True"  # False = Observation / True = Trading réel

# --- Paramètres Globaux ---
investment_amount = 5.00  # Montant par trade en mode normal
multiplier_intelligent = 2.0  # x2 ou x3 si mode intelligent

rsi_buy_threshold = 35
moving_average_window = 10
take_profit = 0.15
stop_loss = -0.10

# --- Cryptos surveillées ---
assets = {
    'BTC': {'pair': 'BTCEUR', 'asset': 'BTC'},
    'ETH': {'pair': 'ETHEUR', 'asset': 'ETH'},
    'LINK': {'pair': 'LINKEUR', 'asset': 'LINK'},
    'AVAX': {'pair': 'AVAXEUR', 'asset': 'AVAX'},
    'ADA': {'pair': 'ADAEUR', 'asset': 'ADA'},
    'SOL': {'pair': 'SOLEUR', 'asset': 'SOL'},
    'MATIC': {'pair': 'MATICEUR', 'asset': 'MATIC'},
    'XRP': {'pair': 'XRPEUR', 'asset': 'XRP'},
}

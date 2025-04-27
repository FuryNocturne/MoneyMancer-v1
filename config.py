import os

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

MODE = "LIVE"  # "TEST" pour simuler sans vrais achats
investment_amount = 2.5  # Montant investi par achat
stop_loss = -5  # Vente si perte de -5%
take_profit = 5  # Vente si gain de +5%
rsi_buy_threshold = 30  # Acheter si RSI < 30
moving_average_window = 5  # Fenêtre de moyenne mobile
assets = ["BTC", "ETH", "LINK", "AVAX", "ADA", "SOL", "MATIC", "XRP"]

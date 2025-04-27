import random

def calculate_moving_average(prices, window):
    if len(prices) < window:
        return sum(prices) / len(prices)
    return sum(prices[-window:]) / window

def should_buy(rsi, threshold):
    return rsi < threshold

def should_sell(current_price, buy_price, stop_loss, take_profit):
    change_percentage = ((current_price - buy_price) / buy_price) * 100
    return change_percentage <= stop_loss or change_percentage >= take_profit

def get_balance():
    # Simulation de balance pour Kraken (à remplacer par API si besoin)
    return round(random.uniform(10, 100), 2)

def get_prices_get_indicators(asset):
    # Simulation pour récupérer les prix et RSI pour Kraken (à remplacer par l'API)
    current_price = round(random.uniform(0.5, 100), 2)
    historical_prices = [round(random.uniform(0.5, 100), 2) for _ in range(30)]
    rsi = round(random.uniform(20, 80), 2)
    return current_price, historical_prices, rsi

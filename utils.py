import requests
import numpy as np

def send_notification(message, webhook_url):
    try:
        data = {"content": message}
        requests.post(webhook_url, json=data)
    except Exception as e:
        print(f"Erreur notification Discord : {e}")

def calculate_rsi(prices, period=14):
    if len(prices) < period:
        return 50
    deltas = np.diff(prices)
    seed = deltas[:period]
    up = seed[seed > 0].sum() / period
    down = -seed[seed < 0].sum() / period
    rs = up / down if down != 0 else 0
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_moving_average(prices, window=10):
    if len(prices) < window:
        return np.mean(prices)
    return np.mean(prices[-window:])

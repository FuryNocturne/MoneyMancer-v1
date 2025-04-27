import pandas as pd
import random

def simulate_backtest(cryptos, stop_loss_percent=5):
    results = {}
    for crypto in cryptos:
        trades = 0
        wins = 0
        losses = 0
        pnl = 0
        
        for day in range(365):
            buy_price = random.uniform(10, 100)  # Simule un prix d'achat
            sell_price = buy_price * random.uniform(0.90, 1.10)  # Simule la variation de prix
            
            trades += 1
            if sell_price > buy_price:
                pnl += (sell_price - buy_price)
                wins += 1
            elif sell_price <= buy_price * (1 - stop_loss_percent / 100):
                pnl -= (buy_price * stop_loss_percent / 100)
                losses += 1
            else:
                pnl += (sell_price - buy_price)

        results[crypto] = {
            'Trades': trades,
            'Wins': wins,
            'Losses': losses,
            'PnL': round(pnl, 2)
        }
    return results

def print_backtest_summary(results):
    print("\n=== Résultats Backtest 1 An ===")
    for crypto, data in results.items():
        print(f"{crypto} | Trades: {data['Trades']} | Wins: {data['Wins']} | Losses: {data['Losses']} | PnL: {data['PnL']}€")
    print("===============================")

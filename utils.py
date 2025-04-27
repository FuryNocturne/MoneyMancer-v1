def calculate_moving_average(prices, window):
    if len(prices) < window:
        return sum(prices) / len(prices)
    return sum(prices[-window:]) / window

def should_buy(rsi, threshold):
    return rsi < threshold

def should_sell(current_price, buy_price, stop_loss, take_profit):
    change_percentage = ((current_price - buy_price) / buy_price) * 100
    if change_percentage <= stop_loss or change_percentage >= take_profit:
        return True
    return False

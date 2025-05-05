import matplotlib.pyplot as plt

def run_backtest(prix_historique, take_profit=0.05, stop_loss=-0.05):
    position = None
    prix_achat = 0
    profits = []

    for i, prix in enumerate(prix_historique):
        if position is None:
            position = prix
            prix_achat = prix
            continue

        variation = (prix - prix_achat) / prix_achat

        if variation >= take_profit or variation <= stop_loss:
            profits.append(variation)
            position = None

    rendement_total = sum(profits)
    print(f"[BACKTEST] Rendement total : {rendement_total*100:.2f}%")

    plt.plot(profits, label="Trades")
    plt.title("Backtest des variations")
    plt.xlabel("Trades")
    plt.ylabel("Variation (%)")
    plt.legend()
    plt.grid()
    plt.show()

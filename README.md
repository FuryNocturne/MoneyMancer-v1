# MoneyMancer

MoneyMancer est un bot de trading automatique pour la plateforme Kraken. Il utilise les API de Kraken pour acheter et vendre automatiquement des cryptomonnaies selon une stratégie simple basée sur le seuil de take profit et stop loss.

## Fonctionnalités

- Achat automatique de cryptomonnaies si un solde EUR est disponible
- Vente automatique à +5% ou -5% de variation du prix d'achat
- Système d'XP pour suivre les transactions réussies
- Configuration entièrement gérée via les variables d'environnement sur Railway

## Technologies utilisées

- Python
- Krakenex (API Kraken)
- Railway (pour l'hébergement)

## Variables d’environnement nécessaires (Railway)

- `KRAKEN_API_KEY`
- `KRAKEN_API_SECRET`

## Utilisation

Déployez directement sur Railway ou en local avec :
```bash
pip install -r requirements.txt
python main.py
```

## Auteur

Développé avec fierté pour Juju le Moneymancer.

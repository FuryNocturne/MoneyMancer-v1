# MoneyMancer V3 — Bot de Trading Automatisé

MoneyMancer est un bot de trading automatique connecté à Kraken. Il achète, vend, analyse les marchés et fait fructifier ta bankroll avec une stratégie évolutive.

---

## ⚙️ Fonctionnalités

- Achat automatique de cryptomonnaies rentables
- Revente automatique avec système de Take Profit et Stop Loss
- Stratégie de trading basée sur la suite de Fibonacci
- Gestion du capital par paliers
- Système d’XP pour suivre la performance du bot
- Tableau de bord visuel (console)
- Fonctionne en continu sur Railway ou Replit

---

## 📦 Technologies utilisées

- Python 3.11+
- Krakenex (API Kraken)
- python-dotenv (variables d’environnement)
- Railway (déploiement cloud)
- GitHub (versionning)

---

## 🔑 Variables d’environnement

À configurer dans Railway (onglet Variables) ou dans un fichier `.env` local :

```env
KRAKEN_API_KEY=votre_clé_api
KRAKEN_API_SECRET=votre_clé_secrète

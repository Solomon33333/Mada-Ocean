# 🌊 Mada Océan Pro

**Plateforme intelligente de mise en relation pêcheurs-acheteurs à Tuléar, Madagascar**

## 🎯 Fonctionnalités

- ✅ **Marketplace** : Publication et réservation de prises de pêche
- 🧠 **IA Prédictive** : Prédiction des espèces probables (Random Forest + XGBoost)
- 🔌 **Temps Réel** : Notifications instantanées via WebSocket
- 💳 **Orange Money** : Simulation complète de paiement mobile
- 📍 **Géolocalisation** : Carte interactive des pêcheurs actifs
- 📊 **Dashboard** : Statistiques et analytics

## 🛠️ Stack Technique

| Couche | Technologie |
|--------|-------------|
| Backend | Python Flask |
| Base de données | MySQL 8.0 |
| IA/ML | scikit-learn (Random Forest, XGBoost) |
| Temps réel | Flask-SocketIO + WebSocket |
| Frontend | HTML5 + Bootstrap 5 + JavaScript |
| Déploiement | Render / Railway / Ngrok |

## 🚀 Installation rapide

```bash
# 1. Cloner le projet
git clone <url>
cd mada-ocean-pro

# 2. Créer environnement virtuel
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 3. Installer dépendances
pip install -r requirements.txt

# 4. Créer base de données
mysql -u root -p < database/schema.sql

# 5. Générer données et entraîner IA
python data/generate_training_data.py
python train_model.py

# 6. Lancer l'application
python app.py
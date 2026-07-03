#!/bin/bash

echo "=========================================="
echo "   🌊 MADA OCEAN PRO - DÉMARRAGE"
echo "=========================================="
echo ""

# Activer environnement virtuel
echo "[1/5] Activation environnement virtuel..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "❌ Erreur: venv non trouvé"
    exit 1
fi
echo "✅ OK"

# Installer dépendances
echo "[2/5] Vérification dépendances..."
pip install -r requirements.txt -q
echo "✅ OK"

# Vérifier base de données
echo "[3/5] Vérification base de données..."
python -c "from database import db; db.connect(); print('✅ Connexion OK')" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️ Base non trouvée. Création..."
    mysql -u root -p < database/schema.sql
fi
echo "✅ OK"

# Générer données entraînement
echo "[4/5] Génération données entraînement..."
python data/generate_training_data.py 2>/dev/null
echo "✅ OK"

# Entraîner IA si modèles absents
if [ ! -f "models_saves/species_model.joblib" ]; then
    echo "[5/5] Entraînement IA..."
    python train_model.py
else
    echo "[5/5] Modèles IA déjà présents ✅"
fi

echo ""
echo "=========================================="
echo "   🚀 LANCEMENT SERVEUR"
echo "=========================================="
echo "   📍 http://localhost:5000"
echo "=========================================="
echo ""

python app.py
# ==========================================
# SCRIPT D'ENTRAÎNEMENT DU MODÈLE IA
# ==========================================
from ml_model import PredictionPeche
import mysql.connector
import json

print("=" * 60)
print("🌊 MADA OCÉAN - ENTRAÎNEMENT IA")
print("=" * 60)

# Initialiser le prédicteur
predictor = PredictionPeche()

# Entraîner les modèles
print("\n🚀 Démarrage de l'entraînement...")
resultats = predictor.entrainer()

print("\n" + "=" * 60)
print("📊 RÉSULTATS DE L'ENTRAÎNEMENT")
print("=" * 60)
print(f"✅ Accuracy classification espèces : {resultats['accuracy_espece']:.2%}")
print(f"✅ Erreur moyenne quantité        : {resultats['mae_quantite_kg']:.2f} kg")
print(f"✅ Erreur moyenne prix            : {resultats['mae_prix_ar']:.2f} Ar/kg")
print(f"✅ Nombre d'espèces               : {resultats['nb_especes']}")
print("=" * 60)

# Test de prédiction
print("\n🧪 Test de prédiction...")
test_pred = predictor.predire(
    date_cible='2026-07-03',
    port_id=1,
    temp_eau=26.5,
    temp_air=28.0,
    vent=15.0,
    pression=1013.0,
    humidite=75.0,
    precip=2.0,
    phase_lune='Premier Quartier',
    vagues=1.2
)

print("\n📈 PRÉDICTION TEST :")
print(json.dumps(test_pred, indent=2, ensure_ascii=False))
print("\n✅ Entraînement terminé avec succès !")
@echo off
chcp 65001 >nul
title MADA OCEAN PRO - Démarrage

echo ==========================================
echo    🌊 MADA OCEAN PRO - DÉMARRAGE
echo ==========================================
echo.

:: Activer environnement virtuel
echo [1/5] Activation environnement virtuel...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Erreur: venv non trouvé. Lancez: python -m venv venv
    pause
    exit /b 1
)
echo ✅ OK

:: Installer dépendances
echo [2/5] Vérification dépendances...
pip install -r requirements.txt -q
echo ✅ OK

:: Vérifier base de données
echo [3/5] Vérification base de données...
python -c "from database import db; db.connect(); print('✅ Connexion OK')" 2>nul
if errorlevel 1 (
    echo ⚠️ Base non trouvée. Création...
    mysql -u root -p < database\schema.sql
)
echo ✅ OK

:: Générer données entraînement
echo [4/5] Génération données entraînement...
python data\generate_training_data.py 2>nul
echo ✅ OK

:: Entraîner IA si modèles absents
if not exist "models_saves\species_model.joblib" (
    echo [5/5] Entraînement IA...
    python train_model.py
) else (
    echo [5/5] Modèles IA déjà présents ✅
)

echo.
echo ==========================================
echo    🚀 LANCEMENT SERVEUR
echo ==========================================
echo    📍 http://localhost:5000
echo    🔌 WebSocket actif
echo    🧠 IA prête
echo    💳 Orange Money simulé
echo ==========================================
echo.

python app.py

pause
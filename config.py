"""
MADA OCEAN PRO - Configuration centralisée
"""
import os
from dotenv import load_dotenv

# Charger variables d'environnement
load_dotenv()

class Config:
    """Configuration de base"""
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Base de données MySQL
    DB_CONFIG = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'database': os.getenv('DB_NAME', 'mada_ocean_db'),
        'charset': 'utf8mb4',
        'use_unicode': True,
        'autocommit': False
    }
    
    # Hôte et port
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    
    # Chemins
    MODELS_DIR = 'models_saves'
    UPLOAD_DIR = 'static/uploads'
    DATA_DIR = 'data'
    
    # Orange Money (simulation)
    ORANGE_MONEY = {
        'api_key': os.getenv('ORANGE_MONEY_API_KEY', 'sim_key'),
        'merchant_id': os.getenv('ORANGE_MONEY_MERCHANT_ID', 'MADAOCEAN'),
        'callback_url': '/api/paiement/callback'
    }
    
    # IA
    ML_MODELS = {
        'species': 'species_model.joblib',
        'quantity': 'quantity_model.joblib',
        'price': 'price_model.joblib',
        'scaler': 'scaler.joblib',
        'encoder_espece': 'label_encoder_espece.joblib',
        'features_list': 'features_list.joblib'
    }
    
    # Session
    PERMANENT_SESSION_LIFETIME = 86400  # 24 heures
    
    # Pagination
    ITEMS_PER_PAGE = 20

# ==========================================
# MADA OCEAN - MODULE IA DE PRÉDICTION
# ==========================================
import pandas as pd
import numpy as np
import mysql.connector
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, mean_absolute_error, classification_report
import joblib
import warnings
warnings.filterwarnings('ignore')

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'mada_ocean_db'
}

class PredictionPeche:
    def __init__(self):
        self.modele_espece = None
        self.modele_quantite = None
        self.modele_prix = None
        self.scaler = StandardScaler()
        self.label_encoder_espece = LabelEncoder()
        self.label_encoder_port = LabelEncoder()
        
    def charger_donnees_entrainement(self):
        """Charge les données depuis MySQL"""
        conn = mysql.connector.connect(**db_config)
        
        query = """
            SELECT 
                hp.date,
                hp.port_id,
                hp.espece_id,
                hp.quantite_kg,
                hp.prix_moyen_kg,
                hp.nb_bateaux,
                hp.nb_pecheurs,
                hp.technique_peche,
                dm.temperature_eau,
                dm.temperature_air,
                dm.vent_kmh,
                dm.pression_hpa,
                dm.humidite_pct,
                dm.precipitation_mm,
                dm.phase_lunaire,
                dm.hauteur_vagues_m
            FROM historique_peche hp
            JOIN donnees_meteo dm ON hp.date = dm.date AND hp.port_id = dm.port_id
            WHERE hp.date >= DATE_SUB(CURDATE(), INTERVAL 365 DAY)
        """
        
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    
    def preparer_features(self, df):
        """Prépare les features pour l'entraînement"""
        df = df.copy()
        
        # Extraire le mois
        df['mois'] = pd.to_datetime(df['date']).dt.month
        
        # Encoder les variables catégorielles
        df['phase_lunaire_encoded'] = self.label_encoder_port.fit_transform(df['phase_lunaire'].astype(str))
        
        # Features numériques
        features_numeriques = [
            'mois', 'temperature_eau', 'temperature_air', 'vent_kmh',
            'pression_hpa', 'humidite_pct', 'precipitation_mm',
            'hauteur_vagues_m', 'nb_bateaux', 'nb_pecheurs',
            'phase_lunaire_encoded'
        ]
        
        X = df[features_numeriques].fillna(0)
        
        # Normaliser
        X_scaled = self.scaler.fit_transform(X)
        
        # Cible classification : espèce
        y_espece = self.label_encoder_espece.fit_transform(df['espece_id'].astype(str))
        
        # Cible régression : quantité
        y_quantite = df['quantite_kg'].fillna(0)
        
        # Cible régression : prix
        y_prix = df['prix_moyen_kg'].fillna(df['prix_moyen_kg'].mean())
        
        return X_scaled, y_espece, y_quantite, y_prix, features_numeriques
    
    def entrainer(self):
        """Entraîne les modèles de prédiction"""
        print("🧠 Chargement des données...")
        df = self.charger_donnees_entrainement()
        
        if len(df) < 50:
            print("⚠️ Pas assez de données. Utilisation de données simulées.")
            df = self.generer_donnees_simulees(500)
        
        print(f"📊 {len(df)} enregistrements chargés")
        
        print("🔧 Préparation des features...")
        X, y_espece, y_quantite, y_prix, features = self.preparer_features(df)
        
        # Split train/test
        X_train, X_test, y_esp_train, y_esp_test = train_test_split(
            X, y_espece, test_size=0.2, random_state=42
        )
        _, _, y_qte_train, y_qte_test = train_test_split(
            X, y_quantite, test_size=0.2, random_state=42
        )
        _, _, y_prix_train, y_prix_test = train_test_split(
            X, y_prix, test_size=0.2, random_state=42
        )
        
        # === MODÈLE 1 : Classification d'espèce ===
        print("\n🌲 Entraînement Random Forest - Classification...")
        self.modele_espece = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            random_state=42,
            n_jobs=-1
        )
        self.modele_espece.fit(X_train, y_esp_train)
        
        y_esp_pred = self.modele_espece.predict(X_test)
        accuracy_espece = accuracy_score(y_esp_test, y_esp_pred)
        print(f"✅ Accuracy classification: {accuracy_espece:.2%}")
        
        # === MODÈLE 2 : Régression quantité ===
        print("\n📈 Entraînement Gradient Boosting - Quantité...")
        self.modele_quantite = GradientBoostingRegressor(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            random_state=42
        )
        self.modele_quantite.fit(X_train, y_qte_train)
        
        y_qte_pred = self.modele_quantite.predict(X_test)
        mae_qte = mean_absolute_error(y_qte_test, y_qte_pred)
        print(f"✅ Erreur absolue moyenne quantité: {mae_qte:.2f} kg")
        
        # === MODÈLE 3 : Régression prix ===
        print("\n💰 Entraînement Gradient Boosting - Prix...")
        self.modele_prix = GradientBoostingRegressor(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            random_state=42
        )
        self.modele_prix.fit(X_train, y_prix_train)
        
        y_prix_pred = self.modele_prix.predict(X_test)
        mae_prix = mean_absolute_error(y_prix_test, y_prix_pred)
        print(f"✅ Erreur absolue moyenne prix: {mae_prix:.2f} Ar/kg")
        
        # Sauvegarder les modèles
        print("\n💾 Sauvegarde des modèles...")
        joblib.dump(self.modele_espece, 'models_saves/species_model.joblib')
        joblib.dump(self.modele_quantite, 'models_saves/quantity_model.joblib')
        joblib.dump(self.modele_prix, 'models_saves/price_model.joblib')
        joblib.dump(self.scaler, 'models_saves/scaler.joblib')
        joblib.dump(self.label_encoder_espece, 'models_saves/label_encoder_espece.joblib')
        joblib.dump(features, 'models_saves/features_list.joblib')
        
        return {
            'accuracy_espece': accuracy_espece,
            'mae_quantite_kg': mae_qte,
            'mae_prix_ar': mae_prix,
            'nb_especes': len(self.label_encoder_espece.classes_)
        }
    
    def generer_donnees_simulees(self, n=500):
        """Génère des données simulées si pas assez de données réelles"""
        np.random.seed(42)
        
        data = []
        for i in range(n):
            date = pd.Timestamp('2025-01-01') + pd.Timedelta(days=np.random.randint(0, 365))
            data.append({
                'date': date,
                'port_id': np.random.randint(1, 8),
                'espece_id': np.random.randint(1, 13),
                'quantite_kg': np.random.uniform(5, 80),
                'prix_moyen_kg': np.random.uniform(3000, 35000),
                'nb_bateaux': np.random.randint(1, 6),
                'nb_pecheurs': np.random.randint(2, 12),
                'technique_peche': np.random.choice(['Pirogue', 'Filet', 'Palangre', 'Ligne']),
                'temperature_eau': np.random.normal(26, 2),
                'temperature_air': np.random.normal(28, 3),
                'vent_kmh': np.random.exponential(15),
                'pression_hpa': np.random.normal(1013, 5),
                'humidite_pct': np.random.normal(75, 8),
                'precipitation_mm': np.random.exponential(3),
                'phase_lunaire': np.random.choice(['Nouvelle Lune', 'Premier Quartier', 'Pleine Lune', 'Dernier Quartier']),
                'hauteur_vagues_m': np.random.exponential(1.5)
            })
        
        return pd.DataFrame(data)
    
    def predire(self, date_cible, port_id, temp_eau, temp_air, vent, pression, humidite, precip, phase_lune, vagues):
        """Prédit l'espèce, la quantité et le prix pour une date donnée"""
        try:
            # Charger les modèles
            if self.modele_espece is None:
                self.modele_espece = joblib.load('models_saves/species_model.joblib')
                self.modele_quantite = joblib.load('models_saves/quantity_model.joblib')
                self.modele_prix = joblib.load('models_saves/price_model.joblib')
                self.scaler = joblib.load('models_saves/scaler.joblib')
                self.label_encoder_espece = joblib.load('models_saves/label_encoder_espece.joblib')
                self.features = joblib.load('models_saves/features_list.joblib')
        except:
            return {'error': 'Modèles non entraînés. Lancez train_model.py d\'abord.'}
        
        # Préparer les features
        mois = pd.Timestamp(date_cible).month
        
        # Encoder la phase lunaire (approximation simple)
        phases = ['Nouvelle Lune', 'Premier Quartier', 'Pleine Lune', 'Dernier Quartier']
        phase_encoded = phases.index(phase_lune) if phase_lune in phases else 0
        
        features = np.array([[
            mois, temp_eau, temp_air, vent, pression,
            humidite, precip, vagues, 3, 6, phase_encoded
        ]])
        
        features_scaled = self.scaler.transform(features)
        
        # Prédire l'espèce (probabilités)
        probas = self.modele_espece.predict_proba(features_scaled)[0]
        top_3_idx = np.argsort(probas)[-3:][::-1]
        
        # Prédire la quantité
        quantite_predite = max(0, self.modele_quantite.predict(features_scaled)[0])
        
        # Prédire le prix
        prix_suggere = max(0, self.modele_prix.predict(features_scaled)[0])
        
        predictions = []
        for idx in top_3_idx:
            espece_id = int(self.label_encoder_espece.inverse_transform([idx])[0])
            predictions.append({
                'espece_id': espece_id,
                'probabilite': round(float(probas[idx]), 3),
                'quantite_estimee_kg': round(float(quantite_predite * probas[idx]), 1),
                'prix_suggere_kg': round(float(prix_suggere), 2)
            })
        
        return {
            'date_cible': date_cible,
            'predictions': predictions,
            'quantite_totale_estimee': round(float(quantite_predite), 1),
            'prix_moyen_suggere': round(float(prix_suggere), 2),
            'confiance': round(float(max(probas)), 3)
        }
    
    def sauvegarder_prediction_db(self, prediction_data):
        """Sauvegarde la prédiction dans la base de données"""
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        for pred in prediction_data['predictions']:
            cursor.execute("""
                INSERT INTO predictions_ia 
                (date_cible, port_id, espece_id, espece_predite_nom,
                 probabilite_succes, quantite_predite_kg,
                 prix_suggere_kg, modele_utilise, accuracy_modele)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                prediction_data['date_cible'],
                1,  # port_id par défaut
                pred['espece_id'],
                f"Espèce {pred['espece_id']}",
                pred['probabilite'],
                pred['quantite_estimee_kg'],
                pred['prix_suggere_kg'],
                'RandomForest+GradientBoosting',
                0.85
            ))
        
        conn.commit()
        cursor.close()
        conn.close()

# Instance globale
predictor = PredictionPeche()
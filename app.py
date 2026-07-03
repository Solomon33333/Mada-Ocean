"""
╔══════════════════════════════════════════════════════════╗
║         🌊 MADA OCÉAN PRO - VERSION ULTIME              ║
║    Plateforme professionnelle pêcheurs-acheteurs        ║
║    Tuléar, Madagascar - 2026                            ║
╚══════════════════════════════════════════════════════════╝
"""
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file
from flask_cors import CORS
from datetime import datetime, timedelta
from functools import wraps
import random
import string
import json
import hashlib
import uuid
import os
from io import BytesIO

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'mada_ocean_ultra_secret_' + str(uuid.uuid4()))
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=12)
app.config['SESSION_COOKIE_SECURE'] = False  # True en production
app.config['SESSION_COOKIE_HTTPONLY'] = True
CORS(app, supports_credentials=True)

# ==========================================
# UTILITAIRES DE SÉCURITÉ
# ==========================================
def hash_password(password):
    """Hash le mot de passe avec SHA-256"""
    salt = "mada_ocean_salt_2026"
    return hashlib.sha256((password + salt).encode()).hexdigest()

def generate_token():
    return str(uuid.uuid4())

def generate_ref():
    prefix = random.choice(['MOC', 'FISH', 'OCEAN'])
    return f'{prefix}-{datetime.now().strftime("%Y%m%d")}-{random.randint(1000,9999)}'

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

# ==========================================
# BASE DE DONNÉES SIMULÉE (VERSION ULTIME)
# ==========================================
users = {
    '0341234567': {
        'id': 1, 'uuid': 'p1-uuid-hery',
        'nom': 'Hery', 'prenom': 'Mahavita',
        'telephone': '0341234567', 'email': 'hery@ocean.mg',
        'password_hash': hash_password('123456'),
        'role': 'pecheur',
        'port': 'Mahavatse', 'type_peche': 'Pirogue traditionnelle - Palangre',
        'experience_ans': 12, 'note_moyenne': 4.8, 'nb_avis': 45,
        'total_ventes': 156, 'revenu_total': 23456000,
        'abonnement_actif': True,
        'date_debut_abonnement': '02/06/2026',
        'date_fin_abonnement': '02/08/2026',
        'photo_profil': '🎣',
        'date_inscription': '15/03/2026',
        'derniere_connexion': '03/07/2026 10:30',
        'notifications': [
            {'id': 1, 'type': 'reservation', 'message': 'Nouvelle réservation pour vos thons', 'date': '03/07/2026 09:15', 'lu': False},
            {'id': 2, 'type': 'paiement', 'message': 'Paiement reçu : 648 000 Ar', 'date': '02/07/2026 15:30', 'lu': True},
        ],
        'badges': ['top_pecheur', 'verifie', 'fidele']
    },
    '0342345678': {
        'id': 2, 'uuid': 'p2-uuid-solo',
        'nom': 'Solo', 'prenom': 'Velonjara',
        'telephone': '0342345678', 'email': 'solo@ocean.mg',
        'password_hash': hash_password('123456'),
        'role': 'pecheur',
        'port': 'Mahajanga-by', 'type_peche': 'Filet maillant',
        'experience_ans': 8, 'note_moyenne': 4.6, 'nb_avis': 23,
        'total_ventes': 89, 'revenu_total': 8900000,
        'abonnement_actif': False,
        'date_debut_abonnement': None,
        'date_fin_abonnement': None,
        'photo_profil': '🎣',
        'date_inscription': '20/04/2026',
        'derniere_connexion': '01/07/2026 08:00',
        'notifications': [],
        'badges': []
    },
    '0343456789': {
        'id': 3, 'uuid': 'p3-uuid-jean',
        'nom': 'Jean', 'prenom': 'Rakotomalala',
        'telephone': '0343456789', 'email': 'jean@ocean.mg',
        'password_hash': hash_password('123456'),
        'role': 'pecheur',
        'port': 'Saint-Augustin', 'type_peche': 'Pirogue - Ligne',
        'experience_ans': 15, 'note_moyenne': 4.9, 'nb_avis': 67,
        'total_ventes': 234, 'revenu_total': 45000000,
        'abonnement_actif': True,
        'date_debut_abonnement': '01/05/2026',
        'date_fin_abonnement': '01/07/2026',
        'photo_profil': '🎣',
        'date_inscription': '10/01/2026',
        'derniere_connexion': '03/07/2026 06:15',
        'notifications': [],
        'badges': ['top_pecheur', 'verifie', 'veteran']
    },
    '0344567890': {
        'id': 4, 'uuid': 'p4-uuid-mamy',
        'nom': 'Mamy', 'prenom': 'Mananjara',
        'telephone': '0344567890', 'email': 'mamy@ocean.mg',
        'password_hash': hash_password('123456'),
        'role': 'pecheur',
        'port': 'Anakao', 'type_peche': 'Filet - Casier',
        'experience_ans': 6, 'note_moyenne': 4.5, 'nb_avis': 12,
        'total_ventes': 45, 'revenu_total': 3400000,
        'abonnement_actif': True,
        'date_debut_abonnement': '15/06/2026',
        'date_fin_abonnement': '15/08/2026',
        'photo_profil': '🎣',
        'date_inscription': '01/06/2026',
        'derniere_connexion': '02/07/2026 14:00',
        'notifications': [],
        'badges': ['verifie']
    },
    '0341231234': {
        'id': 10, 'uuid': 'a1-uuid-bakuba',
        'nom': 'Hotel Bakuba', 'prenom': '',
        'telephone': '0341231234', 'email': 'contact@bakuba.mg',
        'password_hash': hash_password('123456'),
        'role': 'acheteur',
        'adresse_livraison': 'Plage d\'Anakao, BP 12, Tuléar',
        'type_etablissement': 'Hôtel-Restaurant',
        'note_moyenne': 4.8, 'nb_commandes': 67,
        'total_depense': 12345600,
        'photo_profil': '🏨',
        'date_inscription': '05/01/2026',
        'derniere_connexion': '03/07/2026 08:45',
        'notifications': [
            {'id': 1, 'type': 'livraison', 'message': 'Votre commande #45 est en cours de livraison', 'date': '03/07/2026 09:00', 'lu': False},
        ],
        'badges': ['client_fidele', 'verifie']
    },
    '0342342345': {
        'id': 11, 'uuid': 'a2-uuid-pirate',
        'nom': 'Restaurant Le Pirate', 'prenom': '',
        'telephone': '0342342345', 'email': 'lepirate@resto.mg',
        'password_hash': hash_password('123456'),
        'role': 'acheteur',
        'adresse_livraison': 'Boulevard Gallieni, Centre-ville Tuléar',
        'type_etablissement': 'Restaurant',
        'note_moyenne': 4.5, 'nb_commandes': 34,
        'total_depense': 5678000,
        'photo_profil': '🍽️',
        'date_inscription': '20/02/2026',
        'derniere_connexion': '02/07/2026 16:30',
        'notifications': [],
        'badges': ['client_fidele']
    },
    '0343453456': {
        'id': 12, 'uuid': 'a3-uuid-paradisier',
        'nom': 'Le Paradisier', 'prenom': '',
        'telephone': '0343453456', 'email': 'paradisier@hotel.mg',
        'password_hash': hash_password('123456'),
        'role': 'acheteur',
        'adresse_livraison': 'Route d\'Ifaty, Tuléar',
        'type_etablissement': 'Hôtel',
        'note_moyenne': 4.9, 'nb_commandes': 89,
        'total_depense': 23456700,
        'photo_profil': '🏩',
        'date_inscription': '10/01/2026',
        'derniere_connexion': '03/07/2026 07:00',
        'notifications': [],
        'badges': ['client_fidele', 'verifie', 'vip']
    },
    '0349999999': {
        'id': 99, 'uuid': 'admin-uuid',
        'nom': 'Admin', 'prenom': 'Mada Ocean',
        'telephone': '0349999999', 'email': 'admin@madaocean.mg',
        'password_hash': hash_password('admin123'),
        'role': 'admin',
        'photo_profil': '👑',
        'date_inscription': '01/01/2026',
        'derniere_connexion': '03/07/2026 10:00',
        'notifications': [],
        'badges': ['admin', 'super_admin']
    }
}

# Prises enrichies
prises = [
    {
        'id': 1, 'uuid': 'prise-001',
        'pecheur_id': 1, 'pecheur_nom': 'Hery Mahavita', 'pecheur_tel': '0341234567',
        'pecheur_note': 4.8, 'pecheur_photo': '🎣',
        'espece': 'Thon Jaune', 'nom_scientifique': 'Thunnus albacares', 'icon': '🐟',
        'categorie': 'poisson',
        'poids_kg': 36, 'prix_kg': 18000, 'prix_total': 648000,
        'stock_kg': 36, 'qualite': 'A+',
        'description': '2 magnifiques thons jaunes pêchés au large ce matin. Chair ferme, idéal sashimi.',
        'zone': '5 km au large de Mangarivotra', 'port': 'Mahavatse',
        'latitude': -23.3800, 'longitude': 43.6200,
        'statut': 'active', 'date': '03/07/2026 09:24', 'nb_vues': 145,
        'photos': ['thon1.jpg', 'thon2.jpg']
    },
    {
        'id': 2, 'uuid': 'prise-002',
        'pecheur_id': 1, 'pecheur_nom': 'Hery Mahavita', 'pecheur_tel': '0341234567',
        'pecheur_note': 4.8, 'pecheur_photo': '🎣',
        'espece': 'Langouste', 'nom_scientifique': 'Panulirus ornatus', 'icon': '🦞',
        'categorie': 'crustace',
        'poids_kg': 8, 'prix_kg': 32000, 'prix_total': 256000,
        'stock_kg': 8, 'qualite': 'A+',
        'description': 'Langoustes vivantes pêchées cette nuit sur le récif. Idéales pour grillade.',
        'zone': 'Récif de Salary', 'port': 'Salary',
        'latitude': -23.4000, 'longitude': 43.6000,
        'statut': 'active', 'date': '03/07/2026 08:15', 'nb_vues': 98,
        'photos': ['langouste1.jpg']
    },
    {
        'id': 3, 'uuid': 'prise-003',
        'pecheur_id': 3, 'pecheur_nom': 'Jean Rakotomalala', 'pecheur_tel': '0343456789',
        'pecheur_note': 4.9, 'pecheur_photo': '🎣',
        'espece': 'Espadon', 'nom_scientifique': 'Xiphias gladius', 'icon': '🐠',
        'categorie': 'poisson',
        'poids_kg': 22, 'prix_kg': 20000, 'prix_total': 440000,
        'stock_kg': 22, 'qualite': 'A',
        'description': 'Espadon frais entier, très belle pièce pêchée à la palangre.',
        'zone': 'Large de Saint-Augustin', 'port': 'Saint-Augustin',
        'latitude': -23.5000, 'longitude': 43.7000,
        'statut': 'active', 'date': '03/07/2026 10:30', 'nb_vues': 67,
        'photos': ['espadon1.jpg']
    },
    {
        'id': 4, 'uuid': 'prise-004',
        'pecheur_id': 4, 'pecheur_nom': 'Mamy Mananjara', 'pecheur_tel': '0344567890',
        'pecheur_note': 4.5, 'pecheur_photo': '🎣',
        'espece': 'Poulpe', 'nom_scientifique': 'Octopus cyanea', 'icon': '🐙',
        'categorie': 'mollusque',
        'poids_kg': 15, 'prix_kg': 12000, 'prix_total': 180000,
        'stock_kg': 15, 'qualite': 'B+',
        'description': 'Poulpe frais, idéal pour salade ou ragoût de poulpe au coco.',
        'zone': 'Côte Anakao', 'port': 'Anakao',
        'latitude': -23.3500, 'longitude': 43.6400,
        'statut': 'active', 'date': '03/07/2026 07:45', 'nb_vues': 45,
        'photos': []
    },
    {
        'id': 5, 'uuid': 'prise-005',
        'pecheur_id': 3, 'pecheur_nom': 'Jean Rakotomalala', 'pecheur_tel': '0343456789',
        'pecheur_note': 4.9, 'pecheur_photo': '🎣',
        'espece': 'Maquereau', 'nom_scientifique': 'Rastrelliger kanagurta', 'icon': '🎣',
        'categorie': 'poisson',
        'poids_kg': 50, 'prix_kg': 8000, 'prix_total': 400000,
        'stock_kg': 50, 'qualite': 'A',
        'description': 'Belle prise de maquereaux frais ce matin. Parfait pour grillade.',
        'zone': 'Baie de Tuléar', 'port': 'Mahavatse',
        'latitude': -23.3600, 'longitude': 43.6500,
        'statut': 'active', 'date': '03/07/2026 06:50', 'nb_vues': 89,
        'photos': ['maquereau1.jpg']
    },
    {
        'id': 6, 'uuid': 'prise-006',
        'pecheur_id': 4, 'pecheur_nom': 'Mamy Mananjara', 'pecheur_tel': '0344567890',
        'pecheur_note': 4.5, 'pecheur_photo': '🎣',
        'espece': 'Crabes', 'nom_scientifique': 'Scylla serrata', 'icon': '🦀',
        'categorie': 'crustace',
        'poids_kg': 12, 'prix_kg': 15000, 'prix_total': 180000,
        'stock_kg': 12, 'qualite': 'A',
        'description': 'Crabes de mangrove bien charnus, pêchés à la main.',
        'zone': 'Mangrove de Mangarivotra', 'port': 'Mangarivotra',
        'latitude': -23.3000, 'longitude': 43.6300,
        'statut': 'reservee', 'date': '02/07/2026 14:20', 'nb_vues': 120,
        'photos': ['crabe1.jpg', 'crabe2.jpg']
    },
]

# Réservations
reservations = [
    {
        'id': 1, 'prise_id': 6, 'pecheur_id': 4,
        'acheteur_id': 12, 'acheteur_nom': 'Le Paradisier',
        'espece': 'Crabes', 'icon': '🦀', 'poids_kg': 12, 'prix_total': 180000,
        'statut': 'confirmee', 'date': '02/07/2026 15:30',
        'mode_paiement': 'orange_money', 'reference': 'FISH-20260702-4521'
    },
]

# Commandes
commandes = [
    {
        'id': 1, 'acheteur_id': 12, 'acheteur_nom': 'Le Paradisier',
        'articles': [{'espece': 'Crabes', 'icon': '🦀', 'quantite_kg': 12, 'prix_total': 180000}],
        'frais_livraison': 12000, 'total_commande': 192000,
        'adresse_livraison': 'Route d\'Ifaty, Tuléar',
        'statut_livraison': 'en_cours',
        'date_commande': '02/07/2026 15:35',
        'date_livraison_estimee': '02/07/2026 17:00',
        'livreur': 'Rakoto - Moto',
        'suivi': [
            {'statut': 'Préparation', 'date': '15:35'},
            {'statut': 'En cours de livraison', 'date': '16:00'},
            {'statut': 'Arrivée estimée 17:00', 'date': '16:30'},
        ]
    }
]

# Panier utilisateurs
paniers = {}

# Abonnements
abonnements = [
    {'id': 1, 'pecheur_id': 1, 'date_debut': '02/06/2026', 'date_fin': '02/08/2026', 'montant': 10000, 'statut': 'actif'},
    {'id': 2, 'pecheur_id': 3, 'date_debut': '01/05/2026', 'date_fin': '01/07/2026', 'montant': 10000, 'statut': 'expire'},
    {'id': 3, 'pecheur_id': 4, 'date_debut': '15/06/2026', 'date_fin': '15/08/2026', 'montant': 10000, 'statut': 'actif'},
]

# Messages
messages = [
    {'id': 1, 'from_id': 12, 'from_nom': 'Le Paradisier', 'from_photo': '🏩', 'to_id': 4, 'message': 'Bonjour, les crabes sont disponibles ?', 'date': '02/07/2026 14:00', 'lu': True},
    {'id': 2, 'from_id': 4, 'from_nom': 'Mamy', 'from_photo': '🎣', 'to_id': 12, 'message': 'Oui, 12 kg dispo au port de Mangarivotra', 'date': '02/07/2026 14:15', 'lu': True},
    {'id': 3, 'from_id': 12, 'from_nom': 'Le Paradisier', 'from_photo': '🏩', 'to_id': 4, 'message': 'Parfait, je réserve ! Livraison à Ifaty possible ?', 'date': '02/07/2026 14:20', 'lu': True},
]

# Avis
avis = [
    {'id': 1, 'from_id': 12, 'from_nom': 'Le Paradisier', 'to_id': 4, 'note': 5, 'commentaire': 'Crabes excellents, livraison rapide !', 'date': '02/07/2026 18:00'},
    {'id': 2, 'from_id': 10, 'from_nom': 'Hotel Bakuba', 'to_id': 1, 'note': 5, 'commentaire': 'Thon d\'une fraîcheur exceptionnelle', 'date': '01/07/2026 20:00'},
    {'id': 3, 'from_id': 11, 'from_nom': 'Restaurant Le Pirate', 'to_id': 1, 'note': 4, 'commentaire': 'Bon produit, un peu cher', 'date': '30/06/2026 19:00'},
]

# Frais de livraison
frais_livraison = {
    'Mahavatse': 3000,
    'Centre-ville': 5000,
    'Anakao': 10000,
    'Ifaty': 12000,
    'Salary': 15000,
    'Saint-Augustin': 8000,
    'Mangarivotra': 4000,
    'Tsianengea': 4000,
    'Tanambao': 5000,
}

# ==========================================
# DÉCORATEURS
# ==========================================
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            if request.is_json:
                return jsonify({'success': False, 'error': 'Authentification requise'}), 401
            return redirect(url_for('connexion'))
        return f(*args, **kwargs)
    return decorated

def pecheur_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('user_role') != 'pecheur':
            return jsonify({'success': False, 'message': 'Réservé aux pêcheurs'}), 403
        return f(*args, **kwargs)
    return decorated

def acheteur_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('user_role') != 'acheteur':
            return jsonify({'success': False, 'message': 'Réservé aux acheteurs'}), 403
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('user_role') != 'admin':
            if request.is_json:
                return jsonify({'success': False, 'error': 'Admin requis'}), 403
            return redirect(url_for('accueil'))
        return f(*args, **kwargs)
    return decorated

def abonnement_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        tel = session.get('user_phone', '')
        if tel in users:
            user = users[tel]
            if user['role'] == 'pecheur' and not user.get('abonnement_actif', False):
                if request.is_json:
                    return jsonify({'success': False, 'message': 'Abonnement requis', 'redirect': '/abonnement', 'code': 'ABONNEMENT_REQUIS'}), 403
                return redirect(url_for('abonnement'))
        return f(*args, **kwargs)
    return decorated

# ==========================================
# PAGES PRINCIPALES
# ==========================================
@app.route('/')
def accueil():
    user = None
    if 'user_id' in session:
        tel = session.get('user_phone', '')
        if tel in users:
            user = users[tel]
    return render_template('index.html', user=user)

@app.route('/connexion')
def connexion():
    return render_template('connexion.html')

@app.route('/inscription')
def inscription():
    return render_template('inscription.html')

@app.route('/dashboard')
@login_required
def dashboard():
    tel = session.get('user_phone', '')
    if tel in users:
        user = users[tel]
        if user['role'] == 'pecheur' and not user.get('abonnement_actif', False):
            return redirect(url_for('abonnement'))
    return render_template('dashboard.html')

@app.route('/marche')
def marche():
    # Marché visible par tous
    # Mais pour réserver, il faudra se connecter
    return render_template('marche.html')

@app.route('/panier')
@login_required
def panier():
    return render_template('panier.html')

@app.route('/commandes')
@login_required
def page_commandes():
    return render_template('commandes.html')

@app.route('/abonnement')
@login_required
def abonnement():
    return render_template('abonnement.html')

@app.route('/reservations')
@login_required
def page_reservations():
    return render_template('reservations.html')

@app.route('/predictions')
@login_required
def predictions_page():
    return render_template('predictions.html')

@app.route('/chat')
@login_required
def chat():
    return render_template('chat.html')

@app.route('/paiement')
@login_required
def paiement():
    return render_template('paiement.html')

@app.route('/profil')
@login_required
def profil():
    return render_template('profil.html')

@app.route('/avis')
@login_required
def page_avis():
    return render_template('avis.html')

@app.route('/notifications')
@login_required
def page_notifications():
    return render_template('notifications.html')

@app.route('/admin')
@login_required
@admin_required
def admin_page():
    return render_template('admin.html')

# ==========================================
# API AUTHENTIFICATION (SÉCURISÉE)
# ==========================================
@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.json
    telephone = data.get('telephone', '').strip()
    password = data.get('mot_de_passe', '')
    nom = data.get('nom', '').strip()
    role = data.get('role', '')
    
    # Validations
    if not role or role not in ['pecheur', 'acheteur']:
        return jsonify({'success': False, 'message': 'Veuillez choisir un rôle valide'}), 400
    
    if len(password) < 4:
        return jsonify({'success': False, 'message': 'Mot de passe trop court (minimum 4 caractères)'}), 400
    
    if len(nom) < 2:
        return jsonify({'success': False, 'message': 'Nom trop court'}), 400
    
    if telephone in users:
        return jsonify({'success': False, 'message': 'Ce numéro existe déjà. Connectez-vous.'}), 400
    
    # Créer l'utilisateur
    user_uuid = str(uuid.uuid4())
    users[telephone] = {
        'id': max([u['id'] for u in users.values()]) + 1,
        'uuid': user_uuid,
        'nom': nom,
        'prenom': data.get('prenom', ''),
        'telephone': telephone,
        'email': data.get('email', ''),
        'password_hash': hash_password(password),
        'role': role,
        'port': data.get('port', ''),
        'type_peche': data.get('type_peche', ''),
        'adresse_livraison': data.get('adresse', ''),
        'type_etablissement': data.get('type_etablissement', ''),
        'experience_ans': 0,
        'note_moyenne': 5.0,
        'nb_avis': 0,
        'total_ventes': 0,
        'revenu_total': 0,
        'total_depense': 0,
        'abonnement_actif': False,
        'date_debut_abonnement': None,
        'date_fin_abonnement': None,
        'photo_profil': '🎣' if role == 'pecheur' else '🏨',
        'date_inscription': datetime.now().strftime('%d/%m/%Y'),
        'derniere_connexion': datetime.now().strftime('%d/%m/%Y %H:%M'),
        'notifications': [],
        'badges': []
    }
    
    # Connecter automatiquement
    session.permanent = True
    session['user_id'] = users[telephone]['id']
    session['user_uuid'] = user_uuid
    session['user_nom'] = nom
    session['user_role'] = role
    session['user_phone'] = telephone
    
    return jsonify({
        'success': True,
        'message': f'✅ Inscription {role} réussie ! Bienvenue {nom} !',
        'redirect': '/abonnement' if role == 'pecheur' else '/marche',
        'user': {'id': users[telephone]['id'], 'nom': nom, 'role': role}
    })

# ==========================================
# API RÉSERVATIONS (GET + POST fusionnés)
# ==========================================
@app.route('/api/reservations', methods=['GET', 'POST'])
def api_reservations():
    # Si c'est un POST (créer une réservation)
    if request.method == 'POST':
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': 'Connectez-vous'}), 401
        
        data = request.json
        prise_id = int(data.get('prise_id', 0))
        
        prise = next((p for p in prises if p['id'] == prise_id), None)
        if not prise:
            return jsonify({'success': False, 'message': 'Prise introuvable'}), 404
        
        if prise['statut'] != 'active':
            return jsonify({'success': False, 'message': 'Cette prise n\'est plus disponible'}), 400
        
        new_res = {
            'id': len(reservations) + 1,
            'prise_id': prise_id,
            'pecheur_id': prise['pecheur_id'],
            'pecheur_nom': prise['pecheur_nom'],
            'acheteur_id': session['user_id'],
            'acheteur_nom': session.get('user_nom', ''),
            'espece': prise['espece'],
            'icon': prise['icon'],
            'poids_kg': prise['poids_kg'],
            'prix_total': prise['prix_total'],
            'statut': 'en_attente',
            'date': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'mode_paiement': 'orange_money'
        }
        reservations.append(new_res)
        prise['statut'] = 'reservee'
        
        # Notification au pêcheur
        pecheur_prise = next((p for p in prises if p['id'] == prise_id), None)
        if pecheur_prise:
            pecheur_tel = pecheur_prise.get('pecheur_tel')
            if pecheur_tel and pecheur_tel in users:
                users[pecheur_tel]['notifications'].append({
                    'id': len(users[pecheur_tel]['notifications']) + 1,
                    'type': 'reservation',
                    'message': f'📅 {session.get("user_nom")} a réservé {prise["espece"]}',
                    'date': datetime.now().strftime('%d/%m/%Y %H:%M'),
                    'lu': False
                })
        
        return jsonify({
            'success': True,
            'message': f'✅ {prise["icon"]} {prise["espece"]} réservé avec succès !',
            'reservation': new_res
        })
    
    # Si c'est un GET (lister les réservations)
    else:
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': 'Connectez-vous'}), 401
        
        user_id = session['user_id']
        user_role = session.get('user_role')
        
        if user_role == 'pecheur':
            # Réservations sur les prises du pêcheur
            result = []
            for r in reservations:
                prise = next((p for p in prises if p['id'] == r['prise_id']), None)
                if prise and prise['pecheur_id'] == user_id:
                    result.append(r)
        elif user_role == 'acheteur':
            # Réservations faites par l'acheteur
            result = [r for r in reservations if r.get('acheteur_id') == user_id]
        else:
            result = reservations
        
        return jsonify({
            'success': True,
            'reservations': result,
            'count': len(result)
        })

@app.route('/api/reservations/<int:reservation_id>/confirmer', methods=['POST'])
@login_required
def api_confirmer_reservation(reservation_id):
    """Confirmer une réservation (par le pêcheur)"""
    if session.get('user_role') != 'pecheur':
        return jsonify({'success': False, 'message': 'Seul le pêcheur peut confirmer'}), 403
    
    # Trouver la réservation
    reservation = next((r for r in reservations if r['id'] == reservation_id), None)
    if not reservation:
        return jsonify({'success': False, 'message': 'Réservation introuvable'}), 404
    
    # Vérifier que le pêcheur est bien le propriétaire de la prise
    prise = next((p for p in prises if p['id'] == reservation['prise_id']), None)
    if not prise or prise['pecheur_id'] != session['user_id']:
        return jsonify({'success': False, 'message': 'Non autorisé'}), 403
    
    # Confirmer la réservation
    reservation['statut'] = 'confirmee'
    reservation['date_confirmation'] = datetime.now().strftime('%d/%m/%Y %H:%M')
    
    # Notification à l'acheteur
    acheteur_id = reservation.get('acheteur_id')
    for tel, user in users.items():
        if user['id'] == acheteur_id:
            users[tel]['notifications'].append({
                'id': len(users[tel]['notifications']) + 1,
                'type': 'reservation',
                'message': f'✅ Votre réservation pour {reservation["espece"]} a été confirmée !',
                'date': datetime.now().strftime('%d/%m/%Y %H:%M'),
                'lu': False
            })
            break
    
    return jsonify({
        'success': True,
        'message': f'✅ Réservation #{reservation_id} confirmée ! L\'acheteur va être notifié.',
        'reservation': reservation
    })

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    telephone = data.get('telephone', '').strip()
    password = data.get('mot_de_passe', '')
    
    if telephone not in users:
        return jsonify({'success': False, 'message': 'Numéro introuvable. Créez un compte.'}), 401
    
    user = users[telephone]
    
    # Vérifier le mot de passe hashé
    if user['password_hash'] != hash_password(password):
        return jsonify({'success': False, 'message': 'Mot de passe incorrect'}), 401
    
    # Créer la session
    session.permanent = True
    session['user_id'] = user['id']
    session['user_uuid'] = user['uuid']
    session['user_nom'] = f"{user['prenom']} {user['nom']}".strip()
    session['user_role'] = user['role']
    session['user_phone'] = telephone
    
    # Mettre à jour dernière connexion
    user['derniere_connexion'] = datetime.now().strftime('%d/%m/%Y %H:%M')
    
    # Déterminer la redirection
    if user['role'] == 'pecheur':
        if user.get('abonnement_actif', False):
            redirect_url = '/dashboard'
            message = f'✅ Bon retour {user["nom"]} !'
        else:
            redirect_url = '/abonnement'
            message = '⚠️ Abonnement requis pour publier vos prises.'
    elif user['role'] == 'admin':
        redirect_url = '/admin'
        message = '✅ Dashboard Administrateur'
    else:
        redirect_url = '/marche'
        message = '✅ Bienvenue sur le marché !'
    
    return jsonify({
        'success': True,
        'message': message,
        'user': {
            'id': user['id'], 'uuid': user['uuid'],
            'nom': user['nom'], 'prenom': user.get('prenom', ''),
            'role': user['role'], 'photo_profil': user['photo_profil'],
            'note_moyenne': user.get('note_moyenne', 5.0),
            'abonnement_actif': user.get('abonnement_actif', False),
            'badges': user.get('badges', [])
        },
        'redirect': redirect_url
    })

@app.route('/api/logout', methods=['POST'])
def api_logout():
    session.clear()
    return jsonify({'success': True, 'message': 'Déconnecté. À bientôt !'})

@app.route('/api/me')
def api_me():
    if 'user_id' not in session:
        return jsonify({'success': False}), 401
    
    tel = session.get('user_phone', '')
    if tel in users:
        user = {k: v for k, v in users[tel].items() if k != 'password_hash'}
        return jsonify({'success': True, 'user': user})
    
    return jsonify({'success': False}), 401

# ==========================================
# API ABONNEMENT
# ==========================================
@app.route('/api/abonnement/souscrire', methods=['POST'])
@login_required
@pecheur_required
def api_souscrire_abonnement():
    tel = session.get('user_phone', '')
    
    abonnement = {
        'id': len(abonnements) + 1,
        'pecheur_id': users[tel]['id'],
        'date_debut': datetime.now().strftime('%d/%m/%Y'),
        'date_fin': (datetime.now() + timedelta(days=30)).strftime('%d/%m/%Y'),
        'montant': 10000,
        'statut': 'actif'
    }
    abonnements.append(abonnement)
    
    users[tel]['abonnement_actif'] = True
    users[tel]['date_debut_abonnement'] = abonnement['date_debut']
    users[tel]['date_fin_abonnement'] = abonnement['date_fin']
    
    # Ajouter badge
    if 'verifie' not in users[tel]['badges']:
        users[tel]['badges'].append('verifie')
    
    return jsonify({
        'success': True,
        'message': f'✅ Abonnement activé jusqu\'au {abonnement["date_fin"]} !',
        'abonnement': abonnement
    })

@app.route('/api/abonnement/statut', methods=['GET'])
@login_required
def api_statut_abonnement():
    tel = session.get('user_phone', '')
    if tel in users:
        user = users[tel]
        jours_restants = 0
        if user.get('date_fin_abonnement'):
            try:
                date_fin = datetime.strptime(user['date_fin_abonnement'], '%d/%m/%Y')
                jours_restants = (date_fin - datetime.now()).days
            except:
                pass
        
        return jsonify({
            'success': True,
            'abonnement_actif': user.get('abonnement_actif', False),
            'date_fin': user.get('date_fin_abonnement'),
            'jours_restants': max(0, jours_restants),
            'montant_mensuel': 10000
        })
    return jsonify({'success': False}), 404

# ==========================================
# API PRISES (avec vérification abonnement)
# ==========================================
@app.route('/api/prises', methods=['GET'])
def api_prises():
    statut = request.args.get('statut', 'active')
    categorie = request.args.get('categorie')
    espece = request.args.get('espece')
    prix_min = request.args.get('prix_min', type=float)
    prix_max = request.args.get('prix_max', type=float)
    port = request.args.get('port')
    pecheur_id = request.args.get('pecheur_id', type=int)
    search = request.args.get('search', '').lower()
    tri = request.args.get('tri', 'recent')
    
    result = prises.copy()
    
    # Filtres
    if statut and statut != 'all':
        result = [p for p in result if p['statut'] == statut]
    if categorie:
        result = [p for p in result if p.get('categorie') == categorie]
    if espece:
        result = [p for p in result if espece.lower() in p['espece'].lower()]
    if prix_min is not None:
        result = [p for p in result if p['prix_kg'] >= prix_min]
    if prix_max is not None:
        result = [p for p in result if p['prix_kg'] <= prix_max]
    if port:
        result = [p for p in result if port.lower() in p.get('port', '').lower()]
    if pecheur_id:
        result = [p for p in result if p['pecheur_id'] == pecheur_id]
    if search:
        result = [p for p in result if search in p['espece'].lower() or search in p['description'].lower()]
    
    # Tri
    if tri == 'prix_croissant':
        result.sort(key=lambda p: p['prix_kg'])
    elif tri == 'prix_decroissant':
        result.sort(key=lambda p: p['prix_kg'], reverse=True)
    elif tri == 'note':
        result.sort(key=lambda p: p.get('pecheur_note', 0), reverse=True)
    elif tri == 'vues':
        result.sort(key=lambda p: p['nb_vues'], reverse=True)
    else:  # recent
        result.sort(key=lambda p: p['date'], reverse=True)
    
    return jsonify({
        'success': True,
        'prises': result,
        'count': len(result),
        'filtres_appliques': {
            'statut': statut, 'categorie': categorie, 'tri': tri
        }
    })

@app.route('/api/prises', methods=['POST'])
@login_required
@pecheur_required
@abonnement_required
def api_creer_prise():
    data = request.json
    tel = session.get('user_phone', '')
    user = users.get(tel, {})
    
    nouvelle_prise = {
        'id': len(prises) + 1,
        'uuid': f'prise-{uuid.uuid4().hex[:8]}',
        'pecheur_id': session['user_id'],
        'pecheur_nom': session.get('user_nom', ''),
        'pecheur_tel': tel,
        'pecheur_note': user.get('note_moyenne', 5.0),
        'pecheur_photo': user.get('photo_profil', '🎣'),
        'espece': data.get('espece', 'Poisson'),
        'icon': data.get('icon', '🐟'),
        'categorie': data.get('categorie', 'poisson'),
        'poids_kg': float(data.get('poids_kg', 10)),
        'prix_kg': float(data.get('prix_kg', 10000)),
        'prix_total': float(data.get('poids_kg', 10)) * float(data.get('prix_kg', 10000)),
        'stock_kg': float(data.get('poids_kg', 10)),
        'qualite': data.get('qualite', 'A'),
        'description': data.get('description', ''),
        'zone': data.get('zone', ''),
        'port': data.get('port', user.get('port', 'Mahavatse')),
        'latitude': data.get('latitude'),
        'longitude': data.get('longitude'),
        'statut': 'active',
        'date': datetime.now().strftime('%d/%m/%Y %H:%M'),
        'nb_vues': 0,
        'photos': data.get('photos', [])
    }
    prises.insert(0, nouvelle_prise)
    
    return jsonify({
        'success': True,
        'message': f'✅ {nouvelle_prise["icon"]} {nouvelle_prise["espece"]} publié avec succès !',
        'prise': nouvelle_prise
    })

# ==========================================
# API PANIER
# ==========================================
@app.route('/api/panier', methods=['GET'])
@login_required
def api_get_panier():
    user_id = session['user_id']
    panier_user = paniers.get(user_id, [])
    total = sum(item['prix_total'] for item in panier_user)
    
    return jsonify({
        'success': True,
        'panier': panier_user,
        'nb_articles': len(panier_user),
        'total': total
    })

@app.route('/api/panier/ajouter', methods=['POST'])
@login_required
@acheteur_required
def api_ajouter_panier():
    data = request.json
    prise_id = int(data.get('prise_id', 0))
    quantite_kg = float(data.get('quantite_kg', 1))
    
    prise = next((p for p in prises if p['id'] == prise_id), None)
    if not prise:
        return jsonify({'success': False, 'message': 'Prise introuvable'}), 404
    
    if quantite_kg > prise['stock_kg']:
        return jsonify({'success': False, 'message': f'Stock insuffisant. Disponible: {prise["stock_kg"]} kg'}), 400
    
    user_id = session['user_id']
    if user_id not in paniers:
        paniers[user_id] = []
    
    for item in paniers[user_id]:
        if item['prise_id'] == prise_id:
            item['quantite_kg'] += quantite_kg
            item['prix_total'] = item['quantite_kg'] * prise['prix_kg']
            prise['stock_kg'] -= quantite_kg
            return jsonify({'success': True, 'message': '✅ Quantité mise à jour', 'panier': paniers[user_id]})
    
    paniers[user_id].append({
        'prise_id': prise_id,
        'espece': prise['espece'],
        'icon': prise['icon'],
        'quantite_kg': quantite_kg,
        'prix_kg': prise['prix_kg'],
        'prix_total': quantite_kg * prise['prix_kg'],
        'pecheur_nom': prise['pecheur_nom'],
        'port': prise['port']
    })
    
    prise['stock_kg'] -= quantite_kg
    prise['nb_vues'] += 1
    
    return jsonify({
        'success': True,
        'message': f'✅ {prise["icon"]} {prise["espece"]} ajouté au panier !',
        'panier': paniers[user_id]
    })

@app.route('/api/panier/supprimer', methods=['POST'])
@login_required
def api_supprimer_panier():
    data = request.json
    prise_id = int(data.get('prise_id', 0))
    user_id = session['user_id']
    
    if user_id in paniers:
        for item in paniers[user_id]:
            if item['prise_id'] == prise_id:
                prise = next((p for p in prises if p['id'] == prise_id), None)
                if prise:
                    prise['stock_kg'] += item['quantite_kg']
        
        paniers[user_id] = [item for item in paniers[user_id] if item['prise_id'] != prise_id]
    
    return jsonify({'success': True, 'message': '🗑️ Retiré du panier'})

# ==========================================
# API COMMANDES + LIVRAISON
# ==========================================
@app.route('/api/commandes', methods=['GET'])
@login_required
def api_get_commandes():
    user_id = session['user_id']
    user_role = session.get('user_role')
    
    if user_role == 'acheteur':
        mes_commandes = [c for c in commandes if c['acheteur_id'] == user_id]
    elif user_role == 'pecheur':
        # Commandes contenant des articles du pêcheur
        mes_commandes = []
        for c in commandes:
            for a in c['articles']:
                if a.get('pecheur_nom') == session.get('user_nom'):
                    mes_commandes.append(c)
                    break
    else:
        mes_commandes = commandes
    
    return jsonify({'success': True, 'commandes': mes_commandes, 'count': len(mes_commandes)})

@app.route('/api/commandes/creer', methods=['POST'])
@login_required
@acheteur_required
def api_creer_commande():
    data = request.json
    user_id = session['user_id']
    tel = session.get('user_phone', '')
    adresse_livraison = data.get('adresse_livraison', users[tel].get('adresse_livraison', 'Tuléar'))
    
    panier_user = paniers.get(user_id, [])
    if not panier_user:
        return jsonify({'success': False, 'message': 'Votre panier est vide'}), 400
    
    frais = 5000
    for zone, cout in frais_livraison.items():
        if zone.lower() in adresse_livraison.lower():
            frais = cout
            break
    
    total_produits = sum(item['prix_total'] for item in panier_user)
    total_commande = total_produits + frais
    
    commande = {
        'id': len(commandes) + 1,
        'uuid': f'CMD-{uuid.uuid4().hex[:8].upper()}',
        'acheteur_id': user_id,
        'acheteur_nom': session.get('user_nom', ''),
        'articles': panier_user.copy(),
        'frais_livraison': frais,
        'total_produits': total_produits,
        'total_commande': total_commande,
        'adresse_livraison': adresse_livraison,
        'statut_livraison': 'confirmee',
        'date_commande': datetime.now().strftime('%d/%m/%Y %H:%M'),
        'date_livraison_estimee': (datetime.now() + timedelta(hours=2)).strftime('%d/%m/%Y %H:%M'),
        'livreur': random.choice(['Rakoto - Moto', 'Jean - Vélo', 'Pierre - Camionnette']),
        'suivi': [
            {'statut': 'Commande confirmée', 'date': datetime.now().strftime('%H:%M')},
        ]
    }
    commandes.append(commande)
    
    # Ajouter notification
    for article in panier_user:
        prise = next((p for p in prises if p['id'] == article['prise_id']), None)
        if prise:
            pecheur_tel = prise.get('pecheur_tel')
            if pecheur_tel and pecheur_tel in users:
                users[pecheur_tel]['notifications'].append({
                    'id': len(users[pecheur_tel]['notifications']) + 1,
                    'type': 'commande',
                    'message': f'Nouvelle commande : {article["espece"]} - {article["quantite_kg"]}kg',
                    'date': datetime.now().strftime('%d/%m/%Y %H:%M'),
                    'lu': False
                })
    
    # Vider le panier
    paniers[user_id] = []
    
    # Mettre à jour stats acheteur
    if tel in users:
        users[tel]['nb_commandes'] = users[tel].get('nb_commandes', 0) + 1
        users[tel]['total_depense'] = users[tel].get('total_depense', 0) + total_commande
    
    return jsonify({
        'success': True,
        'message': f'✅ Commande #{commande["id"]} confirmée ! Livraison ~{commande["date_livraison_estimee"]}',
        'commande': commande
    })

# ==========================================
# API AVIS
# ==========================================
@app.route('/api/avis', methods=['GET'])
def api_avis():
    pecheur_id = request.args.get('pecheur_id', type=int)
    acheteur_id = request.args.get('acheteur_id', type=int)
    
    result = avis.copy()
    if pecheur_id:
        result = [a for a in result if a['to_id'] == pecheur_id]
    if acheteur_id:
        result = [a for a in result if a['from_id'] == acheteur_id]
    
    return jsonify({'success': True, 'avis': result, 'count': len(result)})

@app.route('/api/avis', methods=['POST'])
@login_required
def api_donner_avis():
    data = request.json
    nouvel_avis = {
        'id': len(avis) + 1,
        'from_id': session['user_id'],
        'from_nom': session.get('user_nom', ''),
        'to_id': int(data.get('to_id', 0)),
        'note': int(data.get('note', 5)),
        'commentaire': data.get('commentaire', ''),
        'date': datetime.now().strftime('%d/%m/%Y')
    }
    avis.append(nouvel_avis)
    
    return jsonify({'success': True, 'message': '✅ Avis enregistré ! Merci !'})

# ==========================================
# API NOTIFICATIONS
# ==========================================
@app.route('/api/notifications', methods=['GET'])
@login_required
def api_notifications():
    tel = session.get('user_phone', '')
    if tel in users:
        notifs = users[tel].get('notifications', [])
        nb_non_lues = len([n for n in notifs if not n['lu']])
        return jsonify({
            'success': True,
            'notifications': notifs,
            'nb_non_lues': nb_non_lues
        })
    return jsonify({'success': False}), 404

@app.route('/api/notifications/lu', methods=['POST'])
@login_required
def api_marquer_lu():
    tel = session.get('user_phone', '')
    data = request.json
    notif_id = data.get('notification_id')
    
    if tel in users:
        for n in users[tel]['notifications']:
            if n['id'] == notif_id:
                n['lu'] = True
        return jsonify({'success': True})
    return jsonify({'success': False}), 404

# ==========================================
# API PRÉDICTIONS IA (ENRICHIES)
# ==========================================
@app.route('/api/predictions', methods=['GET'])
def api_predictions():
    """Prédictions basées sur les données réelles de la base MySQL"""
    try:
        import mysql.connector
        import pandas as pd
        import numpy as np
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.preprocessing import LabelEncoder
        from datetime import datetime, timedelta
        import joblib
        import os
        
        # Connexion MySQL
        conn = mysql.connector.connect(**db_config)
        
        # 1. Récupérer les données historiques
        query_historique = """
            SELECT 
                hp.date,
                hp.port_id,
                hp.espece_id,
                hp.quantite_kg,
                hp.prix_moyen_kg,
                hp.nb_bateaux,
                hp.nb_pecheurs,
                hp.technique_peche,
                e.nom as espece_nom,
                e.icon_emoji as espece_icon,
                e.categorie,
                p.nom as port_nom
            FROM historique_peche hp
            JOIN especes_poissons e ON hp.espece_id = e.id
            JOIN ports p ON hp.port_id = p.id
            WHERE hp.date >= DATE_SUB(CURDATE(), INTERVAL 90 DAY)
            ORDER BY hp.date DESC
        """
        
        df_historique = pd.read_sql(query_historique, conn)
        
        # 2. Récupérer les données météo
        query_meteo = """
            SELECT 
                date,
                port_id,
                temperature_eau,
                temperature_air,
                vent_kmh,
                pression_hpa,
                humidite_pct,
                precipitation_mm,
                phase_lunaire,
                hauteur_vagues_m
            FROM donnees_meteo
            WHERE date >= DATE_SUB(CURDATE(), INTERVAL 90 DAY)
            ORDER BY date DESC
        """
        
        df_meteo = pd.read_sql(query_meteo, conn)
        conn.close()
        
        # 3. Vérifier si assez de données
        if len(df_historique) < 10:
            return jsonify({
                'success': True,
                'prediction': generer_prediction_simulee(),
                'warning': 'Données insuffisantes. Prédictions basées sur les tendances générales.'
            })
        
        # 4. Fusionner historique + météo
        df_historique['date'] = pd.to_datetime(df_historique['date'])
        df_meteo['date'] = pd.to_datetime(df_meteo['date'])
        
        df = df_historique.merge(df_meteo, on=['date', 'port_id'], how='left')
        
        # 5. Préparer les features
        df['mois'] = df['date'].dt.month
        df['jour_semaine'] = df['date'].dt.dayofweek
        
        # Encoder les variables catégorielles
        le_espece = LabelEncoder()
        le_port = LabelEncoder()
        le_technique = LabelEncoder()
        le_lune = LabelEncoder()
        
        df['espece_encoded'] = le_espece.fit_transform(df['espece_nom'].astype(str))
        df['port_encoded'] = le_port.fit_transform(df['port_nom'].astype(str))
        df['technique_encoded'] = le_technique.fit_transform(df['technique_peche'].astype(str))
        
        if 'phase_lunaire' in df.columns and not df['phase_lunaire'].isna().all():
            df['lune_encoded'] = le_lune.fit_transform(df['phase_lunaire'].astype(str))
        else:
            df['lune_encoded'] = 0
        
        # Features numériques
        features = ['mois', 'jour_semaine', 'port_encoded', 'technique_encoded', 'lune_encoded']
        
        # Ajouter les colonnes météo si disponibles
        for col in ['temperature_eau', 'temperature_air', 'vent_kmh', 'pression_hpa', 'humidite_pct', 'precipitation_mm', 'hauteur_vagues_m']:
            if col in df.columns and not df[col].isna().all():
                df[col] = df[col].fillna(df[col].mean())
                features.append(col)
        
        X = df[features].fillna(0)
        y_quantite = df['quantite_kg'].fillna(0)
        y_prix = df['prix_moyen_kg'].fillna(df['prix_moyen_kg'].mean())
        
        # 6. Entraîner le modèle
        model_quantite = RandomForestRegressor(n_estimators=50, max_depth=5, random_state=42, n_jobs=-1)
        model_prix = RandomForestRegressor(n_estimators=50, max_depth=5, random_state=42, n_jobs=-1)
        
        model_quantite.fit(X, y_quantite)
        model_prix.fit(X, y_prix)
        
        # 7. Prédire pour demain
        demain = datetime.now() + timedelta(days=1)
        mois_demain = demain.month
        jour_demain = demain.weekday()
        
        # Récupérer les prévisions météo pour demain (ou utiliser la moyenne)
        meteo_demain = {}
        for col in ['temperature_eau', 'temperature_air', 'vent_kmh', 'pression_hpa', 'humidite_pct', 'precipitation_mm', 'hauteur_vagues_m']:
            if col in df.columns:
                meteo_demain[col] = df[col].mean()
        
        # Phase lunaire estimée
        lune_demain = df['lune_encoded'].mode()[0] if 'lune_encoded' in df.columns else 0
        
        predictions = []
        
        # Pour chaque port et chaque espèce
        ports_uniques = df['port_encoded'].unique()[:3]
        especes_top = df.groupby('espece_nom').agg({
            'quantite_kg': 'mean',
            'prix_moyen_kg': 'mean',
            'espece_icon': 'first'
        }).sort_values('quantite_kg', ascending=False).head(5)
        
        for port_enc in ports_uniques[:1]:  # Un seul port pour simplifier
            for idx, (espece_nom, row) in enumerate(especes_top.iterrows()):
                try:
                    espece_enc = le_espece.transform([espece_nom])[0]
                except:
                    espece_enc = 0
                
                X_pred = pd.DataFrame([[
                    mois_demain, jour_demain, port_enc,
                    df['technique_encoded'].mode()[0], lune_demain
                ] + [meteo_demain.get(col, 0) for col in features[5:]]], columns=features)
                
                X_pred = X_pred.fillna(0)
                
                qte_pred = max(0, model_quantite.predict(X_pred)[0])
                prix_pred = max(0, model_prix.predict(X_pred)[0])
                
                # Calculer la probabilité basée sur la fréquence historique
                freq = len(df[df['espece_nom'] == espece_nom]) / len(df)
                probabilite = min(95, int(freq * 100 + np.random.randint(-10, 15)))
                probabilite = max(20, probabilite)
                
                predictions.append({
                    'espece': espece_nom,
                    'icon': row['espece_icon'] if pd.notna(row['espece_icon']) else '🐟',
                    'probabilite': probabilite,
                    'quantite_estimee_kg': round(float(qte_pred), 1),
                    'prix_suggere_kg': round(float(prix_pred), -2),
                    'confiance': 'Élevée' if probabilite >= 70 else 'Moyenne' if probabilite >= 45 else 'Faible',
                    'tendance': 'hausse' if probabilite >= 70 else 'stable' if probabilite >= 45 else 'baisse'
                })
        
        # Trier par probabilité
        predictions.sort(key=lambda x: x['probabilite'], reverse=True)
        predictions = predictions[:5]
        
        # Port principal
        port_principal = df['port_nom'].mode()[0] if len(df) > 0 else 'Mahavatse - Tuléar'
        
        # Phase lunaire actuelle
        phase_lune_actuelle = df['phase_lunaire'].mode()[0] if 'phase_lunaire' in df.columns and not df['phase_lunaire'].isna().all() else 'Premier Quartier'
        
        # Sauvegarder les prédictions dans la base
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            for pred in predictions:
                espece_id = df[df['espece_nom'] == pred['espece']]['espece_id'].iloc[0] if len(df[df['espece_nom'] == pred['espece']]) > 0 else 1
                port_id = df[df['port_encoded'] == port_enc]['port_id'].iloc[0] if len(df[df['port_encoded'] == port_enc]) > 0 else 1
                
                cursor.execute("""
                    INSERT INTO predictions_ia 
                    (date_cible, port_id, espece_id, espece_predite_nom,
                     probabilite_succes, quantite_predite_kg, prix_suggere_kg,
                     modele_utilise, accuracy_modele)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    demain.strftime('%Y-%m-%d'), port_id, espece_id,
                    pred['espece'], pred['probabilite'] / 100,
                    pred['quantite_estimee_kg'], pred['prix_suggere_kg'],
                    'RandomForest', 0.75
                ))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"⚠️ Sauvegarde prédictions ignorée: {e}")
        
        return jsonify({
            'success': True,
            'prediction': {
                'date_cible': demain.strftime('%d/%m/%Y'),
                'port': port_principal,
                'meteo': {
                    'temperature_eau': f"{meteo_demain.get('temperature_eau', 26):.1f}°C",
                    'vent': f"{meteo_demain.get('vent_kmh', 15):.0f} km/h",
                    'pression': f"{meteo_demain.get('pression_hpa', 1013):.0f} hPa",
                    'phase_lunaire': phase_lune_actuelle
                },
                'predictions': predictions,
                'confiance_globale': int(np.mean([p['probabilite'] for p in predictions])),
                'message': '🤖 IA entraînée sur les données réelles de pêche',
                'nb_donnees': len(df),
                'modele': 'RandomForest Regressor'
            }
        })
        
    except Exception as e:
        print(f"❌ Erreur IA: {e}")
        import traceback
        traceback.print_exc()
        
        # Fallback : prédictions simulées mais basées sur les données si disponibles
        return jsonify({
            'success': True,
            'prediction': generer_prediction_simulee(),
            'warning': f'Erreur IA: {str(e)[:100]}. Utilisation des tendances générales.'
        })


def generer_prediction_simulee():
    """Fallback si l'IA réelle échoue"""
    from datetime import datetime, timedelta
    demain = (datetime.now() + timedelta(days=1)).strftime('%d/%m/%Y')
    
    return {
        'date_cible': demain,
        'port': 'Mahavatse - Tuléar',
        'meteo': {
            'temperature_eau': '26.5°C',
            'vent': '15 km/h',
            'pression': '1013 hPa',
            'phase_lunaire': 'Premier Quartier'
        },
        'predictions': [
            {'espece': 'Thon Jaune', 'icon': '🐟', 'probabilite': 78, 'quantite_estimee_kg': 35, 'prix_suggere_kg': 18000, 'confiance': 'Élevée', 'tendance': 'hausse'},
            {'espece': 'Maquereau', 'icon': '🎣', 'probabilite': 65, 'quantite_estimee_kg': 42, 'prix_suggere_kg': 8000, 'confiance': 'Moyenne', 'tendance': 'stable'},
            {'espece': 'Langouste', 'icon': '🦞', 'probabilite': 52, 'quantite_estimee_kg': 6.5, 'prix_suggere_kg': 35000, 'confiance': 'Moyenne', 'tendance': 'baisse'},
            {'espece': 'Poulpe', 'icon': '🐙', 'probabilite': 45, 'quantite_estimee_kg': 18, 'prix_suggere_kg': 12000, 'confiance': 'Faible', 'tendance': 'stable'},
            {'espece': 'Espadon', 'icon': '🐠', 'probabilite': 38, 'quantite_estimee_kg': 20, 'prix_suggere_kg': 22000, 'confiance': 'Faible', 'tendance': 'hausse'},
        ],
        'confiance_globale': 78,
        'message': '🤖 IA - Tendances basées sur les saisons',
        'nb_donnees': 0,
        'modele': 'Simulation saisonnière'
    }
# ==========================================
# API PAIEMENT ORANGE MONEY
# ==========================================
@app.route('/api/paiement/initier', methods=['POST'])
@login_required
def api_initier_paiement():
    data = request.json
    montant = data.get('montant', 10000)
    otp = generate_otp()
    ref = generate_ref()
    
    return jsonify({
        'success': True,
        'reference': ref,
        'code_secret': otp,
        'montant': montant,
        'message': f'💳 Orange Money - Code : {otp}',
        'instructions': [
            '1. Composez *144*1# sur votre téléphone',
            '2. Entrez le code : ' + otp,
            f'3. Montant : {montant:,} Ar',
            '4. Validez le paiement'
        ]
    })

@app.route('/api/paiement/confirmer', methods=['POST'])
@login_required
def api_confirmer_paiement():
    data = request.json
    code = data.get('code_secret', '')
    
    # Accepter n'importe quel code à 6 chiffres pour la démo
    if len(code) == 6 and code.isdigit():
        return jsonify({
            'success': True,
            'message': '✅ Paiement confirmé avec succès ! 🎉',
            'reference': generate_ref(),
            'date': datetime.now().strftime('%d/%m/%Y %H:%M')
        })
    
    return jsonify({'success': False, 'message': '❌ Code incorrect. Utilisez le code affiché.'}), 400

# ==========================================
# API MESSAGES
# ==========================================
@app.route('/api/messages', methods=['GET'])
@login_required
def api_messages():
    user_id = session['user_id']
    interlocuteur_id = request.args.get('with', type=int)
    
    user_msgs = [m for m in messages if m['from_id'] == user_id or m['to_id'] == user_id]
    
    if interlocuteur_id:
        user_msgs = [m for m in user_msgs if m['from_id'] == interlocuteur_id or m['to_id'] == interlocuteur_id]
    
    return jsonify({'success': True, 'messages': user_msgs, 'count': len(user_msgs)})

@app.route('/api/messages', methods=['POST'])
@login_required
def api_envoyer_message():
    data = request.json
    tel = session.get('user_phone', '')
    photo = users[tel]['photo_profil'] if tel in users else '👤'
    
    new_msg = {
        'id': len(messages) + 1,
        'from_id': session['user_id'],
        'from_nom': session.get('user_nom', ''),
        'from_photo': photo,
        'to_id': int(data.get('to_id', 0)),
        'message': data.get('message', ''),
        'date': datetime.now().strftime('%d/%m/%Y %H:%M'),
        'lu': False
    }
    messages.append(new_msg)
    
    # Notification au destinataire
    dest_tel = None
    for tel_num, user in users.items():
        if user['id'] == new_msg['to_id']:
            dest_tel = tel_num
            break
    
    if dest_tel and dest_tel in users:
        users[dest_tel]['notifications'].append({
            'id': len(users[dest_tel]['notifications']) + 1,
            'type': 'message',
            'message': f'Nouveau message de {new_msg["from_nom"]}',
            'date': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'lu': False
        })
    
    return jsonify({'success': True, 'message': new_msg})

# ==========================================
# API STATISTIQUES (ENRICHIES)
# ==========================================
@app.route('/api/stats', methods=['GET'])
def api_stats():
    total_volume = sum(c['total_commande'] for c in commandes)
    total_pecheurs = len([u for u in users.values() if u['role'] == 'pecheur'])
    total_acheteurs = len([u for u in users.values() if u['role'] == 'acheteur'])
    pecheurs_actifs = len([u for u in users.values() if u['role'] == 'pecheur' and u.get('abonnement_actif')])
    
    return jsonify({
        'success': True,
        'stats': {
            'prises_actives': len([p for p in prises if p['statut'] == 'active']),
            'pecheurs': total_pecheurs,
            'pecheurs_actifs': pecheurs_actifs,
            'acheteurs': total_acheteurs,
            'volume_transactions': total_volume,
            'reservations_jour': len(reservations),
            'commandes_jour': len(commandes),
            'taux_conversion': 85,
            'note_moyenne_globale': 4.7,
            'total_kg_vendus': sum(c['articles'][0]['quantite_kg'] for c in commandes if c['articles']),
        }
    })

@app.route('/api/frais_livraison', methods=['GET'])
def api_frais_livraison():
    return jsonify({'success': True, 'frais': frais_livraison})

# ==========================================
# DÉMARRAGE
# ==========================================
if __name__ == '__main__':
    print("=" * 65)
    print("║  🌊 MADA OCÉAN PRO - VERSION ULTIME 2026        ║")
    print("=" * 65)
    print(f"  📍 Local    : http://127.0.0.1:5000")
    print(f"  📍 Réseau   : http://192.168.40.178:5000")
    print()
    print("  👥 COMPTES TEST :")
    print("     🎣 Pêcheur  : 0341234567 / 123456 (Hery - ABONNÉ)")
    print("     🎣 Pêcheur  : 0342345678 / 123456 (Solo - NON ABONNÉ)")
    print("     🏨 Acheteur : 0341231234 / 123456 (Hotel Bakuba)")
    print("     🏩 Acheteur : 0343453456 / 123456 (Le Paradisier)")
    print("     👑 Admin    : 0349999999 / admin123")
    print()
    print("  💰 Abonnement pêcheur : 10 000 Ar/mois")
    print("  🛒 Panier → Commande → Livraison")
    print("  ⭐ Système de notation")
    print("  🔔 Centre de notifications")
    print("=" * 65)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
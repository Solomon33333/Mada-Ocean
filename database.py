"""
MADA OCEAN PRO - Gestion base de données MySQL
"""
import mysql.connector
from mysql.connector import Error
from config import Config

class Database:
    """Classe singleton pour la connexion MySQL"""
    
    _instance = None
    _connection = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance
    
    def connect(self):
        """Établit la connexion à MySQL"""
        try:
            self._connection = mysql.connector.connect(**Config.DB_CONFIG)
            return self._connection
        except Error as e:
            print(f"❌ Erreur connexion MySQL: {e}")
            raise
    
    def get_connection(self):
        """Retourne la connexion existante ou en crée une nouvelle"""
        if self._connection is None or not self._connection.is_connected():
            return self.connect()
        return self._connection
    
    def close(self):
        """Ferme la connexion"""
        if self._connection and self._connection.is_connected():
            self._connection.close()
            self._connection = None
    
    def execute_query(self, query, params=None, fetch_one=False, fetch_all=False, commit=False):
        """Exécute une requête SQL"""
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute(query, params or ())
            
            result = None
            if fetch_one:
                result = cursor.fetchone()
            elif fetch_all:
                result = cursor.fetchall()
            
            if commit:
                conn.commit()
                result = cursor.lastrowid
            
            cursor.close()
            return result
        except Error as e:
            print(f"❌ Erreur requête: {e}")
            if commit:
                conn.rollback()
            cursor.close()
            raise
    
    def insert(self, table, data):
        """Insère une ligne dans une table"""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        return self.execute_query(query, tuple(data.values()), commit=True)
    
    def update(self, table, data, where_column, where_value):
        """Met à jour une ligne"""
        set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {where_column} = %s"
        params = tuple(data.values()) + (where_value,)
        return self.execute_query(query, params, commit=True)
    
    def delete(self, table, where_column, where_value):
        """Supprime une ligne"""
        query = f"DELETE FROM {table} WHERE {where_column} = %s"
        return self.execute_query(query, (where_value,), commit=True)
    
    def select_one(self, table, where_column=None, where_value=None, columns='*'):
        """Sélectionne une ligne"""
        if where_column:
            query = f"SELECT {columns} FROM {table} WHERE {where_column} = %s"
            return self.execute_query(query, (where_value,), fetch_one=True)
        query = f"SELECT {columns} FROM {table} LIMIT 1"
        return self.execute_query(query, fetch_one=True)
    
    def select_all(self, table, where_column=None, where_value=None, 
                   order_by=None, limit=None, columns='*'):
        """Sélectionne toutes les lignes correspondantes"""
        query = f"SELECT {columns} FROM {table}"
        params = []
        
        if where_column:
            query += f" WHERE {where_column} = %s"
            params.append(where_value)
        
        if order_by:
            query += f" ORDER BY {order_by}"
        
        if limit:
            query += f" LIMIT {limit}"
        
        return self.execute_query(query, tuple(params) if params else None, fetch_all=True)

# Instance globale
db = Database()

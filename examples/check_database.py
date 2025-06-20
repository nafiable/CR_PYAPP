#!/usr/bin/env python3
"""
Script d'exemple pour vérifier le contenu de la base de données.
Ce fichier peut être utilisé pour diagnostiquer l'état de la base de données
et vérifier que les tables sont correctement créées et peuplées.
"""

import sqlite3
import os
import sys
from pathlib import Path

def check_database(db_path='database.db'):
    """
    Vérifie le contenu de la base de données
    
    Args:
        db_path (str): Chemin vers le fichier de base de données
    """
    
    # Vérifier si le fichier de base existe
    if not os.path.exists(db_path):
        print(f"❌ Le fichier {db_path} n'existe pas")
        return False
    
    print(f"✅ Base de données trouvée: {os.path.getsize(db_path)} bytes")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier les tables existantes
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"\n📋 Tables disponibles: {len(tables)}")
        for table in tables:
            print(f"  - {table[0]}")
        
        # Vérifier la table gestionnaire
        if ('gestionnaire',) in tables:
            cursor.execute("SELECT COUNT(*) FROM gestionnaire")
            count = cursor.fetchone()[0]
            print(f"\n👥 Nombre de gestionnaires: {count}")
            
            if count > 0:
                cursor.execute("SELECT id, code, nom, tel, email FROM gestionnaire LIMIT 5")
                rows = cursor.fetchall()
                print("\n📊 Détails des gestionnaires:")
                for row in rows:
                    print(f"  ID: {row[0]}, Code: {row[1]}, Nom: {row[2]}, Tel: {row[3]}, Email: {row[4]}")
            else:
                print("⚠️  La table gestionnaire est vide")
        else:
            print("❌ La table gestionnaire n'existe pas")
        
        # Vérifier d'autres tables importantes
        important_tables = ['fonds', 'titre', 'pays', 'devise', 'secteur', 'region', 'type_actif']
        print(f"\n📊 État des tables importantes:")
        for table in important_tables:
            if (table,) in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"  {table.capitalize()}: {count} enregistrements")
            else:
                print(f"  {table.capitalize()}: ❌ Table manquante")
        
        # Vérifier les tables de composition
        composition_tables = ['composition_fonds', 'composition_portefeuille', 'composition_indice']
        print(f"\n📊 Tables de composition:")
        for table in composition_tables:
            if (table,) in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"  {table}: {count} enregistrements")
            else:
                print(f"  {table}: ❌ Table manquante")
        
        conn.close()
        print("\n✅ Vérification terminée")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        return False

def check_database_schema(db_path='database.db'):
    """
    Affiche le schéma de la base de données
    
    Args:
        db_path (str): Chemin vers le fichier de base de données
    """
    if not os.path.exists(db_path):
        print(f"❌ Le fichier {db_path} n'existe pas")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print(f"\n🔍 Schéma de la base de données {db_path}:")
        
        # Récupérer toutes les tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            print(f"\n📋 Table: {table_name}")
            
            # Récupérer le schéma de la table
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            for col in columns:
                col_id, col_name, col_type, not_null, default_val, pk = col
                pk_str = " (PK)" if pk else ""
                not_null_str = " NOT NULL" if not_null else ""
                default_str = f" DEFAULT {default_val}" if default_val else ""
                print(f"  {col_name}: {col_type}{not_null_str}{default_str}{pk_str}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification du schéma: {e}")

def main():
    """Fonction principale"""
    print("🔍 Vérification de la base de données")
    print("=" * 50)
    
    # Vérifier le contenu
    success = check_database()
    
    if success:
        # Afficher le schéma si demandé
        if len(sys.argv) > 1 and sys.argv[1] == '--schema':
            check_database_schema()
    
    print("\n" + "=" * 50)
    print("💡 Utilisation:")
    print("  python -m examples.check_database          # Vérifier le contenu")
    print("  python -m examples.check_database --schema # Vérifier le contenu + schéma")

if __name__ == "__main__":
    main() 
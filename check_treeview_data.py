#!/usr/bin/env python3
"""
Script pour vérifier les données nécessaires au treeview
"""

import sqlite3

def check_treeview_data():
    """Vérifie les données nécessaires au treeview"""
    
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        print("🔍 Vérification des données pour le TreeView")
        print("=" * 50)
        
        # 1. Vérifier les gestionnaires
        print("\n1. Gestionnaires:")
        cursor.execute("SELECT id, code, nom, email FROM gestionnaire")
        gestionnaires = cursor.fetchall()
        print(f"   Nombre: {len(gestionnaires)}")
        for gest in gestionnaires:
            print(f"   - ID: {gest[0]}, Code: {gest[1]}, Nom: {gest[2]}, Email: {gest[3]}")
        
        # 2. Vérifier les fonds
        print("\n2. Fonds:")
        cursor.execute("SELECT id, code, nom, type_fonds FROM fonds")
        fonds = cursor.fetchall()
        print(f"   Nombre: {len(fonds)}")
        for fonds_item in fonds:
            print(f"   - ID: {fonds_item[0]}, Code: {fonds_item[1]}, Nom: {fonds_item[2]}, Type: {fonds_item[3]}")
        
        # 3. Vérifier les liens gestionnaire_fonds
        print("\n3. Liens gestionnaire_fonds:")
        cursor.execute("SELECT id_gestionnaire, id_fonds FROM gestionnaire_fonds")
        liens = cursor.fetchall()
        print(f"   Nombre: {len(liens)}")
        for lien in liens:
            print(f"   - Gestionnaire {lien[0]} -> Fonds {lien[1]}")
        
        # 4. Vérifier les titres
        print("\n4. Titres:")
        cursor.execute("SELECT id, code, nom FROM titre")
        titres = cursor.fetchall()
        print(f"   Nombre: {len(titres)}")
        for titre in titres:
            print(f"   - ID: {titre[0]}, Code: {titre[1]}, Nom: {titre[2]}")
        
        # 5. Vérifier les compositions de fonds
        print("\n5. Compositions de fonds:")
        cursor.execute("SELECT id_fonds, id_titre FROM composition_fonds")
        compositions = cursor.fetchall()
        print(f"   Nombre: {len(compositions)}")
        for comp in compositions:
            print(f"   - Fonds {comp[0]} -> Titre {comp[1]}")
        
        # 6. Test de la requête du treeview
        print("\n6. Test de la requête du treeview:")
        for gest_id, gest_code, gest_nom, gest_email in gestionnaires:
            print(f"\n   Gestionnaire: {gest_nom} (ID: {gest_id})")
            cursor.execute("""
                SELECT f.id, f.code, f.nom, f.type_fonds
                FROM fonds f
                JOIN gestionnaire_fonds gf ON f.id = gf.id_fonds
                WHERE gf.id_gestionnaire = ?
                ORDER BY f.nom
            """, (gest_id,))
            fonds_gestionnaire = cursor.fetchall()
            print(f"   Fonds associés: {len(fonds_gestionnaire)}")
            for fonds_id, fonds_code, fonds_nom, fonds_type in fonds_gestionnaire:
                print(f"     - {fonds_nom} ({fonds_code}) - Type: {fonds_type}")
                
                # Test des titres pour ce fonds
                cursor.execute("""
                    SELECT t.id, t.nom, t.code
                    FROM composition_fonds cf
                    JOIN titre t ON cf.id_titre = t.id
                    WHERE cf.id_fonds = ?
                """, (fonds_id,))
                titres_fonds = cursor.fetchall()
                print(f"       Titres: {len(titres_fonds)}")
                for titre_id, titre_nom, titre_code in titres_fonds:
                    print(f"         - {titre_nom} ({titre_code})")
        
        conn.close()
        print("\n✅ Vérification terminée")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    check_treeview_data() 
"""
Démonstration des outils de visualisation.
"""

import pandas as pd
from sqlalchemy import text
from database.connexionsqlLiter import SQLiteConnection
from examples_ui.dataframe_viewer import affiche_dataframe
from examples_ui.open_sqlite_viewer import open_with_sqlite_viewer

def demo_sqlite_viewer():
    """Démontre l'utilisation de SQLite Viewer."""
    print("Ouverture de la base de données avec SQLite Viewer...")
    open_with_sqlite_viewer()

def demo_dataframe_viewer():
    """Démontre l'utilisation du visualiseur de DataFrame."""
    # Connexion à la base de données
    db = SQLiteConnection()
    
    # Exemple 1 : Affichage des gestionnaires
    print("\nAffichage des gestionnaires...")
    with db.engine.connect() as conn:
        query = text("""
            SELECT g.code, g.nom, g.tel, g.contact_principal, g.email,
                   COUNT(gf.id_fonds) as nombre_fonds
            FROM gestionnaire g
            LEFT JOIN gestionnaire_fonds gf ON g.id = gf.id_gestionnaire
            GROUP BY g.id, g.code, g.nom, g.tel, g.contact_principal, g.email
        """)
        df_gestionnaires = pd.read_sql(query, conn)
    
    affiche_dataframe(
        df_gestionnaires,
        title="Liste des Gestionnaires",
        geometry="1200x400"
    )
    
    # Exemple 2 : Affichage des compositions avec statistiques
    print("\nAffichage des compositions...")
    with db.engine.connect() as conn:
        query = text("""
            SELECT 
                cf.date,
                f.code as code_fonds,
                t.code as code_titre,
                s.nom as secteur,
                cf.quantite,
                cf.prix,
                cf.valeur_marchande,
                cf.dividende
            FROM composition_fonds cf
            JOIN fonds f ON cf.id_fonds = f.id
            JOIN titre t ON cf.id_titre = t.id
            JOIN secteur s ON t.id_secteur = s.id
        """)
        df_compositions = pd.read_sql(query, conn)
    
    affiche_dataframe(
        df_compositions,
        title="Compositions des Fonds",
        geometry="1400x600"
    )

if __name__ == "__main__":
    print("Démonstration des outils de visualisation")
    print("-" * 50)
    
    while True:
        print("\nQue souhaitez-vous faire ?")
        print("1. Ouvrir SQLite Viewer")
        print("2. Visualiser les données avec le DataFrameViewer")
        print("3. Quitter")
        
        choix = input("\nVotre choix (1-3) : ")
        
        if choix == "1":
            demo_sqlite_viewer()
        elif choix == "2":
            demo_dataframe_viewer()
        elif choix == "3":
            print("\nAu revoir !")
            break
        else:
            print("\nChoix invalide. Veuillez réessayer.") 
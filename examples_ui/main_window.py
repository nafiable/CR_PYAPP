"""
Interface graphique principale pour l'affichage des données financières.
"""

import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from pandastable import Table
import pandas as pd
from database.connexionsqlLiter import SQLiteConnection
from sqlalchemy import text

class MainWindow:
    """Fenêtre principale de l'application."""
    
    def __init__(self):
        """Initialise la fenêtre principale."""
        self.root = ThemedTk(theme="arc")  # Thème moderne
        self.root.title("Visualisation des Données Financières")
        self.root.geometry("1200x800")
        
        # Configuration de la grille principale
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Création du notebook pour les onglets
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        
        # Création des onglets
        self.create_gestionnaires_tab()
        self.create_fonds_tab()
        self.create_composition_tab()
    
    def create_gestionnaires_tab(self):
        """Crée l'onglet des gestionnaires."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Gestionnaires')
        
        # Création de la table
        pt = Table(frame)
        pt.show()
        
        # Chargement des données
        db = SQLiteConnection()
        with db.engine.connect() as conn:
            query = text("""
                SELECT g.code, g.nom, g.tel, g.contact_principal, g.email,
                       COUNT(gf.id_fonds) as nombre_fonds
                FROM gestionnaire g
                LEFT JOIN gestionnaire_fonds gf ON g.id = gf.id_gestionnaire
                GROUP BY g.id, g.code, g.nom, g.tel, g.contact_principal, g.email
            """)
            df = pd.read_sql(query, conn)
        
        pt.model.df = df
        pt.redraw()
    
    def create_fonds_tab(self):
        """Crée l'onglet des fonds."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Fonds')
        
        # Création de la table
        pt = Table(frame)
        pt.show()
        
        # Chargement des données
        db = SQLiteConnection()
        with db.engine.connect() as conn:
            query = text("""
                SELECT f.code, f.nom, f.type_fonds,
                       COUNT(DISTINCT gf.id_gestionnaire) as nombre_gestionnaires,
                       COUNT(DISTINCT fi.id_indice) as nombre_indices
                FROM fonds f
                LEFT JOIN gestionnaire_fonds gf ON f.id = gf.id_fonds
                LEFT JOIN fonds_indice fi ON f.id = fi.id_fonds
                GROUP BY f.id, f.code, f.nom, f.type_fonds
            """)
            df = pd.read_sql(query, conn)
        
        pt.model.df = df
        pt.redraw()
    
    def create_composition_tab(self):
        """Crée l'onglet des compositions."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Compositions')
        
        # Création de la table
        pt = Table(frame)
        pt.show()
        
        # Chargement des données
        db = SQLiteConnection()
        with db.engine.connect() as conn:
            query = text("""
                SELECT cf.date,
                       f.code as code_fonds,
                       f.nom as nom_fonds,
                       t.code as code_titre,
                       t.nom as nom_titre,
                       cf.quantite,
                       cf.prix,
                       cf.valeur_marchande,
                       cf.dividende
                FROM composition_fonds cf
                JOIN fonds f ON cf.id_fonds = f.id
                JOIN titre t ON cf.id_titre = t.id
            """)
            df = pd.read_sql(query, conn)
        
        pt.model.df = df
        pt.redraw()
    
    def run(self):
        """Lance l'application."""
        self.root.mainloop()

if __name__ == "__main__":
    app = MainWindow()
    app.run() 
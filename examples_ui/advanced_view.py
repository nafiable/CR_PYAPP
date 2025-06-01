"""
Interface graphique avancée avec filtres et graphiques.
"""

import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from pandastable import Table
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from database.connexionsqlLiter import SQLiteConnection
from sqlalchemy import text

class AdvancedWindow:
    """Fenêtre avec fonctionnalités avancées."""
    
    def __init__(self):
        """Initialise la fenêtre avancée."""
        self.root = ThemedTk(theme="arc")
        self.root.title("Analyse Avancée des Données")
        self.root.geometry("1400x900")
        
        # Configuration de la grille principale
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
        # Création du panneau de filtres
        self.create_filter_panel()
        
        # Création du notebook pour les vues
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        
        # Création des onglets
        self.create_portfolio_analysis_tab()
        self.create_performance_tab()
    
    def create_filter_panel(self):
        """Crée le panneau de filtres."""
        filter_frame = ttk.LabelFrame(self.root, text="Filtres")
        filter_frame.grid(row=0, column=0, sticky='ns', padx=5, pady=5)
        
        # Filtre par date
        ttk.Label(filter_frame, text="Date:").pack(pady=5)
        self.date_var = tk.StringVar()
        dates = self.get_available_dates()
        date_combo = ttk.Combobox(filter_frame, textvariable=self.date_var, values=dates)
        date_combo.pack(pady=5, padx=5)
        
        # Filtre par gestionnaire
        ttk.Label(filter_frame, text="Gestionnaire:").pack(pady=5)
        self.gestionnaire_var = tk.StringVar()
        gestionnaires = self.get_gestionnaires()
        gest_combo = ttk.Combobox(filter_frame, textvariable=self.gestionnaire_var, values=gestionnaires)
        gest_combo.pack(pady=5, padx=5)
        
        # Bouton d'application des filtres
        ttk.Button(filter_frame, text="Appliquer", command=self.apply_filters).pack(pady=20)
    
    def create_portfolio_analysis_tab(self):
        """Crée l'onglet d'analyse de portefeuille."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Analyse de Portefeuille')
        
        # Division en deux parties
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        
        # Graphique de répartition
        fig = plt.Figure(figsize=(8, 4))
        self.portfolio_canvas = FigureCanvasTkAgg(fig, frame)
        self.portfolio_canvas.get_tk_widget().grid(row=0, column=0, sticky='ew', pady=5)
        
        # Table des données
        self.portfolio_table = Table(frame)
        self.portfolio_table.show()
        self.portfolio_table.grid(row=1, column=0, sticky='nsew')
        
        # Chargement initial des données
        self.update_portfolio_view()
    
    def create_performance_tab(self):
        """Crée l'onglet de performance."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Performance')
        
        # Graphique de performance
        fig = plt.Figure(figsize=(8, 6))
        self.performance_canvas = FigureCanvasTkAgg(fig, frame)
        self.performance_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Chargement initial des données
        self.update_performance_view()
    
    def get_available_dates(self):
        """Récupère les dates disponibles."""
        db = SQLiteConnection()
        with db.engine.connect() as conn:
            query = text("SELECT DISTINCT date FROM composition_fonds ORDER BY date")
            return [str(date[0]) for date in conn.execute(query)]
    
    def get_gestionnaires(self):
        """Récupère la liste des gestionnaires."""
        db = SQLiteConnection()
        with db.engine.connect() as conn:
            query = text("SELECT code FROM gestionnaire ORDER BY code")
            return [code[0] for code in conn.execute(query)]
    
    def apply_filters(self):
        """Applique les filtres sélectionnés."""
        self.update_portfolio_view()
        self.update_performance_view()
    
    def update_portfolio_view(self):
        """Met à jour la vue du portefeuille."""
        db = SQLiteConnection()
        with db.engine.connect() as conn:
            # Construction de la requête avec filtres
            query = text("""
                SELECT 
                    t.code as code_titre,
                    t.nom as nom_titre,
                    s.nom as secteur,
                    cf.quantite,
                    cf.prix,
                    cf.valeur_marchande
                FROM composition_fonds cf
                JOIN titre t ON cf.id_titre = t.id
                JOIN secteur s ON t.id_secteur = s.id
                JOIN fonds f ON cf.id_fonds = f.id
                JOIN gestionnaire_fonds gf ON f.id = gf.id_fonds
                JOIN gestionnaire g ON gf.id_gestionnaire = g.id
                WHERE 1=1
            """)
            
            df = pd.read_sql(query, conn)
            
            # Mise à jour du graphique
            fig = self.portfolio_canvas.figure
            fig.clear()
            ax = fig.add_subplot(111)
            
            # Graphique en secteurs
            secteur_data = df.groupby('secteur')['valeur_marchande'].sum()
            ax.pie(secteur_data, labels=secteur_data.index, autopct='%1.1f%%')
            ax.set_title('Répartition par Secteur')
            
            self.portfolio_canvas.draw()
            
            # Mise à jour de la table
            self.portfolio_table.model.df = df
            self.portfolio_table.redraw()
    
    def update_performance_view(self):
        """Met à jour la vue des performances."""
        db = SQLiteConnection()
        with db.engine.connect() as conn:
            query = text("""
                SELECT 
                    cf.date,
                    SUM(cf.valeur_marchande) as valeur_totale
                FROM composition_fonds cf
                GROUP BY cf.date
                ORDER BY cf.date
            """)
            
            df = pd.read_sql(query, conn)
            
            # Mise à jour du graphique
            fig = self.performance_canvas.figure
            fig.clear()
            ax = fig.add_subplot(111)
            
            ax.plot(df['date'], df['valeur_totale'], marker='o')
            ax.set_title('Évolution de la Valeur du Portefeuille')
            ax.set_xlabel('Date')
            ax.set_ylabel('Valeur Totale')
            fig.autofmt_xdate()  # Rotation des dates
            
            self.performance_canvas.draw()
    
    def run(self):
        """Lance l'application."""
        self.root.mainloop()

if __name__ == "__main__":
    app = AdvancedWindow()
    app.run() 
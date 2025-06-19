"""
Interface graphique avancée avec filtres et graphiques.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
from pandastable import Table
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from database.connexionsqlLiter import SQLiteConnection
from sqlalchemy import text
import os
from pathlib import Path

DEFAULT_DB_FILES = ["ma_base.db", "database.db"]

class AdvancedWindow:
    """Fenêtre avec fonctionnalités avancées."""
    
    def __init__(self, db_path=None):
        self.db_path = self.find_db_path(db_path)
        self.root = ThemedTk(theme="arc")
        self.root.title("Analyse Avancée des Données")
        self.root.geometry("1400x900")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.create_filter_panel()
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        self.create_portfolio_analysis_tab()
        self.create_performance_tab()
    
    def find_db_path(self, db_path):
        if db_path and Path(db_path).exists():
            return db_path
        for f in DEFAULT_DB_FILES:
            if Path(f).exists():
                return f
        if messagebox.askyesno("Base absente", "Aucune base SQLite trouvée. Initialiser la base ?"):
            if self.init_database():
                return DEFAULT_DB_FILES[0]
        messagebox.showerror("Erreur", "Aucune base de données SQLite trouvée.")
        raise SystemExit(1)
    
    def create_filter_panel(self):
        filter_frame = ttk.LabelFrame(self.root, text="Filtres")
        filter_frame.grid(row=0, column=0, sticky='ns', padx=5, pady=5)
        ttk.Label(filter_frame, text="Date:").pack(pady=5)
        self.date_var = tk.StringVar()
        dates = self.get_available_dates()
        date_combo = ttk.Combobox(filter_frame, textvariable=self.date_var, values=dates)
        date_combo.pack(pady=5, padx=5)
        ttk.Label(filter_frame, text="Gestionnaire:").pack(pady=5)
        self.gestionnaire_var = tk.StringVar()
        gestionnaires = self.get_gestionnaires()
        gest_combo = ttk.Combobox(filter_frame, textvariable=self.gestionnaire_var, values=gestionnaires)
        gest_combo.pack(pady=5, padx=5)
        ttk.Button(filter_frame, text="Appliquer", command=self.apply_filters).pack(pady=20)
        ttk.Button(filter_frame, text="Initialiser la base", command=self.init_database_and_reload).pack(pady=5)
    
    def get_available_dates(self):
        try:
            db = SQLiteConnection(f"sqlite:///{self.db_path}")
            with db.engine.connect() as conn:
                query = text("SELECT DISTINCT date FROM composition_fonds ORDER BY date")
                return [str(date[0]) for date in conn.execute(query)]
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la récupération des dates : {str(e)}")
            return []
    
    def get_gestionnaires(self):
        try:
            db = SQLiteConnection(f"sqlite:///{self.db_path}")
            with db.engine.connect() as conn:
                query = text("SELECT code FROM gestionnaire ORDER BY code")
                return [code[0] for code in conn.execute(query)]
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la récupération des gestionnaires : {str(e)}")
            return []
    
    def apply_filters(self):
        self.update_portfolio_view()
        self.update_performance_view()
    
    def create_portfolio_analysis_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Analyse de Portefeuille')
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        fig = plt.Figure(figsize=(8, 4))
        self.portfolio_canvas = FigureCanvasTkAgg(fig, frame)
        self.portfolio_canvas.get_tk_widget().grid(row=0, column=0, sticky='ew', pady=5)
        self.portfolio_table = Table(frame)
        self.portfolio_table.show()
        self.portfolio_table.grid(row=1, column=0, sticky='nsew')
        self.update_portfolio_view()
    
    def create_performance_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Performance')
        fig = plt.Figure(figsize=(8, 6))
        self.performance_canvas = FigureCanvasTkAgg(fig, frame)
        self.performance_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.update_performance_view()
    
    def update_portfolio_view(self):
        try:
            db = SQLiteConnection(f"sqlite:///{self.db_path}")
            with db.engine.connect() as conn:
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
                """
                )
                df = pd.read_sql(query, conn)
                if df.empty:
                    if messagebox.askyesno("Aucune donnée", "Aucune donnée trouvée. Peupler la base de test ?"):
                        self.populate_database()
                        self.update_portfolio_view()
                        return
                    messagebox.showwarning("Aucune donnée", "Aucune donnée trouvée dans la base.")
                    return
                fig = self.portfolio_canvas.figure
                fig.clear()
                ax = fig.add_subplot(111)
                secteur_data = df.groupby('secteur')['valeur_marchande'].sum()
                ax.pie(secteur_data, labels=secteur_data.index, autopct='%1.1f%%')
                ax.set_title('Répartition par Secteur')
                self.portfolio_canvas.draw()
                self.portfolio_table.model.df = df
                self.portfolio_table.redraw()
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'affichage du portefeuille : {str(e)}")
    
    def update_performance_view(self):
        try:
            db = SQLiteConnection(f"sqlite:///{self.db_path}")
            with db.engine.connect() as conn:
                query = text("""
                    SELECT 
                        cf.date,
                        SUM(cf.valeur_marchande) as valeur_totale
                    FROM composition_fonds cf
                    GROUP BY cf.date
                    ORDER BY cf.date
                """
                )
                df = pd.read_sql(query, conn)
                if df.empty:
                    return
                fig = self.performance_canvas.figure
                fig.clear()
                ax = fig.add_subplot(111)
                ax.plot(df['date'], df['valeur_totale'], marker='o')
                ax.set_title('Évolution de la Valeur du Portefeuille')
                ax.set_xlabel('Date')
                ax.set_ylabel('Valeur Totale')
                fig.autofmt_xdate()
                self.performance_canvas.draw()
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'affichage de la performance : {str(e)}")
    
    def init_database(self):
        try:
            SQLiteConnection().init_database()
            messagebox.showinfo("Initialisation", "Base de données initialisée avec succès.")
            return True
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'initialisation de la base: {str(e)}")
            return False
    
    def init_database_and_reload(self):
        if self.init_database():
            self.__init__(self.db_path)
    
    def populate_database(self):
        try:
            import subprocess, sys
            subprocess.run([sys.executable, "examples/populate_database.py"], check=True)
            messagebox.showinfo("Peuplement", "Base de test peuplée avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du peuplement: {str(e)}")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AdvancedWindow()
    app.run() 
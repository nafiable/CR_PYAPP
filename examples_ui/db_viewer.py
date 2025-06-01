"""
Outil de visualisation de la base de données SQLite.
"""

import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from pandastable import Table
import pandas as pd
import sqlite3

class DBViewer:
    """Visualiseur de base de données SQLite."""
    
    def __init__(self):
        """Initialise la fenêtre de visualisation."""
        self.root = ThemedTk(theme="arc")
        self.root.title("Visualiseur de Base de Données SQLite")
        self.root.geometry("1200x800")
        
        # Configuration de la grille principale
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
        # Création du panneau de tables
        self.create_tables_panel()
        
        # Création de la zone d'affichage
        self.create_display_area()
        
        # Chargement initial des tables
        self.load_tables()
    
    def create_tables_panel(self):
        """Crée le panneau de sélection des tables."""
        tables_frame = ttk.LabelFrame(self.root, text="Tables")
        tables_frame.grid(row=0, column=0, sticky='ns', padx=5, pady=5)
        
        # Liste des tables
        self.tables_list = tk.Listbox(tables_frame, width=30)
        self.tables_list.pack(pady=5, padx=5, fill=tk.Y, expand=True)
        self.tables_list.bind('<<ListboxSelect>>', self.on_table_select)
        
        # Boutons d'action
        ttk.Button(tables_frame, text="Structure", command=self.show_structure).pack(pady=5, padx=5)
        ttk.Button(tables_frame, text="Données", command=self.show_data).pack(pady=5, padx=5)
    
    def create_display_area(self):
        """Crée la zone d'affichage des données."""
        display_frame = ttk.Frame(self.root)
        display_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        
        # Configuration de la grille
        display_frame.grid_rowconfigure(1, weight=1)
        display_frame.grid_columnconfigure(0, weight=1)
        
        # Label d'information
        self.info_label = ttk.Label(display_frame, text="")
        self.info_label.grid(row=0, column=0, sticky='w', pady=5)
        
        # Table de données
        self.data_frame = ttk.Frame(display_frame)
        self.data_frame.grid(row=1, column=0, sticky='nsew')
        self.table = Table(self.data_frame)
        self.table.show()
    
    def load_tables(self):
        """Charge la liste des tables de la base de données."""
        try:
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            
            # Récupération des tables
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table'
                ORDER BY name
            """)
            
            tables = cursor.fetchall()
            self.tables_list.delete(0, tk.END)
            for table in tables:
                self.tables_list.insert(tk.END, table[0])
            
            conn.close()
        except Exception as e:
            self.info_label.config(text=f"Erreur: {str(e)}")
    
    def on_table_select(self, event):
        """Gère la sélection d'une table."""
        self.show_data()
    
    def show_structure(self):
        """Affiche la structure de la table sélectionnée."""
        if not self.tables_list.curselection():
            return
        
        table_name = self.tables_list.get(self.tables_list.curselection())
        try:
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            
            # Récupération de la structure
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            # Création du DataFrame
            df = pd.DataFrame(columns, columns=['cid', 'name', 'type', 'notnull', 'dflt_value', 'pk'])
            
            # Mise à jour de l'affichage
            self.info_label.config(text=f"Structure de la table: {table_name}")
            self.table.model.df = df
            self.table.redraw()
            
            conn.close()
        except Exception as e:
            self.info_label.config(text=f"Erreur: {str(e)}")
    
    def show_data(self):
        """Affiche les données de la table sélectionnée."""
        if not self.tables_list.curselection():
            return
        
        table_name = self.tables_list.get(self.tables_list.curselection())
        try:
            conn = sqlite3.connect("database.db")
            
            # Récupération des données
            df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
            
            # Mise à jour de l'affichage
            self.info_label.config(text=f"Données de la table: {table_name}")
            self.table.model.df = df
            self.table.redraw()
            
            conn.close()
        except Exception as e:
            self.info_label.config(text=f"Erreur: {str(e)}")
    
    def run(self):
        """Lance l'application."""
        self.root.mainloop()

if __name__ == "__main__":
    app = DBViewer()
    app.run() 
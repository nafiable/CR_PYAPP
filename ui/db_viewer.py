"""
Outil de visualisation de la base de données SQLite.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
from pandastable import Table
import pandas as pd
import sqlite3
import os
from pathlib import Path
from database.connexionsqlLiter import SQLiteConnection

DEFAULT_DB_FILES = ["ma_base.db", "database.db"]

class DBViewer:
    """Visualiseur de base de données SQLite."""
    
    def __init__(self, db_path=None):
        """Initialise la fenêtre de visualisation."""
        self.db_path = self.find_db_path(db_path)
        self.root = ThemedTk(theme="arc")
        self.root.title("Visualiseur de Base de Données SQLite")
        self.root.geometry("1200x800")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.create_tables_panel()
        self.create_display_area()
        self.load_tables()
    
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
    
    def create_tables_panel(self):
        tables_frame = ttk.LabelFrame(self.root, text="Tables")
        tables_frame.grid(row=0, column=0, sticky='ns', padx=5, pady=5)
        self.tables_list = tk.Listbox(tables_frame, width=30)
        self.tables_list.pack(pady=5, padx=5, fill=tk.Y, expand=True)
        self.tables_list.bind('<<ListboxSelect>>', self.on_table_select)
        ttk.Button(tables_frame, text="Structure", command=self.show_structure).pack(pady=5, padx=5)
        ttk.Button(tables_frame, text="Données", command=self.show_data).pack(pady=5, padx=5)
        ttk.Button(tables_frame, text="Initialiser la base", command=self.init_database_and_reload).pack(pady=5, padx=5)
    
    def create_display_area(self):
        display_frame = ttk.Frame(self.root)
        display_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        display_frame.grid_rowconfigure(1, weight=1)
        display_frame.grid_columnconfigure(0, weight=1)
        self.info_label = ttk.Label(display_frame, text="")
        self.info_label.grid(row=0, column=0, sticky='w', pady=5)
        self.data_frame = ttk.Frame(display_frame)
        self.data_frame.grid(row=1, column=0, sticky='nsew')
        self.table = Table(self.data_frame)
        self.table.show()
    
    def load_tables(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table'
                ORDER BY name
            """)
            tables = cursor.fetchall()
            self.tables_list.delete(0, tk.END)
            if not tables:
                if messagebox.askyesno("Aucune table", "Aucune table trouvée. Initialiser la base ?"):
                    if self.init_database():
                        self.load_tables()
                        return
                if messagebox.askyesno("Peuplement", "Voulez-vous peupler la base de test ?"):
                    self.populate_database()
                    self.load_tables()
                    return
                messagebox.showwarning("Aucune table", "Aucune table trouvée dans la base.")
                self.info_label.config(text="Aucune table trouvée")
                return
            for table in tables:
                self.tables_list.insert(tk.END, table[0])
            conn.close()
        except Exception as e:
            self.info_label.config(text=f"Erreur: {str(e)}")
    
    def on_table_select(self, event):
        self.show_data()
    
    def show_structure(self):
        if not self.tables_list.curselection():
            return
        table_name = self.tables_list.get(self.tables_list.curselection())
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            df = pd.DataFrame(columns, columns=['cid', 'name', 'type', 'notnull', 'dflt_value', 'pk'])
            self.info_label.config(text=f"Structure de la table: {table_name}")
            self.table.model.df = df
            self.table.redraw()
            conn.close()
        except Exception as e:
            self.info_label.config(text=f"Erreur: {str(e)}")
    
    def show_data(self):
        if not self.tables_list.curselection():
            return
        table_name = self.tables_list.get(self.tables_list.curselection())
        try:
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
            self.info_label.config(text=f"Données de la table: {table_name}")
            self.table.model.df = df
            self.table.redraw()
            conn.close()
        except Exception as e:
            self.info_label.config(text=f"Erreur: {str(e)}")
    
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
            self.load_tables()
    
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
    app = DBViewer()
    app.run() 
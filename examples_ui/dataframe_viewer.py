"""
Module pour afficher des DataFrames dans une fenêtre Tkinter séparée.
"""

import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from pandastable import Table
import pandas as pd
from typing import Optional, Union, Dict

class DataFrameViewer:
    """Classe pour afficher un DataFrame dans une fenêtre séparée."""
    
    def __init__(self, title: str = "Visualisation de DataFrame"):
        """
        Initialise la fenêtre de visualisation.
        
        Args:
            title (str): Titre de la fenêtre
        """
        self.root = None
        self.table = None
        self.title = title
    
    def setup_window(self):
        """Configure la fenêtre principale."""
        self.root = ThemedTk(theme="arc")
        self.root.title(self.title)
        self.root.geometry("1000x600")
        
        # Configuration de la grille
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Barre d'outils
        toolbar = ttk.Frame(self.root)
        toolbar.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        
        # Boutons de la barre d'outils
        ttk.Button(toolbar, text="Exporter CSV", command=self.export_csv).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Exporter Excel", command=self.export_excel).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Statistiques", command=self.show_stats).pack(side=tk.LEFT, padx=5)
        
        # Zone de données
        frame = ttk.Frame(self.root)
        frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        
        # Table
        self.table = Table(frame)
        self.table.show()
    
    def show(self, df: pd.DataFrame, options: Optional[Dict] = None):
        """
        Affiche le DataFrame dans une nouvelle fenêtre.
        
        Args:
            df (pd.DataFrame): DataFrame à afficher
            options (dict, optional): Options d'affichage
                - title: Titre personnalisé
                - theme: Thème à utiliser
                - geometry: Taille de la fenêtre (ex: "1000x600")
        """
        if options is None:
            options = {}
        
        # Configuration de la fenêtre
        if self.root is None:
            self.title = options.get('title', self.title)
            self.setup_window()
        
        if 'theme' in options:
            self.root.set_theme(options['theme'])
        
        if 'geometry' in options:
            self.root.geometry(options['geometry'])
        
        # Affichage des données
        self.table.model.df = df
        self.table.redraw()
        
        # Lancement de la boucle d'événements
        if not self.root.winfo_exists():
            self.root.mainloop()
    
    def export_csv(self):
        """Exporte les données en CSV."""
        if self.table is not None and hasattr(self.table.model, 'df'):
            try:
                filename = tk.filedialog.asksaveasfilename(
                    defaultextension=".csv",
                    filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
                )
                if filename:
                    self.table.model.df.to_csv(filename, index=False)
                    tk.messagebox.showinfo("Succès", "Données exportées avec succès!")
            except Exception as e:
                tk.messagebox.showerror("Erreur", f"Erreur lors de l'export: {str(e)}")
    
    def export_excel(self):
        """Exporte les données en Excel."""
        if self.table is not None and hasattr(self.table.model, 'df'):
            try:
                filename = tk.filedialog.asksaveasfilename(
                    defaultextension=".xlsx",
                    filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
                )
                if filename:
                    self.table.model.df.to_excel(filename, index=False)
                    tk.messagebox.showinfo("Succès", "Données exportées avec succès!")
            except Exception as e:
                tk.messagebox.showerror("Erreur", f"Erreur lors de l'export: {str(e)}")
    
    def show_stats(self):
        """Affiche les statistiques du DataFrame."""
        if self.table is not None and hasattr(self.table.model, 'df'):
            df = self.table.model.df
            stats_window = tk.Toplevel(self.root)
            stats_window.title("Statistiques")
            stats_window.geometry("800x600")
            
            # Création des statistiques
            stats_text = ttk.Text(stats_window)
            stats_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            # Informations générales
            stats_text.insert(tk.END, "INFORMATIONS GÉNÉRALES\n")
            stats_text.insert(tk.END, "-" * 50 + "\n")
            stats_text.insert(tk.END, f"Nombre de lignes: {len(df)}\n")
            stats_text.insert(tk.END, f"Nombre de colonnes: {len(df.columns)}\n\n")
            
            # Types des colonnes
            stats_text.insert(tk.END, "TYPES DES COLONNES\n")
            stats_text.insert(tk.END, "-" * 50 + "\n")
            for col in df.columns:
                stats_text.insert(tk.END, f"{col}: {df[col].dtype}\n")
            stats_text.insert(tk.END, "\n")
            
            # Statistiques descriptives
            stats_text.insert(tk.END, "STATISTIQUES DESCRIPTIVES\n")
            stats_text.insert(tk.END, "-" * 50 + "\n")
            stats_text.insert(tk.END, df.describe().to_string())
            
            stats_text.config(state='disabled')

def affiche_dataframe(df: pd.DataFrame, **options):
    """
    Fonction utilitaire pour afficher rapidement un DataFrame.
    
    Args:
        df (pd.DataFrame): DataFrame à afficher
        **options: Options d'affichage (voir DataFrameViewer.show())
    """
    viewer = DataFrameViewer()
    viewer.show(df, options)

# Exemple d'utilisation
if __name__ == "__main__":
    # Création d'un DataFrame de test
    df_test = pd.DataFrame({
        'A': range(1, 11),
        'B': [f"Val_{i}" for i in range(1, 11)],
        'C': [i * 2.5 for i in range(1, 11)]
    })
    
    # Affichage du DataFrame
    affiche_dataframe(df_test, title="Test DataFrame") 
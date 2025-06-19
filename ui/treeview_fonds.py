"""
Interface TreeView pour afficher la hiérarchie Gestionnaires > Fonds
avec menu contextuel sur double-clic pour modifier, supprimer, afficher composition.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
import sqlite3
import pandas as pd
from pandastable import Table
from pathlib import Path
import logging
import os
from database.connexionsqlLiter import SQLiteConnection

logger = logging.getLogger(__name__)

DEFAULT_DB_FILES = ["ma_base.db", "database.db"]

class FondsTreeViewApp:
    """Application TreeView pour la gestion des fonds et gestionnaires."""
    
    def __init__(self, db_path=None):
        """Initialise l'application TreeView."""
        self.db_path = self.find_db_path(db_path)
        self.root = ThemedTk(theme="arc")
        self.root.title("Gestionnaires et Fonds - TreeView")
        self.root.geometry("1400x900")
        
        # Configuration de la grille principale
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Création de l'interface
        self.create_toolbar()
        self.create_treeview()
        self.create_status_bar()
        self.create_details_panel()
        
        # Chargement initial des données
        self.load_data()
        
        # Binding des événements
        self.tree.bind("<Double-1>", self.on_double_click)
        self.tree.bind("<Button-3>", self.on_right_click)
    
    def find_db_path(self, db_path):
        """Trouve le chemin de la base de données existante ou propose de l'initialiser."""
        if db_path and Path(db_path).exists():
            return db_path
        for f in DEFAULT_DB_FILES:
            if Path(f).exists():
                return f
        # Si aucune base n'existe, propose de l'initialiser
        if messagebox.askyesno("Base absente", "Aucune base SQLite trouvée. Initialiser la base ?"):
            if self.init_database():
                return DEFAULT_DB_FILES[0]
        messagebox.showerror("Erreur", "Aucune base de données SQLite trouvée.")
        raise SystemExit(1)

    def create_toolbar(self):
        """Crée la barre d'outils."""
        toolbar = ttk.Frame(self.root)
        toolbar.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        
        # Boutons d'action
        ttk.Button(toolbar, text="Actualiser", command=self.load_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Initialiser la base", command=self.init_database_and_reload).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Ajouter Gestionnaire", command=self.add_gestionnaire).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Ajouter Fonds", command=self.add_fonds).pack(side=tk.LEFT, padx=5)
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        ttk.Button(toolbar, text="Exporter CSV", command=self.export_to_csv).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Exporter Excel", command=self.export_to_excel).pack(side=tk.LEFT, padx=5)
    
    def create_treeview(self):
        """Crée la TreeView principale."""
        tree_frame = ttk.Frame(self.root)
        tree_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        self.tree = ttk.Treeview(tree_frame, columns=("id", "type", "details"), show="tree headings")
        self.tree.heading("#0", text="Gestionnaires / Fonds", anchor="w")
        self.tree.heading("id", text="ID")
        self.tree.heading("type", text="Type")
        self.tree.heading("details", text="Détails")
        self.tree.column("#0", width=300, minwidth=200)
        self.tree.column("id", width=80, minwidth=60)
        self.tree.column("type", width=100, minwidth=80)
        self.tree.column("details", width=200, minwidth=150)
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
    
    def create_status_bar(self):
        self.status_bar = ttk.Label(self.root, text="Prêt", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=2, column=0, sticky='ew', padx=5, pady=2)
    
    def create_details_panel(self):
        details_frame = ttk.LabelFrame(self.root, text="Détails")
        details_frame.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)
        details_frame.grid_rowconfigure(0, weight=1)
        details_frame.grid_columnconfigure(0, weight=1)
        self.details_text = tk.Text(details_frame, wrap=tk.WORD, width=40)
        details_scrollbar = ttk.Scrollbar(details_frame, orient="vertical", command=self.details_text.yview)
        self.details_text.configure(yscrollcommand=details_scrollbar.set)
        self.details_text.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        details_scrollbar.grid(row=0, column=1, sticky='ns')
    
    def load_data(self):
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            # Vérifie la présence de la table gestionnaire
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='gestionnaire'")
            if not cursor.fetchone():
                if messagebox.askyesno("Table absente", "La table 'gestionnaire' est absente. Initialiser la base ?"):
                    if self.init_database():
                        self.load_data()
                        return
                messagebox.showerror("Erreur", "La table 'gestionnaire' est absente dans la base.")
                self.status_bar.config(text="Erreur : table gestionnaire absente")
                return
            # Récupération des gestionnaires
            cursor.execute("SELECT id, code, nom, email FROM gestionnaire ORDER BY nom")
            gestionnaires = cursor.fetchall()
            if not gestionnaires:
                if messagebox.askyesno("Aucun gestionnaire", "Aucun gestionnaire trouvé. Peupler la base de test ?"):
                    self.populate_database()
                    self.load_data()
                    return
                messagebox.showwarning("Aucun gestionnaire", "Aucun gestionnaire trouvé dans la base.")
                self.status_bar.config(text="Aucun gestionnaire trouvé")
                return
            for gest_id, gest_code, gest_nom, gest_email in gestionnaires:
                gest_item = self.tree.insert("", "end", 
                    text=f"📊 {gest_nom} ({gest_code})",
                    values=(gest_id, "Gestionnaire", f"Email: {gest_email}"),
                    tags=("gestionnaire",),
                    open=True
                )
                cursor.execute("""
                    SELECT f.id, f.code, f.nom, f.type_fonds
                    FROM fonds f
                    JOIN gestionnaire_fonds gf ON f.id = gf.id_fonds
                    WHERE gf.id_gestionnaire = ?
                    ORDER BY f.nom
                """, (gest_id,))
                fonds = cursor.fetchall()
                for fonds_id, fonds_code, fonds_nom, fonds_type in fonds:
                    icon = "💰" if fonds_type == "simple" else "📈"
                    self.tree.insert(gest_item, "end",
                        text=f"{icon} {fonds_nom} ({fonds_code})",
                        values=(fonds_id, "Fonds", f"Type: {fonds_type}"),
                        tags=("fonds",)
                    )
            conn.close()
            self.status_bar.config(text=f"Données chargées: {len(gestionnaires)} gestionnaires")
        except Exception as e:
            logger.error(f"Erreur lors du chargement des données: {str(e)}")
            messagebox.showerror("Erreur", f"Impossible de charger les données: {str(e)}")
            self.status_bar.config(text="Erreur de chargement")
    
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
            self.load_data()
    
    def populate_database(self):
        try:
            import subprocess, sys
            subprocess.run([sys.executable, "examples/populate_database.py"], check=True)
            messagebox.showinfo("Peuplement", "Base de test peuplée avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du peuplement: {str(e)}")
    
    def on_double_click(self, event):
        """Gère le double-clic sur un élément."""
        item = self.tree.selection()[0]
        item_type = self.tree.item(item, "tags")[0] if self.tree.item(item, "tags") else ""
        
        if item_type == "fonds":
            fonds_id = self.tree.item(item, "values")[0]
            fonds_nom = self.tree.item(item, "text").split(" ", 1)[1]  # Enlever l'icône
            self.show_fonds_options(fonds_id, fonds_nom)
        elif item_type == "gestionnaire":
            gest_id = self.tree.item(item, "values")[0]
            gest_nom = self.tree.item(item, "text").split(" ", 1)[1]  # Enlever l'icône
            self.show_gestionnaire_details(gest_id, gest_nom)
    
    def on_right_click(self, event):
        """Gère le clic droit pour le menu contextuel."""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            item_type = self.tree.item(item, "tags")[0] if self.tree.item(item, "tags") else ""
            
            if item_type == "fonds":
                self.show_context_menu(event, "fonds", item)
            elif item_type == "gestionnaire":
                self.show_context_menu(event, "gestionnaire", item)
    
    def show_context_menu(self, event, item_type, item):
        """Affiche le menu contextuel."""
        menu = tk.Menu(self.root, tearoff=0)
        
        if item_type == "fonds":
            menu.add_command(label="Modifier", command=lambda: self.modify_fonds(item))
            menu.add_command(label="Supprimer", command=lambda: self.delete_fonds(item))
            menu.add_separator()
            menu.add_command(label="Afficher composition", command=lambda: self.show_composition(item))
            menu.add_command(label="Exporter composition", command=lambda: self.export_composition(item))
        elif item_type == "gestionnaire":
            menu.add_command(label="Modifier", command=lambda: self.modify_gestionnaire(item))
            menu.add_command(label="Supprimer", command=lambda: self.delete_gestionnaire(item))
            menu.add_separator()
            menu.add_command(label="Ajouter fonds", command=lambda: self.add_fonds_to_gestionnaire(item))
            menu.add_command(label="Voir tous les fonds", command=lambda: self.show_all_fonds(item))
        
        menu.tk_popup(event.x_root, event.y_root)
    
    def show_fonds_options(self, fonds_id, fonds_nom):
        """Affiche les options pour un fonds."""
        options_window = tk.Toplevel(self.root)
        options_window.title(f"Options - {fonds_nom}")
        options_window.geometry("400x300")
        options_window.transient(self.root)
        options_window.grab_set()
        
        # Frame principal
        main_frame = ttk.Frame(options_window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titre
        ttk.Label(main_frame, text=f"Fonds: {fonds_nom}", font=("Arial", 12, "bold")).pack(pady=10)
        ttk.Label(main_frame, text=f"ID: {fonds_id}").pack()
        
        # Boutons d'action
        ttk.Button(main_frame, text="📝 Modifier le fonds", 
                  command=lambda: self.modify_fonds(fonds_id)).pack(fill=tk.X, pady=5)
        ttk.Button(main_frame, text="🗑️ Supprimer le fonds", 
                  command=lambda: self.delete_fonds(fonds_id)).pack(fill=tk.X, pady=5)
        ttk.Button(main_frame, text="📊 Afficher composition", 
                  command=lambda: self.show_composition(fonds_id)).pack(fill=tk.X, pady=5)
        ttk.Button(main_frame, text="📈 Voir performance", 
                  command=lambda: self.show_performance(fonds_id)).pack(fill=tk.X, pady=5)
        ttk.Button(main_frame, text="💾 Exporter composition", 
                  command=lambda: self.export_composition(fonds_id)).pack(fill=tk.X, pady=5)
    
    def modify_fonds(self, fonds_id):
        """Modifie un fonds."""
        messagebox.showinfo("Modifier", f"Modification du fonds {fonds_id} (à implémenter)")
    
    def delete_fonds(self, fonds_id):
        """Supprime un fonds."""
        if messagebox.askyesno("Confirmer", "Êtes-vous sûr de vouloir supprimer ce fonds ?"):
            messagebox.showinfo("Supprimer", f"Suppression du fonds {fonds_id} (à implémenter)")
    
    def show_composition(self, fonds_id):
        """Affiche la composition d'un fonds."""
        try:
            conn = sqlite3.connect(self.db_path)
            query = """
                SELECT t.code, t.nom, cf.quantite, cf.prix, cf.valeur_marchande
                FROM composition_fonds cf
                JOIN titre t ON cf.id_titre = t.id
                WHERE cf.id_fonds = ?
                ORDER BY cf.valeur_marchande DESC
            """
            df = pd.read_sql_query(query, conn, params=(fonds_id,))
            conn.close()
            
            if not df.empty:
                self.show_dataframe_window(df, f"Composition du fonds {fonds_id}")
            else:
                messagebox.showinfo("Composition", "Aucune composition trouvée pour ce fonds")
                
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'afficher la composition: {str(e)}")
    
    def show_performance(self, fonds_id):
        """Affiche la performance d'un fonds."""
        messagebox.showinfo("Performance", f"Affichage de la performance du fonds {fonds_id} (à implémenter)")
    
    def export_composition(self, fonds_id):
        """Exporte la composition d'un fonds."""
        messagebox.showinfo("Export", f"Export de la composition du fonds {fonds_id} (à implémenter)")
    
    def show_gestionnaire_details(self, gest_id, gest_nom):
        """Affiche les détails d'un gestionnaire."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Récupération des détails du gestionnaire
            cursor.execute("""
                SELECT code, nom, tel, email, contact_principal
                FROM gestionnaire
                WHERE id = ?
            """, (gest_id,))
            gest_data = cursor.fetchone()
            
            # Récupération des fonds gérés
            cursor.execute("""
                SELECT f.code, f.nom, f.type_fonds
                FROM fonds f
                JOIN gestionnaire_fonds gf ON f.id = gf.id_fonds
                WHERE gf.id_gestionnaire = ?
                ORDER BY f.nom
            """, (gest_id,))
            fonds_data = cursor.fetchall()
            
            conn.close()
            
            # Affichage dans le panneau de détails
            self.details_text.delete(1.0, tk.END)
            self.details_text.insert(tk.END, f"Gestionnaire: {gest_nom}\n")
            self.details_text.insert(tk.END, f"Code: {gest_data[0]}\n")
            self.details_text.insert(tk.END, f"Téléphone: {gest_data[2]}\n")
            self.details_text.insert(tk.END, f"Email: {gest_data[3]}\n")
            self.details_text.insert(tk.END, f"Contact: {gest_data[4]}\n\n")
            self.details_text.insert(tk.END, f"Fonds gérés ({len(fonds_data)}):\n")
            
            for fonds_code, fonds_nom, fonds_type in fonds_data:
                self.details_text.insert(tk.END, f"• {fonds_nom} ({fonds_code}) - {fonds_type}\n")
                
        except Exception as e:
            self.details_text.delete(1.0, tk.END)
            self.details_text.insert(tk.END, f"Erreur: {str(e)}")
    
    def show_dataframe_window(self, df, title):
        """Affiche un DataFrame dans une nouvelle fenêtre."""
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry("800x600")
        
        frame = ttk.Frame(window)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        table = Table(frame, dataframe=df, showtoolbar=True, showstatusbar=True)
        table.show()
    
    def add_gestionnaire(self):
        """Ajoute un nouveau gestionnaire."""
        messagebox.showinfo("Ajouter", "Ajout d'un gestionnaire (à implémenter)")
    
    def add_fonds(self):
        """Ajoute un nouveau fonds."""
        messagebox.showinfo("Ajouter", "Ajout d'un fonds (à implémenter)")
    
    def add_fonds_to_gestionnaire(self, gest_item):
        """Ajoute un fonds à un gestionnaire."""
        gest_id = self.tree.item(gest_item, "values")[0]
        messagebox.showinfo("Ajouter", f"Ajout d'un fonds au gestionnaire {gest_id} (à implémenter)")
    
    def modify_gestionnaire(self, gest_item):
        """Modifie un gestionnaire."""
        gest_id = self.tree.item(gest_item, "values")[0]
        messagebox.showinfo("Modifier", f"Modification du gestionnaire {gest_id} (à implémenter)")
    
    def delete_gestionnaire(self, gest_item):
        """Supprime un gestionnaire."""
        gest_id = self.tree.item(gest_item, "values")[0]
        if messagebox.askyesno("Confirmer", "Êtes-vous sûr de vouloir supprimer ce gestionnaire ?"):
            messagebox.showinfo("Supprimer", f"Suppression du gestionnaire {gest_id} (à implémenter)")
    
    def show_all_fonds(self, gest_item):
        """Affiche tous les fonds d'un gestionnaire."""
        gest_id = self.tree.item(gest_item, "values")[0]
        messagebox.showinfo("Fonds", f"Affichage de tous les fonds du gestionnaire {gest_id} (à implémenter)")
    
    def export_to_csv(self):
        """Exporte les données en CSV."""
        messagebox.showinfo("Export", "Export CSV (à implémenter)")
    
    def export_to_excel(self):
        """Exporte les données en Excel."""
        messagebox.showinfo("Export", "Export Excel (à implémenter)")
    
    def run(self):
        """Lance l'application."""
        self.root.mainloop()

if __name__ == "__main__":
    app = FondsTreeViewApp()
    app.run() 
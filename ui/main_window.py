"""
Fenêtre principale pour lancer toutes les interfaces graphiques.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
import subprocess
import sys
import os
from pathlib import Path

class MainWindow:
    """Fenêtre principale de l'application."""
    
    def __init__(self):
        """Initialise la fenêtre principale."""
        self.root = ThemedTk(theme="arc")
        self.root.title("Interface Graphique - Finance API")
        self.root.geometry("800x600")
        
        # Configuration de la grille
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Création de l'interface
        self.create_header()
        self.create_main_content()
        self.create_status_bar()
    
    def create_header(self):
        """Crée l'en-tête de l'application."""
        header_frame = ttk.Frame(self.root)
        header_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)
        
        # Titre
        title_label = ttk.Label(header_frame, text="Interface Graphique - Finance API", 
                               font=("Arial", 16, "bold"))
        title_label.pack()
        
        # Sous-titre
        subtitle_label = ttk.Label(header_frame, text="Sélectionnez une interface à lancer", 
                                  font=("Arial", 10))
        subtitle_label.pack(pady=5)
    
    def create_main_content(self):
        """Crée le contenu principal avec les boutons d'interface."""
        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=1, column=0, sticky='nsew', padx=20, pady=20)
        
        # Configuration de la grille
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Liste des interfaces disponibles
        interfaces = [
            {
                "name": "TreeView Fonds",
                "description": "Affichage hiérarchique Gestionnaires > Fonds avec menu contextuel",
                "icon": "🌳",
                "file": "treeview_fonds.py",
                "row": 0, "col": 0
            },
            {
                "name": "Visualiseur Base de Données",
                "description": "Exploration des tables et données SQLite",
                "icon": "🗄️",
                "file": "db_viewer.py",
                "row": 0, "col": 1
            },
            {
                "name": "Analyse Avancée",
                "description": "Graphiques et analyses de portefeuille",
                "icon": "📊",
                "file": "advanced_view.py",
                "row": 1, "col": 0
            },
            {
                "name": "Visualiseur DataFrame",
                "description": "Affichage de DataFrames avec pandas",
                "icon": "📋",
                "file": "dataframe_viewer.py",
                "row": 1, "col": 1
            },
            {
                "name": "Démo Viewers",
                "description": "Démonstrations des différents viewers",
                "icon": "🎬",
                "file": "demo_viewers.py",
                "row": 2, "col": 0
            },
            {
                "name": "Exemple d'Utilisation",
                "description": "Exemples d'utilisation des interfaces",
                "icon": "📚",
                "file": "exemple_utilisation.py",
                "row": 2, "col": 1
            }
        ]
        
        # Création des boutons pour chaque interface
        for interface in interfaces:
            self.create_interface_button(main_frame, interface)
    
    def create_interface_button(self, parent, interface):
        """Crée un bouton pour une interface."""
        # Frame pour le bouton
        button_frame = ttk.LabelFrame(parent, text=f"{interface['icon']} {interface['name']}")
        button_frame.grid(row=interface['row'], column=interface['col'], 
                         sticky='nsew', padx=10, pady=10)
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_rowconfigure(1, weight=1)
        
        # Description
        desc_label = ttk.Label(button_frame, text=interface['description'], 
                              wraplength=300, justify=tk.CENTER)
        desc_label.grid(row=0, column=0, padx=10, pady=5)
        
        # Bouton de lancement
        launch_button = ttk.Button(button_frame, text="Lancer", 
                                  command=lambda: self.launch_interface(interface))
        launch_button.grid(row=1, column=0, padx=10, pady=10)
        
        # Bouton d'aide
        help_button = ttk.Button(button_frame, text="Aide", 
                                command=lambda: self.show_help(interface))
        help_button.grid(row=2, column=0, padx=10, pady=5)
    
    def launch_interface(self, interface):
        """Lance une interface spécifique."""
        try:
            # Chemin vers le fichier d'interface
            ui_dir = Path(__file__).parent
            interface_path = ui_dir / interface['file']
            
            if not interface_path.exists():
                messagebox.showerror("Erreur", f"Fichier {interface['file']} non trouvé")
                return
            
            # Lancement de l'interface
            if interface['file'] == 'treeview_fonds.py':
                # Import direct pour TreeView
                from ui.treeview_fonds import FondsTreeViewApp
                app = FondsTreeViewApp()
                app.run()
            elif interface['file'] == 'db_viewer.py':
                # Import direct pour DB Viewer
                from ui.db_viewer import DBViewer
                app = DBViewer()
                app.run()
            else:
                # Lancement via subprocess pour les autres
                subprocess.Popen([sys.executable, str(interface_path)])
            
            self.status_bar.config(text=f"Interface {interface['name']} lancée")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lancer {interface['name']}: {str(e)}")
            self.status_bar.config(text="Erreur de lancement")
    
    def show_help(self, interface):
        """Affiche l'aide pour une interface."""
        help_texts = {
            "TreeView Fonds": """
Interface TreeView pour la gestion des fonds et gestionnaires.

Fonctionnalités :
• Affichage hiérarchique : Gestionnaires > Fonds
• Double-clic sur un fonds : menu d'options
• Clic droit : menu contextuel
• Affichage de la composition des fonds
• Panneau de détails pour les gestionnaires

Utilisation :
• Double-clic sur un gestionnaire : voir les détails
• Double-clic sur un fonds : options (modifier, supprimer, composition)
• Clic droit : menu contextuel avec actions supplémentaires
            """,
            "Visualiseur Base de Données": """
Outil de visualisation de la base de données SQLite.

Fonctionnalités :
• Liste des tables de la base
• Affichage de la structure des tables
• Affichage des données en tableau
• Navigation entre les tables

Utilisation :
• Sélectionnez une table dans la liste
• Cliquez sur "Structure" pour voir la définition
• Cliquez sur "Données" pour voir le contenu
            """,
            "Analyse Avancée": """
Interface d'analyse avancée avec graphiques.

Fonctionnalités :
• Graphiques de répartition par secteur
• Évolution de la valeur du portefeuille
• Filtres par date et gestionnaire
• Analyse de performance

Utilisation :
• Sélectionnez les filtres souhaités
• Visualisez les graphiques dans les onglets
• Analysez les données dans les tableaux
            """,
            "Visualiseur DataFrame": """
Affichage de DataFrames avec interface web.

Fonctionnalités :
• Affichage de DataFrames en HTML
• Résumé statistique des données
• Historique des DataFrames chargés
• Interface web responsive

Utilisation :
• Chargez un DataFrame via l'API
• Visualisez les données dans le navigateur
• Consultez les statistiques et l'historique
            """
        }
        
        help_text = help_texts.get(interface['name'], 
                                  f"Aide pour {interface['name']} (à documenter)")
        
        # Fenêtre d'aide
        help_window = tk.Toplevel(self.root)
        help_window.title(f"Aide - {interface['name']}")
        help_window.geometry("500x400")
        help_window.transient(self.root)
        
        # Zone de texte pour l'aide
        text_widget = tk.Text(help_window, wrap=tk.WORD, padx=10, pady=10)
        scrollbar = ttk.Scrollbar(help_window, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_widget.insert(tk.END, help_text)
        text_widget.config(state=tk.DISABLED)
    
    def create_status_bar(self):
        """Crée la barre de statut."""
        self.status_bar = ttk.Label(self.root, text="Prêt", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=2, column=0, sticky='ew', padx=5, pady=2)
    
    def run(self):
        """Lance l'application."""
        self.root.mainloop()

if __name__ == "__main__":
    app = MainWindow()
    app.run() 
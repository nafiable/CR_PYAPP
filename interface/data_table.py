"""
Interface de tableau de données avec édition, tri et menu contextuel.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from typing import Dict, Any, Optional, Callable
import numpy as np

class DataTable(ttk.Frame):
    """Table de données interactive."""
    
    def __init__(self, parent, df: pd.DataFrame):
        """Initialise la table de données.
        
        Args:
            parent: Widget parent
            df: DataFrame à afficher
        """
        super().__init__(parent)
        
        self.df = df
        self.sort_column = None
        self.sort_ascending = True
        
        # Configuration du style
        style = ttk.Style()
        style.configure(
            "Header.TLabel",
            font=('Helvetica', 12, 'bold'),
            padding=5,
            background='#e0e0e0'
        )
        style.configure(
            "Data.Treeview",
            font=('Helvetica', 10),
            rowheight=25
        )
        style.configure(
            "Data.Treeview.Heading",
            font=('Helvetica', 11, 'bold'),
            padding=5
        )
        
        # Création des widgets
        self._create_widgets()
        
        # Chargement des données
        self._load_data()
    
    def _create_widgets(self):
        """Crée les widgets de l'interface."""
        # Frame pour les en-têtes de colonnes
        self.header_frame = ttk.Frame(self)
        self.header_frame.pack(fill=tk.X, padx=5, pady=(5,0))
        
        # Labels d'en-tête pour chaque colonne
        self.headers = {}
        for i, col in enumerate(self.df.columns):
            header = ttk.Label(
                self.header_frame,
                text=col.upper(),
                style="Header.TLabel"
            )
            header.grid(row=0, column=i, sticky='nsew', padx=1)
            header.bind('<Button-1>', lambda e, c=col: self._sort_by_column(c))
            self.headers[col] = header
            
            # Configuration du redimensionnement
            self.header_frame.grid_columnconfigure(i, weight=1)
        
        # Frame pour la table
        table_frame = ttk.Frame(self)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Création du Treeview
        self.tree = ttk.Treeview(
            table_frame,
            columns=list(self.df.columns),
            show='headings',
            style="Data.Treeview"
        )
        
        # Configuration des colonnes
        for col in self.df.columns:
            self.tree.heading(
                col,
                text=col,
                command=lambda c=col: self._sort_by_column(c)
            )
            self.tree.column(col, width=150)
        
        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Placement des widgets
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        # Configuration du redimensionnement
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Bindings
        self.tree.bind('<Double-Button-1>', self._on_double_click)
        self.tree.bind('<Button-3>', self._show_context_menu)
        
        # Création du menu contextuel
        self._create_context_menu()
        
        # Création de l'éditeur de cellules
        self.cell_editor = CellEditor(self.tree)
    
    def _create_context_menu(self):
        """Crée le menu contextuel."""
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(
            label="Copier",
            command=self._copy_cell
        )
        self.context_menu.add_command(
            label="Coller",
            command=self._paste_cell
        )
        self.context_menu.add_separator()
        self.context_menu.add_command(
            label="Supprimer la ligne",
            command=self._delete_row
        )
    
    def _load_data(self):
        """Charge les données dans le Treeview."""
        # Supprime les anciennes données
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Ajoute les nouvelles données
        for idx, row in self.df.iterrows():
            values = [
                str(val) if not pd.isna(val) else ''
                for val in row.values
            ]
            self.tree.insert('', 'end', values=values, tags=(str(idx),))
    
    def _sort_by_column(self, column: str):
        """Trie les données par colonne.
        
        Args:
            column: Nom de la colonne
        """
        # Inverse l'ordre si on clique sur la même colonne
        if self.sort_column == column:
            self.sort_ascending = not self.sort_ascending
        else:
            self.sort_column = column
            self.sort_ascending = True
        
        # Trie le DataFrame
        self.df.sort_values(
            by=column,
            ascending=self.sort_ascending,
            inplace=True
        )
        
        # Met à jour l'affichage
        self._load_data()
        
        # Met à jour l'indicateur de tri
        for col, header in self.headers.items():
            if col == column:
                header.configure(
                    text=f"{col.upper()} {'↑' if self.sort_ascending else '↓'}"
                )
            else:
                header.configure(text=col.upper())
    
    def _on_double_click(self, event):
        """Gère le double-clic sur une cellule."""
        region = self.tree.identify_region(event.x, event.y)
        if region == "cell":
            # Récupère l'item et la colonne
            item = self.tree.identify_row(event.y)
            column = self.tree.identify_column(event.x)
            
            if not item or not column:
                return
            
            # Démarre l'édition
            self.cell_editor.start_edit(
                item,
                column,
                self._on_cell_edited
            )
    
    def _on_cell_edited(self, item: str, column: str, value: str):
        """Gère la modification d'une cellule.
        
        Args:
            item: ID de l'item
            column: Nom de la colonne
            value: Nouvelle valeur
        """
        # Récupère l'index de la ligne et le nom de la colonne
        idx = int(self.tree.item(item)['tags'][0])
        col_name = self.tree.column(column)['id']
        
        # Met à jour le DataFrame
        self.df.at[idx, col_name] = value
        
        # Met à jour l'affichage
        values = list(self.tree.item(item)['values'])
        col_idx = int(column[1]) - 1
        values[col_idx] = value
        self.tree.item(item, values=values)
    
    def _show_context_menu(self, event):
        """Affiche le menu contextuel."""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def _copy_cell(self):
        """Copie la valeur de la cellule sélectionnée."""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = selection[0]
        column = self.tree.identify_column(self.tree.winfo_pointerx() - self.tree.winfo_rootx())
        if not column:
            return
        
        col_idx = int(column[1]) - 1
        value = self.tree.item(item)['values'][col_idx]
        
        self.clipboard_clear()
        self.clipboard_append(str(value))
    
    def _paste_cell(self):
        """Colle la valeur dans la cellule sélectionnée."""
        try:
            value = self.clipboard_get()
        except tk.TclError:
            return
        
        selection = self.tree.selection()
        if not selection:
            return
        
        item = selection[0]
        column = self.tree.identify_column(self.tree.winfo_pointerx() - self.tree.winfo_rootx())
        if not column:
            return
        
        self._on_cell_edited(item, column, value)
    
    def _delete_row(self):
        """Supprime la ligne sélectionnée."""
        selection = self.tree.selection()
        if not selection:
            return
        
        if messagebox.askyesno(
            "Confirmation",
            "Voulez-vous vraiment supprimer cette ligne ?"
        ):
            item = selection[0]
            idx = int(self.tree.item(item)['tags'][0])
            
            # Supprime du DataFrame
            self.df.drop(idx, inplace=True)
            
            # Supprime de l'affichage
            self.tree.delete(item)

class CellEditor:
    """Éditeur de cellule."""
    
    def __init__(self, tree):
        """Initialise l'éditeur.
        
        Args:
            tree: TreeView parent
        """
        self.tree = tree
        self.editor = None
        self.editing = False
    
    def start_edit(self, item: str, column: str, callback: Callable):
        """Démarre l'édition d'une cellule.
        
        Args:
            item: ID de l'item
            column: ID de la colonne
            callback: Fonction à appeler lors de la validation
        """
        if self.editing:
            self.cancel_edit()
        
        # Récupère les coordonnées de la cellule
        bbox = self.tree.bbox(item, column)
        if not bbox:
            return
        
        # Récupère la valeur actuelle
        col_idx = int(column[1]) - 1
        current_value = self.tree.item(item)['values'][col_idx]
        
        # Crée le frame d'édition avec un padding de 1 pixel
        self.edit_frame = ttk.Frame(self.tree)
        self.edit_frame.place(
            x=bbox[0] - 1,
            y=bbox[1] - 1,
            width=bbox[2] - bbox[0] + 2,
            height=bbox[3] - bbox[1] + 2
        )
        
        # Crée l'entrée
        self.editor = ttk.Entry(self.edit_frame)
        self.editor.insert(0, str(current_value))
        self.editor.select_range(0, tk.END)
        
        # Configure le style
        self.editor.configure(
            foreground='red',
            font=('Helvetica', 10, 'bold')
        )
        
        # Place l'entrée pour qu'elle occupe tout l'espace disponible
        self.editor.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        # Focus et bindings
        self.editor.focus_set()
        self.editor.bind('<Return>', lambda e: self.validate_edit(item, column, callback))
        self.editor.bind('<Escape>', lambda e: self.cancel_edit())
        
        self.editing = True
    
    def validate_edit(self, item: str, column: str, callback: Callable):
        """Valide l'édition.
        
        Args:
            item: ID de l'item
            column: ID de la colonne
            callback: Fonction à appeler avec la nouvelle valeur
        """
        if not self.editing:
            return
        
        value = self.editor.get()
        callback(item, column, value)
        self.cancel_edit()
    
    def cancel_edit(self):
        """Annule l'édition."""
        if hasattr(self, 'edit_frame'):
            self.edit_frame.destroy()
        self.editor = None
        self.editing = False

def main():
    """Point d'entrée pour les tests."""
    root = tk.Tk()
    root.title("Test DataTable")
    root.geometry("800x600")
    
    # Création d'un DataFrame de test
    data = {
        'Nom': ['Alice', 'Bob', 'Charlie', 'David'],
        'Age': [25, 30, 35, 40],
        'Ville': ['Paris', 'Lyon', 'Marseille', 'Toulouse'],
        'Salaire': [45000, 50000, 55000, 60000]
    }
    df = pd.DataFrame(data)
    
    # Création de la table
    table = DataTable(root, df)
    table.pack(fill=tk.BOTH, expand=True)
    
    root.mainloop()

if __name__ == "__main__":
    main() 
"""
Interface d'exploration des fonds avec TreeView multi-colonnes.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from typing import Dict, List, Optional, Any
from PIL import Image, ImageTk
import io
import base64
from datetime import datetime
from interface.assets.icons import FUND_ICON, MANAGER_ICON, COMPOSITION_ICON, DETAIL_ICON
from interface.context_menu import ContextMenuManager, ActionButtonManager

class CellEditor:
    """Gestionnaire d'édition de cellule."""
    
    def __init__(self, tree):
        """Initialise le gestionnaire d'édition.
        
        Args:
            tree: TreeView parent
        """
        self.tree = tree
        self.editor = None
        self.editing = False
        self.current_item = None
        self.current_column = None
    
    def start_edit(self, item: str, column: str):
        """Démarre l'édition d'une cellule.
        
        Args:
            item: ID de l'item
            column: ID de la colonne
        """
        if self.editing:
            self.cancel_edit()
            
        # Récupère les coordonnées de la cellule
        bbox = self.tree.bbox(item, column)
        if not bbox:
            return
            
        # Récupère la valeur actuelle
        col_idx = int(column[1]) - 1
        current_value = self.tree.item(item)['values'][col_idx] if col_idx >= 0 else self.tree.item(item)['text']
        
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
        self.editor.insert(0, str(current_value) if current_value is not None else '')
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
        self.editor.bind('<Return>', lambda e: self.validate_edit(item, column))
        self.editor.bind('<Escape>', lambda e: self.cancel_edit())
        
        self.current_item = item
        self.current_column = column
        self.editing = True
    
    def validate_edit(self, item: str, column: str):
        """Valide l'édition.
        
        Args:
            item: ID de l'item
            column: ID de la colonne
        """
        if not self.editing:
            return
            
        value = self.editor.get()
        col_idx = int(column[1]) - 1
        
        if col_idx >= 0:
            # Mise à jour des valeurs
            values = list(self.tree.item(item)['values'])
            values[col_idx] = value
            self.tree.item(item, values=values)
        else:
            # Mise à jour du texte (colonne #0)
            self.tree.item(item, text=value)
        
        self.cancel_edit()
    
    def cancel_edit(self):
        """Annule l'édition."""
        if hasattr(self, 'edit_frame'):
            self.edit_frame.destroy()
        self.editor = None
        self.current_item = None
        self.current_column = None
        self.editing = False

class FundExplorer(tk.Tk):
    """Interface principale d'exploration des fonds."""
    
    def __init__(self):
        super().__init__()
        
        # Configuration de la fenêtre
        self.title("Explorateur de Fonds")
        self.geometry("1200x800")
        
        # Chargement des icônes
        self.icons = {
            'fund': self._load_icon_from_base64(FUND_ICON),
            'manager': self._load_icon_from_base64(MANAGER_ICON),
            'composition': self._load_icon_from_base64(COMPOSITION_ICON),
            'detail': self._load_icon_from_base64(DETAIL_ICON)
        }
        
        # Création des widgets
        self._create_widgets()
        
        # Initialisation du menu contextuel
        self._setup_context_menu()
        
        # Initialisation des boutons d'action
        self._setup_action_buttons()
        
        # Initialisation de l'éditeur de cellules
        self.cell_editor = CellEditor(self.tree)
        
        # Création du menu principal
        self._create_menu()
        
        # Chargement des données de test
        self._load_sample_data()
    
    def _load_icon_from_base64(self, b64_str: str, size: tuple = (16, 16)) -> Optional[ImageTk.PhotoImage]:
        """Charge une icône depuis une chaîne base64."""
        try:
            img_data = base64.b64decode(b64_str)
            img = Image.open(io.BytesIO(img_data))
            img = img.resize(size)
            return ImageTk.PhotoImage(img)
        except:
            return None
    
    def _create_widgets(self):
        """Crée les widgets de l'interface."""
        # Frame principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Style personnalisé pour le TreeView
        style = ttk.Style()
        style.configure(
            "Custom.Treeview",
            background="#ffffff",
            foreground="#333333",
            fieldbackground="#ffffff",
            rowheight=25
        )
        style.configure(
            "Custom.Treeview.Heading",
            font=('Helvetica', 10, 'bold'),
            padding=5
        )
        
        # Création du TreeView
        columns = (
            'type', 'value', 'currency', 'last_update', 'actions'
        )
        self.tree = ttk.Treeview(
            main_frame,
            columns=columns,
            style="Custom.Treeview"
        )
        
        # Configuration des colonnes
        self.tree.heading('#0', text='Nom')  # Colonne de l'arbre
        self.tree.heading('type', text='Type')
        self.tree.heading('value', text='Valeur')
        self.tree.heading('currency', text='Devise')
        self.tree.heading('last_update', text='Dernière mise à jour')
        self.tree.heading('actions', text='Actions')
        
        self.tree.column('#0', width=300)  # Colonne de l'arbre
        self.tree.column('type', width=150)
        self.tree.column('value', width=150, anchor='e')
        self.tree.column('currency', width=100, anchor='center')
        self.tree.column('last_update', width=200)
        self.tree.column('actions', width=150)
        
        # Ajout de la scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Placement des widgets
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Frame pour les détails
        self.detail_frame = ttk.LabelFrame(self, text="Détails", padding=10)
        self.detail_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Labels pour les détails
        self.detail_labels = {}
        for i, label in enumerate([
            'Nom complet:', 'Type:', 'Valeur:', 'Devise:',
            'Date de création:', 'Dernière mise à jour:', 'Description:'
        ]):
            lbl = ttk.Label(self.detail_frame, text=label, font=('Helvetica', 10, 'bold'))
            lbl.grid(row=i, column=0, sticky='w', padx=5, pady=2)
            
            value_lbl = ttk.Label(self.detail_frame, text='', font=('Helvetica', 10))
            value_lbl.grid(row=i, column=1, sticky='w', padx=5, pady=2)
            self.detail_labels[label] = value_lbl
        
        # Binding des événements
        self.tree.bind('<<TreeviewSelect>>', self._on_item_selected)
        self.tree.bind('<Double-Button-1>', self._on_double_click)  # Double-clic pour édition
        self.tree.bind('<Button-1>', self._on_click)  # Clic simple pour les actions
        self.tree.bind('<Button-3>', self._on_right_click)  # Clic droit pour le menu contextuel
    
    def _setup_context_menu(self):
        """Configure le menu contextuel."""
        self.context_menu = ContextMenuManager(self)
        
        # Ajout des commandes personnalisées
        self.context_menu.add_command(
            "Rafraîchir",
            lambda data: self._refresh_item(data),
            lambda data: data and data.get('type') in ['fund', 'manager']
        )
        
        self.context_menu.add_command(
            "Analyser",
            lambda data: self._analyze_item(data),
            lambda data: data and data.get('type') == 'composition'
        )
    
    def _setup_action_buttons(self):
        """Configure les boutons d'action."""
        self.action_buttons = ActionButtonManager(self)
        
        # Ajout des boutons standard
        self.action_buttons.add_button(
            "Éditer",
            lambda item_id: self._edit_item(item_id),
            icon=self.icons.get('detail'),
            tooltip="Modifier cet élément"
        )
        
        self.action_buttons.add_button(
            "Supprimer",
            lambda item_id: self._delete_item(item_id),
            tooltip="Supprimer cet élément"
        )
    
    def _on_right_click(self, event):
        """Gère le clic droit sur un élément."""
        item = self.tree.identify('item', event.x, event.y)
        if item:
            # Sélectionne l'élément cliqué
            self.tree.selection_set(item)
            
            # Récupère les données de l'élément
            item_data = self._get_item_data(item)
            
            # Affiche le menu contextuel
            self.context_menu.show_menu(event, item_data)
    
    def _get_item_data(self, item_id: str) -> Dict[str, Any]:
        """Récupère les données d'un élément.
        
        Args:
            item_id: Identifiant de l'élément
        
        Returns:
            Dictionnaire des données de l'élément
        """
        item = self.tree.item(item_id)
        values = item['values']
        
        return {
            'id': item_id,
            'name': item['text'],
            'type': values[0] if values else None,
            'value': values[1] if values else None,
            'currency': values[2] if values else None,
            'last_update': values[3] if values else None
        }
    
    def _refresh_item(self, data: Dict[str, Any]):
        """Rafraîchit les données d'un élément.
        
        Args:
            data: Données de l'élément
        """
        # À implémenter selon les besoins
        print(f"Rafraîchissement de {data['name']}")
    
    def _analyze_item(self, data: Dict[str, Any]):
        """Analyse une composition.
        
        Args:
            data: Données de la composition
        """
        # À implémenter selon les besoins
        print(f"Analyse de {data['name']}")
    
    def _edit_item(self, item_id: str):
        """Édite un élément.
        
        Args:
            item_id: Identifiant de l'élément
        """
        data = self._get_item_data(item_id)
        print(f"Édition de {data['name']}")
    
    def _delete_item(self, item_id: str):
        """Supprime un élément.
        
        Args:
            item_id: Identifiant de l'élément
        """
        data = self._get_item_data(item_id)
        if tk.messagebox.askyesno("Confirmation", f"Voulez-vous vraiment supprimer {data['name']} ?"):
            self.tree.delete(item_id)
    
    def _load_sample_data(self):
        """Charge des données de test."""
        # Exemple de données
        funds_data = {
            'Fonds Actions Europe': {
                'type': 'Actions',
                'value': 1000000,
                'currency': 'EUR',
                'managers': {
                    'Gestionnaire 1': {
                        'compositions': {
                            'Actions Large Cap': {'value': 500000},
                            'Actions Mid Cap': {'value': 300000},
                            'Actions Small Cap': {'value': 200000}
                        }
                    },
                    'Gestionnaire 2': {
                        'compositions': {
                            'Actions Tech': {'value': 400000},
                            'Actions Finance': {'value': 600000}
                        }
                    }
                }
            },
            'Fonds Obligations': {
                'type': 'Obligations',
                'value': 2000000,
                'currency': 'USD',
                'managers': {
                    'Gestionnaire 3': {
                        'compositions': {
                            'Obligations État': {'value': 1200000},
                            'Obligations Corporate': {'value': 800000}
                        }
                    }
                }
            }
        }
        
        # Ajout des données dans le TreeView
        for fund_name, fund_data in funds_data.items():
            fund_id = self.tree.insert(
                '',
                'end',
                text=fund_name,
                values=(
                    fund_data['type'],
                    f"{fund_data['value']:,.2f}",
                    fund_data['currency'],
                    datetime.now().strftime('%Y-%m-%d %H:%M'),
                    '⚙️ 🗑️'  # Icônes pour les actions
                ),
                image=self.icons.get('fund')
            )
            
            # Ajout des gestionnaires
            for manager_name, manager_data in fund_data['managers'].items():
                manager_id = self.tree.insert(
                    fund_id,
                    'end',
                    text=manager_name,
                    values=(
                        'Gestionnaire',
                        '',
                        '',
                        '',
                        '⚙️ 🗑️'  # Icônes pour les actions
                    ),
                    image=self.icons.get('manager')
                )
                
                # Ajout des compositions
                for comp_name, comp_data in manager_data['compositions'].items():
                    comp_id = self.tree.insert(
                        manager_id,
                        'end',
                        text=comp_name,
                        values=(
                            'Composition',
                            f"{comp_data['value']:,.2f}",
                            fund_data['currency'],
                            datetime.now().strftime('%Y-%m-%d %H:%M'),
                            '⚙️ 🗑️'  # Icônes pour les actions
                        ),
                        image=self.icons.get('composition')
                    )
        
        # Binding pour les clics sur la colonne des actions
        self.tree.bind('<Button-1>', self._on_click)
    
    def _on_item_selected(self, event):
        """Gère la sélection d'un élément dans le TreeView."""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        values = item['values']
        
        # Mise à jour des labels de détail
        self.detail_labels['Nom complet:'].configure(text=item['text'])
        if values:
            self.detail_labels['Type:'].configure(text=values[0])
            self.detail_labels['Valeur:'].configure(text=values[1] if values[1] else '')
            self.detail_labels['Devise:'].configure(text=values[2] if values[2] else '')
            self.detail_labels['Dernière mise à jour:'].configure(text=values[3] if values[3] else '')
    
    def _on_double_click(self, event):
        """Gère le double-clic sur une cellule."""
        print(f"Double-clic détecté à x={event.x}, y={event.y}")  # Debug
        
        region = self.tree.identify_region(event.x, event.y)
        print(f"Région: {region}")  # Debug
        
        if region == "cell":
            item = self.tree.identify_row(event.y)
            column = self.tree.identify_column(event.x)
            print(f"Item: {item}, Colonne: {column}")  # Debug
            
            # Ne permet pas l'édition de la colonne des actions
            if column == '#5':  # Colonne des actions
                print("Colonne des actions - pas d'édition")  # Debug
                return
            
            # Empêche le développement/réduction de l'arbre
            self.tree.after(50, lambda: self.cell_editor.start_edit(item, column))
            return "break"  # Empêche la propagation de l'événement
    
    def _on_click(self, event):
        """Gère les clics sur le TreeView."""
        # Identifie l'élément et la colonne cliqués
        region = self.tree.identify_region(event.x, event.y)
        if region == "cell":
            item = self.tree.identify_row(event.y)
            column = self.tree.identify_column(event.x)
            
            # Si c'est la colonne des actions (dernière colonne)
            if column == '#5':  # La colonne des actions est la 5ème
                # Récupère la position du clic dans la cellule
                cell_box = self.tree.bbox(item, column)
                if cell_box:
                    x_rel = event.x - cell_box[0]
                    # Première moitié de la cellule = éditer
                    if x_rel < cell_box[2] / 2:
                        self._edit_item(item)
                    # Seconde moitié = supprimer
                    else:
                        self._delete_item(item)

    def _create_menu(self):
        """Crée le menu principal."""
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        
        # Menu Fichier
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Fichier", menu=file_menu)
        file_menu.add_command(label="Nouveau", command=self._new_project)
        file_menu.add_command(label="Ouvrir...", command=self._load_project)
        file_menu.add_command(label="Enregistrer", command=self._save_project)
        file_menu.add_command(label="Enregistrer sous...", command=self._save_project_as)
        file_menu.add_separator()
        file_menu.add_command(label="Quitter", command=self.quit)
    
    def _new_project(self):
        """Crée un nouveau projet."""
        if messagebox.askyesno("Nouveau projet", "Voulez-vous créer un nouveau projet ? Les données non sauvegardées seront perdues."):
            for item in self.tree.get_children():
                self.tree.delete(item)
    
    def _save_project(self):
        """Enregistre le projet."""
        if not hasattr(self, 'current_file'):
            self._save_project_as()
        else:
            self._save_to_file(self.current_file)
    
    def _save_project_as(self):
        """Enregistre le projet sous un nouveau nom."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("Fichiers JSON", "*.json"), ("Tous les fichiers", "*.*")],
            title="Enregistrer le projet sous..."
        )
        if file_path:
            self.current_file = file_path
            self._save_to_file(file_path)
    
    def _save_to_file(self, file_path: str):
        """Sauvegarde les données dans un fichier.
        
        Args:
            file_path: Chemin du fichier
        """
        try:
            data = self._serialize_tree()
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            messagebox.showinfo("Succès", "Projet sauvegardé avec succès!")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde : {str(e)}")
    
    def _load_project(self):
        """Charge un projet depuis un fichier."""
        file_path = filedialog.askopenfilename(
            filetypes=[("Fichiers JSON", "*.json"), ("Tous les fichiers", "*.*")],
            title="Ouvrir un projet"
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.current_file = file_path
                self._new_project()  # Efface les données actuelles
                self._deserialize_tree(data)
                messagebox.showinfo("Succès", "Projet chargé avec succès!")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors du chargement : {str(e)}")
    
    def _serialize_tree(self) -> Dict:
        """Sérialise les données de l'arbre.
        
        Returns:
            Dictionnaire des données
        """
        def serialize_node(node_id):
            node = self.tree.item(node_id)
            children = self.tree.get_children(node_id)
            
            node_data = {
                'text': node['text'],
                'values': node['values'],
                'children': [serialize_node(child) for child in children]
            }
            return node_data
        
        root_nodes = self.tree.get_children()
        return {
            'version': '1.0',
            'date': datetime.now().isoformat(),
            'nodes': [serialize_node(node) for node in root_nodes]
        }
    
    def _deserialize_tree(self, data: Dict):
        """Désérialise les données dans l'arbre.
        
        Args:
            data: Données à charger
        """
        def deserialize_node(node_data, parent=''):
            node_id = self.tree.insert(
                parent,
                'end',
                text=node_data['text'],
                values=node_data['values'],
                image=self._get_icon_for_type(node_data['values'][0] if node_data['values'] else None)
            )
            
            for child in node_data['children']:
                deserialize_node(child, node_id)
        
        for node in data['nodes']:
            deserialize_node(node)
    
    def _get_icon_for_type(self, type_name: Optional[str]) -> Optional[ImageTk.PhotoImage]:
        """Retourne l'icône correspondant au type.
        
        Args:
            type_name: Nom du type
        
        Returns:
            Icône correspondante
        """
        if type_name == 'Actions' or type_name == 'Obligations':
            return self.icons.get('fund')
        elif type_name == 'Gestionnaire':
            return self.icons.get('manager')
        elif type_name == 'Composition':
            return self.icons.get('composition')
        return None

def main():
    """Point d'entrée de l'application."""
    app = FundExplorer()
    app.mainloop()

if __name__ == "__main__":
    main() 
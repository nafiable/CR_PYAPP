"""
Gestion des menus contextuels pour les TreeView et DataFrames.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, Callable, Optional
import pandas as pd

class ContextMenuManager:
    """Gestionnaire de menus contextuels."""
    
    def __init__(self, parent):
        """Initialise le gestionnaire de menus contextuels.
        
        Args:
            parent: Widget parent (TreeView ou Frame contenant un DataFrame)
        """
        self.parent = parent
        self.context_menu = tk.Menu(parent, tearoff=0)
        self.current_item = None
        self.current_data = None
        
        # Stockage des callbacks
        self.callbacks = {
            'edit': None,
            'delete': None,
            'export': None,
            'details': None
        }
    
    def add_command(self, label: str, callback: Callable, condition: Optional[Callable] = None):
        """Ajoute une commande au menu contextuel.
        
        Args:
            label: Libellé de la commande
            callback: Fonction à appeler
            condition: Fonction qui détermine si la commande doit être affichée
        """
        self.callbacks[label] = {
            'callback': callback,
            'condition': condition
        }
    
    def show_menu(self, event, item_data: Dict[str, Any] = None):
        """Affiche le menu contextuel.
        
        Args:
            event: Événement de clic droit
            item_data: Données de l'élément sélectionné
        """
        self.current_data = item_data
        
        # Reconstruction du menu
        self.context_menu.delete(0, tk.END)
        
        # Ajout des commandes standard
        if item_data:
            self.context_menu.add_command(
                label="Détails",
                command=lambda: self._show_details(item_data)
            )
            self.context_menu.add_separator()
            
            self.context_menu.add_command(
                label="Modifier",
                command=lambda: self._handle_edit(item_data)
            )
            self.context_menu.add_command(
                label="Supprimer",
                command=lambda: self._handle_delete(item_data)
            )
            self.context_menu.add_separator()
            
            self.context_menu.add_command(
                label="Exporter",
                command=lambda: self._handle_export(item_data)
            )
        
        # Ajout des commandes personnalisées
        for label, info in self.callbacks.items():
            if isinstance(info, dict):
                callback = info['callback']
                condition = info['condition']
                
                if condition is None or condition(item_data):
                    self.context_menu.add_command(
                        label=label,
                        command=lambda cb=callback: cb(item_data)
                    )
        
        # Affichage du menu
        self.context_menu.post(event.x_root, event.y_root)
    
    def _show_details(self, data: Dict[str, Any]):
        """Affiche une fenêtre avec les détails de l'élément.
        
        Args:
            data: Données de l'élément
        """
        details_window = tk.Toplevel(self.parent)
        details_window.title("Détails")
        details_window.geometry("400x300")
        
        # Frame avec scrollbar
        frame = ttk.Frame(details_window)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Affichage des données
        for i, (key, value) in enumerate(data.items()):
            ttk.Label(
                scrollable_frame,
                text=f"{key}:",
                font=('Helvetica', 10, 'bold')
            ).grid(row=i, column=0, sticky='w', padx=5, pady=2)
            
            ttk.Label(
                scrollable_frame,
                text=str(value),
                font=('Helvetica', 10)
            ).grid(row=i, column=1, sticky='w', padx=5, pady=2)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _handle_edit(self, data: Dict[str, Any]):
        """Gère l'édition d'un élément.
        
        Args:
            data: Données de l'élément
        """
        if self.callbacks['edit']:
            self.callbacks['edit'](data)
        else:
            messagebox.showinfo("Info", "Fonctionnalité d'édition non implémentée")
    
    def _handle_delete(self, data: Dict[str, Any]):
        """Gère la suppression d'un élément.
        
        Args:
            data: Données de l'élément
        """
        if self.callbacks['delete']:
            if messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer cet élément ?"):
                self.callbacks['delete'](data)
        else:
            messagebox.showinfo("Info", "Fonctionnalité de suppression non implémentée")
    
    def _handle_export(self, data: Dict[str, Any]):
        """Gère l'export d'un élément.
        
        Args:
            data: Données de l'élément
        """
        if self.callbacks['export']:
            self.callbacks['export'](data)
        else:
            messagebox.showinfo("Info", "Fonctionnalité d'export non implémentée")

class ActionButtonManager:
    """Gestionnaire de boutons d'action pour les lignes."""
    
    def __init__(self, parent, column_name: str = "Actions"):
        """Initialise le gestionnaire de boutons d'action.
        
        Args:
            parent: Widget parent (TreeView ou Frame)
            column_name: Nom de la colonne des actions
        """
        self.parent = parent
        self.column_name = column_name
        self.buttons = {}
        self.callbacks = {}
    
    def add_button(
        self,
        name: str,
        callback: Callable,
        icon: Optional[str] = None,
        tooltip: Optional[str] = None
    ):
        """Ajoute un bouton d'action.
        
        Args:
            name: Nom du bouton
            callback: Fonction à appeler
            icon: Chemin vers l'icône (optionnel)
            tooltip: Texte d'aide (optionnel)
        """
        self.buttons[name] = {
            'callback': callback,
            'icon': icon,
            'tooltip': tooltip
        }
    
    def create_button_frame(self, item_id: str) -> ttk.Frame:
        """Crée un frame contenant les boutons d'action.
        
        Args:
            item_id: Identifiant de la ligne
        
        Returns:
            Frame contenant les boutons
        """
        frame = ttk.Frame(self.parent)
        
        for name, info in self.buttons.items():
            btn = ttk.Button(
                frame,
                text=name if not info['icon'] else '',
                image=info['icon'] if info['icon'] else None,
                command=lambda cb=info['callback']: cb(item_id)
            )
            btn.pack(side=tk.LEFT, padx=2)
            
            if info['tooltip']:
                self._create_tooltip(btn, info['tooltip'])
        
        return frame
    
    def _create_tooltip(self, widget: tk.Widget, text: str):
        """Crée une infobulle pour un widget.
        
        Args:
            widget: Widget concerné
            text: Texte de l'infobulle
        """
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = ttk.Label(tooltip, text=text, background="#ffffe0")
            label.pack()
            
            def hide_tooltip():
                tooltip.destroy()
            
            widget.tooltip = tooltip
            widget.bind('<Leave>', lambda e: hide_tooltip())
            tooltip.bind('<Leave>', lambda e: hide_tooltip())
        
        widget.bind('<Enter>', show_tooltip) 
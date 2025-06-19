# Interfaces Graphiques - Finance API

Ce dossier contient toutes les interfaces graphiques de l'application Finance API, organisées de manière centralisée.

## 🚀 Lancement rapide

Pour lancer la fenêtre principale qui permet d'accéder à toutes les interfaces :

```bash
python ui/main_window.py
```

## 📋 Interfaces disponibles

### 🌳 TreeView Fonds (`treeview_fonds.py`)
**Interface principale pour la gestion des fonds et gestionnaires**

- **Fonctionnalités** :
  - Affichage hiérarchique : Gestionnaires > Fonds
  - Double-clic sur un fonds : menu d'options (modifier, supprimer, afficher composition)
  - Clic droit : menu contextuel avec actions supplémentaires
  - Affichage de la composition des fonds dans une fenêtre séparée
  - Panneau de détails pour les gestionnaires
  - Barre d'outils avec actions rapides

- **Utilisation** :
  ```bash
  python ui/treeview_fonds.py
  ```

### 🗄️ Visualiseur Base de Données (`db_viewer.py`)
**Outil d'exploration de la base de données SQLite**

- **Fonctionnalités** :
  - Liste des tables de la base
  - Affichage de la structure des tables (PRAGMA table_info)
  - Affichage des données en tableau interactif
  - Navigation entre les tables

- **Utilisation** :
  ```bash
  python ui/db_viewer.py
  ```

### 📊 Analyse Avancée (`advanced_view.py`)
**Interface d'analyse avec graphiques et filtres**

- **Fonctionnalités** :
  - Graphiques de répartition par secteur
  - Évolution de la valeur du portefeuille
  - Filtres par date et gestionnaire
  - Analyse de performance
  - Onglets multiples pour différentes vues

- **Utilisation** :
  ```bash
  python ui/advanced_view.py
  ```

### 📋 Visualiseur DataFrame (`dataframe_viewer.py`)
**Affichage de DataFrames avec interface web**

- **Fonctionnalités** :
  - Affichage de DataFrames en HTML avec Bootstrap
  - Résumé statistique des données
  - Historique des DataFrames chargés
  - Interface web responsive
  - Intégration FastAPI

- **Utilisation** :
  - Via l'API FastAPI : `/ui/view`
  - Ou directement : `python ui/dataframe_viewer.py`

### 🎬 Démo Viewers (`demo_viewers.py`)
**Démonstrations des différents viewers**

- **Fonctionnalités** :
  - Exemples d'utilisation des différents viewers
  - Démonstrations avec données de test
  - Comparaison des interfaces

- **Utilisation** :
  ```bash
  python ui/demo_viewers.py
  ```

### 📚 Exemple d'Utilisation (`exemple_utilisation.py`)
**Exemples d'utilisation des interfaces**

- **Fonctionnalités** :
  - Exemples complets d'utilisation
  - Cas d'usage réels
  - Tutoriels intégrés

- **Utilisation** :
  ```bash
  python ui/exemple_utilisation.py
  ```

## 🛠️ Dépendances requises

```bash
pip install tkinter ttkthemes pandastable pandas matplotlib
```

## 📁 Structure du dossier

```
ui/
├── __init__.py              # Package Python
├── main_window.py           # Fenêtre principale
├── treeview_fonds.py        # TreeView Gestionnaires > Fonds
├── db_viewer.py             # Visualiseur base de données
├── advanced_view.py         # Analyse avancée avec graphiques
├── dataframe_viewer.py      # Visualiseur DataFrame web
├── demo_viewers.py          # Démonstrations
├── exemple_utilisation.py   # Exemples d'utilisation
└── README.md               # Cette documentation
```

## 🎯 Fonctionnalités communes

Toutes les interfaces partagent :
- **Thème unifié** : Utilisation de `ttkthemes` avec le thème "arc"
- **Gestion d'erreurs** : Messages d'erreur informatifs
- **Interface responsive** : Adaptation à différentes tailles d'écran
- **Logging** : Journalisation des actions importantes

## 🔧 Personnalisation

### Ajouter une nouvelle interface

1. Créez votre fichier dans le dossier `ui/`
2. Ajoutez-la à la liste dans `main_window.py`
3. Documentez-la dans ce README

### Modifier le thème

Changez le thème dans chaque interface :
```python
self.root = ThemedTk(theme="arc")  # arc, breeze, equilux, etc.
```

## 🚨 Dépannage

### Erreur "Module not found"
```bash
# Assurez-vous d'être dans le répertoire racine du projet
cd /chemin/vers/MYPYAPP
python ui/main_window.py
```

### Erreur de base de données
- Vérifiez que `ma_base.db` existe
- Lancez d'abord `examples/populate_database.py`

### Interface ne se lance pas
- Vérifiez les dépendances : `pip install -r requirements.txt`
- Consultez les logs pour plus de détails

## 📞 Support

Pour toute question ou problème :
1. Consultez la documentation de chaque interface
2. Vérifiez les logs d'erreur
3. Testez avec les exemples fournis 
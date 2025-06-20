# Exemples d'utilisation

Ce répertoire contient des exemples d'utilisation de l'API pour la gestion des données financières.

## 📁 Structure des fichiers

### 🔧 Scripts de base de données
- **`populate_database.py`** - Script pour peupler la base de données SQLite avec des données de test
- **`check_database.py`** - Script pour vérifier l'état et le contenu de la base de données

### 🧪 Scripts de test
- **`test_operations.py`** - Script pour tester les différentes opérations sur les données

### 📂 Dossiers
- **`output/`** - Répertoire contenant les fichiers générés par les exemples

## 🚀 Utilisation

### 1. Peuplement de la base de données
```bash
python -m examples.populate_database
```

Ce script va créer et peupler la base de données avec :
- Des gestionnaires
- Des régions et pays
- Des devises
- Des secteurs
- Des types et sous-types d'actifs
- Des classifications
- Des titres
- Des indices
- Des fonds (simples et portefeuilles)
- Des compositions de fonds, portefeuilles et indices

### 2. Vérification de la base de données
```bash
# Vérifier le contenu
python -m examples.check_database

# Vérifier le contenu + schéma détaillé
python -m examples.check_database --schema
```

### 3. Test des opérations
```bash
python -m examples.test_operations
```

Ce script va tester :
- Les opérations CRUD sur les différentes entités
- La lecture des compositions
- L'export des données en CSV et Excel
- L'affichage des données avec le DataFrameViewer

## 📊 Fonctionnalités de check_database.py

Le script `check_database.py` offre plusieurs fonctionnalités :

### ✅ Vérification du contenu
- Compte le nombre d'enregistrements dans chaque table
- Affiche les détails des gestionnaires
- Vérifie l'existence des tables importantes
- Affiche l'état des tables de composition

### 🔍 Analyse du schéma
- Affiche la structure complète de toutes les tables
- Montre les types de données, contraintes et clés primaires
- Utile pour diagnostiquer les problèmes de structure

### 📈 Tables surveillées
- **Tables principales** : gestionnaire, fonds, titre, pays, devise, secteur, region, type_actif
- **Tables de composition** : composition_fonds, composition_portefeuille, composition_indice

### 🛠️ Exemples d'utilisation programmatique
```python
from examples.check_database import check_database, check_database_schema

# Vérifier le contenu
success = check_database('database.db')

# Afficher le schéma
check_database_schema('database.db')
```

## 🏗️ Structure des données

### Relations principales

1. **Gestionnaire -> Fonds** : Un gestionnaire peut gérer plusieurs fonds
2. **Region -> Pays** : Une région contient plusieurs pays
3. **Pays -> Devise** : Un pays a une devise
4. **TypeActif -> SousTypeActif** : Un type d'actif peut avoir plusieurs sous-types
5. **Classif -> SousClassif** : Une classification peut avoir plusieurs sous-classifications
6. **Fonds -> Titre** : Un fonds contient plusieurs titres
7. **Portefeuille -> Fonds/Titre** : Un portefeuille peut contenir des fonds simples et des titres
8. **Indice -> Titre** : Un indice est composé de plusieurs titres

### Tables de composition

1. **`composition_fonds`** : Composition des fonds simples
   - date, id_fonds, id_gestionnaire, id_titre, id_devise, id_pays
   - quantité, prix, valeur_marchande, accrued, dividende

2. **`composition_portefeuille`** : Composition des portefeuilles
   - Mêmes champs que composition_fonds
   - Peut contenir des références à des fonds simples

3. **`composition_indice`** : Composition des indices
   - date, id_indice, id_titre, id_devise, id_pays
   - quantité, prix, valeur_marchande, dividende

## 📝 Exemples de requêtes

Le script `test_operations.py` montre comment :
- Récupérer les fonds gérés par un gestionnaire
- Obtenir les pays d'une région
- Lire la composition d'un fonds à une date donnée
- Exporter les données en CSV/Excel
- Visualiser les données avec le DataFrameViewer

## 🔧 Workflow recommandé

1. **Initialiser la base de données** :
   ```bash
   python -m database.init_db
   ```

2. **Peupler avec des données de test** :
   ```bash
   python -m examples.populate_database
   ```

3. **Vérifier que tout fonctionne** :
   ```bash
   python -m examples.check_database
   ```

4. **Tester les opérations** :
   ```bash
   python -m examples.test_operations
   ```

## 📝 Notes importantes

- Le script `check_database.py` utilise SQLite par défaut
- Assurez-vous que la base de données est initialisée avant de la vérifier
- Les erreurs sont affichées clairement avec des emojis pour faciliter la lecture
- Le script peut être utilisé pour diagnostiquer les problèmes de migration ou de données

## 🔧 Personnalisation

Vous pouvez modifier le script `check_database.py` pour :
- Ajouter de nouvelles tables à surveiller
- Modifier les requêtes de diagnostic
- Ajouter des vérifications spécifiques à votre application
- Changer le format d'affichage des résultats 
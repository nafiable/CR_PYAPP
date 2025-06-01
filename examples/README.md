# Exemples d'utilisation

Ce répertoire contient des exemples d'utilisation de l'API pour la gestion des données financières.

## Structure des fichiers

- `populate_database.py` : Script pour peupler la base de données SQLite avec des données de test
- `test_operations.py` : Script pour tester les différentes opérations sur les données
- `output/` : Répertoire contenant les fichiers générés par les exemples

## Utilisation

1. Peuplement de la base de données :
```bash
python examples/populate_database.py
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

2. Test des opérations :
```bash
python examples/test_operations.py
```
Ce script va tester :
- Les opérations CRUD sur les différentes entités
- La lecture des compositions
- L'export des données en CSV et Excel
- L'affichage des données avec le DataFrameViewer

## Structure des données

### Relations principales

1. Gestionnaire -> Fonds : Un gestionnaire peut gérer plusieurs fonds
2. Region -> Pays : Une région contient plusieurs pays
3. Pays -> Devise : Un pays a une devise
4. TypeActif -> SousTypeActif : Un type d'actif peut avoir plusieurs sous-types
5. Classif -> SousClassif : Une classification peut avoir plusieurs sous-classifications
6. Fonds -> Titre : Un fonds contient plusieurs titres
7. Portefeuille -> Fonds/Titre : Un portefeuille peut contenir des fonds simples et des titres
8. Indice -> Titre : Un indice est composé de plusieurs titres

### Tables de composition

1. `composition_fonds` : Composition des fonds simples
   - date, id_fonds, id_gestionnaire, id_titre, id_devise, id_pays
   - quantité, prix, valeur_marchande, accrued, dividende

2. `composition_portefeuille` : Composition des portefeuilles
   - Mêmes champs que composition_fonds
   - Peut contenir des références à des fonds simples

3. `composition_indice` : Composition des indices
   - date, id_indice, id_titre, id_devise, id_pays
   - quantité, prix, valeur_marchande, dividende

## Exemples de requêtes

Le script `test_operations.py` montre comment :
- Récupérer les fonds gérés par un gestionnaire
- Obtenir les pays d'une région
- Lire la composition d'un fonds à une date donnée
- Exporter les données en CSV/Excel
- Visualiser les données avec le DataFrameViewer 
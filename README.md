# API Financière FastAPI

## Description
API de gestion des fonds, portefeuilles et données financières développée avec FastAPI.

## Fonctionnalités
- Gestion des gestionnaires de fonds
- Gestion des fonds et portefeuilles
- Gestion des titres et indices
- Gestion des compositions de fonds et portefeuilles
- Support de deux bases de données (SQL Server et SQLite)
- Gestion de fichiers (CSV, Excel, PDF)
- Support SFTP
- Documentation automatique avec FastAPI
- Gestion des logs
- Support multilingue

## Structure du Projet
```
MYPYAPP/
├── config/
│   ├── __init__.py
│   └── logging_config.py
├── constantes/
│   ├── __init__.py
│   └── const1.py
├── database/
│   ├── __init__.py
│   ├── connexionsqlServer.py
│   ├── connexionsqlLiter.py
│   └── sqliteCreation.sql
├── logic/
│   ├── __init__.py
│   └── dispatcher.py
├── schemas/
│   ├── __init__.py
│   ├── base.py
│   └── entities.py
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── config.env
├── main.py
├── README.md
└── requirements.txt
```

## Installation

1. Créer un environnement virtuel :
```bash
python -m venv .venv
```

2. Activer l'environnement virtuel :
- Windows :
```bash
.venv\Scripts\activate
```
- Linux/Mac :
```bash
source .venv/bin/activate
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

4. Configurer les variables d'environnement dans `config.env`

5. Initialiser la base de données SQLite :
```bash
python -c "from database.connexionsqlLiter import SQLiteConnection; SQLiteConnection().init_database()"
```

## Utilisation

1. Démarrer le serveur :
```bash
uvicorn main:app --reload
```

2. Accéder à la documentation :
- Swagger UI : http://localhost:8000/docs
- ReDoc : http://localhost:8000/redoc

## Tests
```bash
pytest tests/
```

## Développement

1. Installer les dépendances de développement :
```bash
pip install -r requirements.txt
```

2. Formatter le code :
```bash
black .
```

3. Vérifier le code :
```bash
flake8 .
mypy .
```

## Contribution
1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Créer une Pull Request

## Licence
Ce projet est sous licence MIT.
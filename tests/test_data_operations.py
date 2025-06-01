"""
Tests des opérations sur les données.
"""

import pytest
import pandas as pd
from pathlib import Path
import sqlite3
import os
from fastapi.testclient import TestClient

from main import app
from utils.csv_manager import CSVManager
from utils.excel_manager import ExcelManager
from database.connexionsqlLiter import SQLiteConnection

# Client de test
client = TestClient(app)

# Gestionnaires
csv_manager = CSVManager()
excel_manager = ExcelManager()

# Données de test
TEST_DATA = {
    "gestionnaire": [
        {
            "code": "GEST001",
            "nom": "Gestionnaire Test",
            "tel": "0123456789",
            "email": "test@test.com"
        }
    ],
    "region1": [
        {
            "code": "EUR",
            "nom": "Europe"
        }
    ]
}

@pytest.fixture
def setup_test_db():
    """Prépare la base de données de test."""
    # Création de la base de test
    db_path = Path("test.db")
    if db_path.exists():
        db_path.unlink()
    
    # Initialisation de la base
    sqlite_conn = SQLiteConnection()
    sqlite_conn.init_database()
    
    # Insertion des données de test
    with sqlite3.connect(db_path) as conn:
        for table, data in TEST_DATA.items():
            df = pd.DataFrame(data)
            df.to_sql(table, conn, if_exists='append', index=False)
    
    yield db_path
    
    # Nettoyage
    if db_path.exists():
        db_path.unlink()

def test_get_tables(setup_test_db):
    """Teste la récupération des tables."""
    response = client.get("/api/tables")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert "gestionnaire" in response.json()
    assert "region1" in response.json()

def test_get_table_data(setup_test_db):
    """Teste la récupération des données d'une table."""
    response = client.get("/api/data/gestionnaire")
    assert response.status_code == 200
    data = response.json()
    assert "columns" in data
    assert "data" in data
    assert len(data["data"]) == 1
    assert data["data"][0]["code"] == "GEST001"

def test_csv_operations(setup_test_db):
    """Teste les opérations CSV."""
    # Création d'un CSV de test
    test_data = pd.DataFrame(TEST_DATA["gestionnaire"])
    csv_path = Path("test.csv")
    csv_manager.write_csv(test_data, csv_path)
    
    # Test de lecture
    df = csv_manager.read_csv(csv_path)
    assert len(df) == 1
    assert df.iloc[0]["code"] == "GEST001"
    
    # Test d'import
    with open(csv_path, "rb") as f:
        response = client.post(
            "/api/import/csv/gestionnaire",
            files={"file": ("test.csv", f, "text/csv")}
        )
    assert response.status_code == 200
    
    # Test d'export
    response = client.get("/api/export/csv/gestionnaire")
    assert response.status_code == 200
    
    # Nettoyage
    csv_path.unlink()

def test_excel_operations(setup_test_db):
    """Teste les opérations Excel."""
    # Création d'un Excel de test
    test_data = pd.DataFrame(TEST_DATA["gestionnaire"])
    excel_path = Path("test.xlsx")
    excel_manager.create_workbook()
    excel_manager.write_dataframe(test_data, "Sheet1")
    excel_manager.save(excel_path)
    
    # Test de lecture
    excel_manager.open_workbook(excel_path)
    df = excel_manager.read_sheet()
    assert len(df) == 1
    assert df.iloc[0]["code"] == "GEST001"
    
    # Test d'import
    with open(excel_path, "rb") as f:
        response = client.post(
            "/api/import/excel/gestionnaire",
            files={"file": ("test.xlsx", f, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
        )
    assert response.status_code == 200
    
    # Test d'export
    response = client.get("/api/export/excel/gestionnaire")
    assert response.status_code == 200
    
    # Nettoyage
    excel_path.unlink()

def test_sync_operations(setup_test_db):
    """Teste les opérations de synchronisation."""
    # Note: Ce test nécessite une connexion SQL Server configurée
    if os.getenv("SQLSERVER_SERVER"):
        response = client.post("/api/sync/sqlserver/gestionnaire")
        assert response.status_code == 200
    else:
        pytest.skip("SQL Server non configuré") 
"""
Routes pour la gestion des données.
"""

import logging
from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path
import pandas as pd
from sqlalchemy import inspect

from database.connexionsqlServer import SQLServerConnection
from database.connexionsqlLiter import SQLiteConnection
from utils.csv_manager import CSVManager
from utils.excel_manager import ExcelManager

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api")
csv_manager = CSVManager()
excel_manager = ExcelManager()

@router.get("/tables", response_model=List[str])
async def get_tables():
    """
    Récupère la liste des tables disponibles.
    
    Returns:
        List[str]: Liste des noms de tables
    """
    try:
        sqlite_conn = SQLiteConnection()
        with sqlite_conn.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
        return tables
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des tables: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/data/{table}", response_model=Dict[str, Any])
async def get_table_data(table: str):
    """
    Récupère les données d'une table.
    
    Args:
        table (str): Nom de la table
        
    Returns:
        Dict[str, Any]: Données de la table
    """
    try:
        sqlite_conn = SQLiteConnection()
        with sqlite_conn.get_connection() as conn:
            df = pd.read_sql(f"SELECT * FROM {table}", conn)
        
        return {
            "columns": df.columns.tolist(),
            "data": df.to_dict('records')
        }
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des données: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/import/csv/{table}")
async def import_csv(table: str, file: UploadFile = File(...)):
    """
    Importe un fichier CSV dans une table.
    
    Args:
        table (str): Nom de la table
        file (UploadFile): Fichier CSV
    """
    try:
        # Sauvegarde temporaire du fichier
        temp_path = Path("temp") / file.filename
        temp_path.parent.mkdir(exist_ok=True)
        
        with temp_path.open("wb") as f:
            content = await file.read()
            f.write(content)
        
        # Lecture et import des données
        df = csv_manager.read_csv(temp_path)
        sqlite_conn = SQLiteConnection()
        csv_manager.to_sqlite(df, table, sqlite_conn.database_path, if_exists='append')
        
        # Nettoyage
        temp_path.unlink()
        
        return {"message": "Import réussi"}
    except Exception as e:
        logger.error(f"Erreur lors de l'import CSV: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/import/excel/{table}")
async def import_excel(table: str, file: UploadFile = File(...)):
    """
    Importe un fichier Excel dans une table.
    
    Args:
        table (str): Nom de la table
        file (UploadFile): Fichier Excel
    """
    try:
        # Sauvegarde temporaire du fichier
        temp_path = Path("temp") / file.filename
        temp_path.parent.mkdir(exist_ok=True)
        
        with temp_path.open("wb") as f:
            content = await file.read()
            f.write(content)
        
        # Lecture et import des données
        excel_manager.open_workbook(temp_path)
        df = excel_manager.read_sheet()
        sqlite_conn = SQLiteConnection()
        excel_manager.to_sqlite(df, table, sqlite_conn.database_path, if_exists='append')
        
        # Nettoyage
        temp_path.unlink()
        
        return {"message": "Import réussi"}
    except Exception as e:
        logger.error(f"Erreur lors de l'import Excel: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/export/csv/{table}")
async def export_csv(table: str):
    """
    Exporte une table en CSV.
    
    Args:
        table (str): Nom de la table
    """
    try:
        # Création du répertoire d'export
        export_path = Path("exports")
        export_path.mkdir(exist_ok=True)
        
        # Export des données
        sqlite_conn = SQLiteConnection()
        with sqlite_conn.get_connection() as conn:
            df = pd.read_sql(f"SELECT * FROM {table}", conn)
        
        output_path = export_path / f"{table}.csv"
        csv_manager.write_csv(df, output_path)
        
        return FileResponse(
            output_path,
            media_type="text/csv",
            filename=f"{table}.csv"
        )
    except Exception as e:
        logger.error(f"Erreur lors de l'export CSV: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/export/excel/{table}")
async def export_excel(table: str):
    """
    Exporte une table en Excel.
    
    Args:
        table (str): Nom de la table
    """
    try:
        # Création du répertoire d'export
        export_path = Path("exports")
        export_path.mkdir(exist_ok=True)
        
        # Export des données
        sqlite_conn = SQLiteConnection()
        with sqlite_conn.get_connection() as conn:
            df = pd.read_sql(f"SELECT * FROM {table}", conn)
        
        output_path = export_path / f"{table}.xlsx"
        excel_manager.create_workbook()
        excel_manager.write_dataframe(df, "Sheet1")
        excel_manager.save(output_path)
        
        return FileResponse(
            output_path,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=f"{table}.xlsx"
        )
    except Exception as e:
        logger.error(f"Erreur lors de l'export Excel: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/sync/sqlserver/{table}")
async def sync_to_sqlserver(table: str):
    """
    Synchronise une table SQLite vers SQL Server.
    
    Args:
        table (str): Nom de la table
    """
    try:
        # Lecture des données SQLite
        sqlite_conn = SQLiteConnection()
        with sqlite_conn.get_connection() as conn:
            df = pd.read_sql(f"SELECT * FROM {table}", conn)
        
        # Synchronisation vers SQL Server
        sqlserver_conn = SQLServerConnection()
        csv_manager.to_sql_server(
            df,
            table,
            sqlserver_conn.connection_string,
            if_exists='replace'
        )
        
        return {"message": "Synchronisation réussie"}
    except Exception as e:
        logger.error(f"Erreur lors de la synchronisation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 
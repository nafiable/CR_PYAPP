"""
Routes universelles pour la gestion des données via dispatcher.

Exemples d'appel pour /dispatcher ou /dispatcher-mapped :

1. Lister les tables d'une base SQLite :
POST /api/dispatcher
{
  "function": "list_tables",
  "data": { "db_path": "ma_base.db" }
}

2. Récupérer les données d'une table :
POST /api/dispatcher
{
  "function": "get_table_data",
  "data": { "db_path": "ma_base.db", "table": "gestionnaire" }
}

3. Importer un CSV dans une table :
POST /api/dispatcher
{
  "function": "import_csv",
  "data": { "csv_path": "chemin/monfichier.csv", "table": "ma_table", "db_path": "ma_base.db", "if_exists": "append" }
}

4. Exporter une table en CSV :
POST /api/dispatcher
{
  "function": "export_table_to_csv_sqlite",
  "data": { "table": "ma_table", "db_path": "ma_base.db", "output_path": "export/ma_table.csv" }
}

5. Synchroniser une table SQLite vers SQL Server :
POST /api/dispatcher
{
  "function": "sync_table_sqlite_to_sqlserver",
  "data": { "table": "ma_table", "sqlite_db_path": "ma_base.db", "sqlserver_conn_str": "..." }
}

Remplacez "dispatcher" par "dispatcher-mapped" pour utiliser le mapping.
"""

import logging
from fastapi import APIRouter, HTTPException, Request
from dispatcher import dispatch_request, dispatch_request_mapped
from utils.data_routes_utils import get_tables_sqlite, get_table_data_sqlite, import_csv_to_sqlite, export_table_to_csv_sqlite, sync_table_sqlite_to_sqlserver
from database.connexionsqlLiter import SQLiteConnection

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api")

@router.post("/dispatcher")
async def universal_dispatcher(request: Request):
    """
    Route universelle pour dispatcher les appels vers la logique métier (sans mapping).
    Voir exemples d'appel dans la docstring du fichier.
    """
    try:
        payload = await request.json()
        function_name = payload.get("function")
        data = payload.get("data", {})
        if not function_name:
            raise HTTPException(status_code=400, detail="Champ 'function' requis dans le payload.")
        response = await dispatch_request(function_name, data)
        return {"function": function_name, "result": response.get("data", None) or None}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur dans le dispatcher universel: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/dispatcher-mapped")
async def universal_dispatcher_mapped(request: Request):
    """
    Route universelle pour dispatcher les appels via mapping (alias, renommage, etc).
    Voir exemples d'appel dans la docstring du fichier.
    """
    try:
        payload = await request.json()
        function_name = payload.get("function")
        data = payload.get("data", {})
        if not function_name:
            raise HTTPException(status_code=400, detail="Champ 'function' requis dans le payload.")
        response = await dispatch_request_mapped(function_name, data)
        return {"function": function_name, "result": response.get("data", None) or None}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur dans le dispatcher-mapped: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

db_path = "ma_base.db"
tables = get_tables_sqlite(db_path)
print("Tables présentes :", tables)

df = get_table_data_sqlite("ma_base.db", "gestionnaire")
print(df.head())

import_csv_to_sqlite("chemin/monfichier.csv", "ma_table", "ma_base.db", if_exists="append")

export_table_to_csv_sqlite("ma_table", "ma_base.db", "export/ma_table.csv")

sqlite_db = "ma_base.db"
sqlserver_conn_str = "mssql+pyodbc://user:password@serveur/bdd?driver=ODBC+Driver+17+for+SQL+Server"
sync_table_sqlite_to_sqlserver("ma_table", sqlite_db, sqlserver_conn_str)

SQLiteConnection().init_database() 
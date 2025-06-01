"""
Script pour tester les différentes opérations sur les données.
"""

import asyncio
import logging
from datetime import date, datetime
from database.connexionsqlLiter import SQLiteConnection
from crud.entities import (
    gestionnaire_crud, region_crud, pays_crud, devise_crud,
    secteur_crud, type_actif_crud, sous_type_actif_crud,
    classif_crud, sous_classif_crud, titre_crud, indice_crud,
    fonds_crud, composition_fonds_crud, composition_portefeuille_crud,
    composition_indice_crud
)
from utils.csv_operations import CSVOperations
from utils.excel_operations import ExcelOperations
from ui.dataframe_viewer import DataFrameViewer

logger = logging.getLogger(__name__)

async def test_operations():
    """Teste les différentes opérations sur les données."""
    
    # Création de la connexion
    db = SQLiteConnection().get_session()
    
    try:
        # 1. Test des opérations CRUD
        logger.info("Test des opérations CRUD...")
        
        # Lecture d'un gestionnaire
        gestionnaire = await gestionnaire_crud.get_by_code(db, "GEST1")
        logger.info(f"Gestionnaire trouvé: {gestionnaire.nom}")
        
        # Lecture des fonds d'un gestionnaire
        fonds_gestionnaire = await fonds_crud.get_by_gestionnaire(db, gestionnaire.id)
        logger.info(f"Nombre de fonds pour {gestionnaire.nom}: {len(fonds_gestionnaire)}")
        
        # Lecture des pays d'une région
        region = await region_crud.get_by_code(db, "EUR")
        pays_region = await pays_crud.get_by_region(db, region.id)
        logger.info(f"Pays dans la région {region.nom}: {[p.nom for p in pays_region]}")
        
        # 2. Test des opérations sur les compositions
        logger.info("\nTest des opérations sur les compositions...")
        
        # Lecture de la composition d'un fonds
        today = date.today()
        fonds = await fonds_crud.get_by_code(db, "FUND1")
        compo_fonds = await composition_fonds_crud.get_composition_date(db, fonds.id, today)
        logger.info(f"Composition du fonds {fonds.nom}: {len(compo_fonds)} positions")
        
        # Lecture de la composition d'un portefeuille
        portefeuille = await fonds_crud.get_by_code(db, "PORT1")
        compo_port = await composition_portefeuille_crud.get_composition_date(db, portefeuille.id, today)
        logger.info(f"Composition du portefeuille {portefeuille.nom}: {len(compo_port)} positions")
        
        # 3. Test des opérations CSV/Excel
        logger.info("\nTest des opérations CSV/Excel...")
        
        csv_ops = CSVOperations()
        excel_ops = ExcelOperations()
        
        # Export des données en CSV
        query = "SELECT * FROM titre"
        csv_ops.sql_to_csv(query, "examples/output/titres.csv", is_sqlite=True)
        logger.info("Données des titres exportées en CSV")
        
        # Conversion CSV vers Excel
        csv_ops.csv_to_excel("examples/output/titres.csv", "examples/output/titres.xlsx")
        logger.info("CSV converti en Excel")
        
        # 4. Test du DataFrameViewer
        logger.info("\nTest du DataFrameViewer...")
        
        viewer = DataFrameViewer()
        df = excel_ops.read_excel("examples/output/titres.xlsx")
        viewer.set_dataframe(df, "Titres")
        summary = viewer.get_summary()
        logger.info(f"Résumé du DataFrame: {len(df)} lignes, {len(df.columns)} colonnes")
        
        logger.info("Tests terminés avec succès")
        
    except Exception as e:
        logger.error(f"Erreur lors des tests: {str(e)}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(test_operations()) 
"""
Script pour peupler la base de données avec des données de test.
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
from sqlalchemy import text
from sqlalchemy.sql import text

logger = logging.getLogger(__name__)

async def populate_database():
    """Peuple la base de données avec des données de test."""
    
    # Création de la connexion
    db = SQLiteConnection().get_session()
    
    try:
        # 1. Création des gestionnaires
        gestionnaires = [
            await gestionnaire_crud.create(db, {
                "code": "GEST1",
                "nom": "Gestionnaire 1",
                "tel": "+33123456789",
                "contact_principal": "John Doe",
                "email": "john.doe@gest1.com"
            }),
            await gestionnaire_crud.create(db, {
                "code": "GEST2",
                "nom": "Gestionnaire 2",
                "tel": "+33987654321",
                "contact_principal": "Jane Smith",
                "email": "jane.smith@gest2.com"
            })
        ]
        
        # 2. Création des régions
        regions = [
            await region_crud.create(db, {
                "code": "EUR",
                "nom": "Europe"
            }),
            await region_crud.create(db, {
                "code": "NAM",
                "nom": "Amérique du Nord"
            })
        ]
        
        # 3. Création des devises
        devises = [
            await devise_crud.create(db, {
                "code": "EUR",
                "nom": "Euro"
            }),
            await devise_crud.create(db, {
                "code": "USD",
                "nom": "Dollar US"
            })
        ]
        
        # 4. Création des pays
        pays = [
            await pays_crud.create(db, {
                "code": "FR",
                "nom": "France",
                "id_region": regions[0].id,
                "continent": "Europe",
                "id_devise": devises[0].id
            }),
            await pays_crud.create(db, {
                "code": "US",
                "nom": "États-Unis",
                "id_region": regions[1].id,
                "continent": "Amérique du Nord",
                "id_devise": devises[1].id
            })
        ]
        
        # 5. Création des secteurs
        secteurs = [
            await secteur_crud.create(db, {
                "code": "TECH",
                "nom": "Technologie",
                "code_gics": "45",
                "code_bics": "TECH"
            }),
            await secteur_crud.create(db, {
                "code": "FIN",
                "nom": "Finance",
                "code_gics": "40",
                "code_bics": "FIN"
            })
        ]
        
        # 6. Création des types d'actifs
        types_actifs = [
            await type_actif_crud.create(db, {
                "code": "EQ",
                "nom": "Actions",
                "type": "Equity"
            }),
            await type_actif_crud.create(db, {
                "code": "FI",
                "nom": "Obligations",
                "type": "Fixed Income"
            })
        ]
        
        # 7. Création des sous-types d'actifs
        sous_types_actifs = [
            await sous_type_actif_crud.create(db, {
                "code": "EQCOM",
                "nom": "Actions ordinaires",
                "id_type_actif": types_actifs[0].id
            }),
            await sous_type_actif_crud.create(db, {
                "code": "FIGOV",
                "nom": "Obligations gouvernementales",
                "id_type_actif": types_actifs[1].id
            })
        ]
        
        # 8. Création des classifications
        classifs = [
            await classif_crud.create(db, {
                "code": "STYLE",
                "nom": "Style d'investissement"
            }),
            await classif_crud.create(db, {
                "code": "CAP",
                "nom": "Capitalisation"
            })
        ]
        
        # 9. Création des sous-classifications
        sous_classifs = [
            await sous_classif_crud.create(db, {
                "code": "VALUE",
                "nom": "Value",
                "id_classif": classifs[0].id
            }),
            await sous_classif_crud.create(db, {
                "code": "LARGE",
                "nom": "Large Cap",
                "id_classif": classifs[1].id
            })
        ]
        
        # 10. Création des titres
        titres = [
            await titre_crud.create(db, {
                "code": "AAPL",
                "nom": "Apple Inc.",
                "cusip": "037833100",
                "isin": "US0378331005",
                "ticker": "AAPL",
                "emetteur": "Apple Inc.",
                "id_type_actif": types_actifs[0].id,
                "id_sous_type_actif": sous_types_actifs[0].id,
                "id_secteur": secteurs[0].id,
                "id_classif": classifs[1].id,
                "id_sous_classif": sous_classifs[1].id,
                "id_pays": pays[1].id
            }),
            await titre_crud.create(db, {
                "code": "BNP",
                "nom": "BNP Paribas",
                "cusip": "05565A202",
                "isin": "FR0000131104",
                "ticker": "BNP.PA",
                "emetteur": "BNP Paribas SA",
                "id_type_actif": types_actifs[0].id,
                "id_sous_type_actif": sous_types_actifs[0].id,
                "id_secteur": secteurs[1].id,
                "id_classif": classifs[0].id,
                "id_sous_classif": sous_classifs[0].id,
                "id_pays": pays[0].id
            })
        ]
        
        # 11. Création des indices
        indices = [
            await indice_crud.create(db, {
                "code": "SPX",
                "nom": "S&P 500"
            }),
            await indice_crud.create(db, {
                "code": "CAC",
                "nom": "CAC 40"
            })
        ]
        
        # 12. Création des fonds
        fonds = [
            await fonds_crud.create(db, {
                "code": "FUND1",
                "nom": "Fonds Actions Tech",
                "type_fonds": "simple"
            }),
            await fonds_crud.create(db, {
                "code": "PORT1",
                "nom": "Portefeuille Mixte",
                "type_fonds": "portefeuille"
            })
        ]
        
        # 13. Création des compositions
        today = date.today()
        
        # Composition du fonds simple
        await composition_fonds_crud.create(db, {
            "date": today,
            "id_fonds": fonds[0].id,
            "id_gestionnaire": gestionnaires[0].id,
            "id_titre": titres[0].id,
            "id_devise": devises[1].id,
            "id_pays": pays[1].id,
            "quantite": 1000,
            "prix": 150.0,
            "valeur_marchande": 150000.0,
            "accrued": 0.0,
            "dividende": 0.82
        })
        
        # Composition du portefeuille
        await composition_portefeuille_crud.create(db, {
            "date": today,
            "id_portefeuille": fonds[1].id,
            "id_gestionnaire": gestionnaires[1].id,
            "id_titre": titres[1].id,
            "id_devise": devises[0].id,
            "id_pays": pays[0].id,
            "quantite": 500,
            "prix": 55.0,
            "valeur_marchande": 27500.0,
            "accrued": 0.0,
            "dividende": 3.10
        })
        
        # Composition de l'indice
        await composition_indice_crud.create(db, {
            "date": today,
            "id_indice": indices[0].id,
            "id_titre": titres[0].id,
            "id_devise": devises[1].id,
            "id_pays": pays[1].id,
            "quantite": 1,
            "prix": 150.0,
            "valeur_marchande": 150.0,
            "dividende": 0.82
        })
        
        # 14. Création des liens gestionnaire-fonds
        # Lien Gestionnaire 1 -> Fonds 1
        db.execute(text("INSERT INTO gestionnaire_fonds (id_gestionnaire, id_fonds) VALUES (:id_gest, :id_fonds)"),
                   {"id_gest": gestionnaires[0].id, "id_fonds": fonds[0].id})
        
        # Lien Gestionnaire 2 -> Fonds 2
        db.execute(text("INSERT INTO gestionnaire_fonds (id_gestionnaire, id_fonds) VALUES (:id_gest, :id_fonds)"),
                   {"id_gest": gestionnaires[1].id, "id_fonds": fonds[1].id})
        
        db.commit() # S'assurer que les changements sont sauvegardés
        
        logger.info("Base de données peuplée avec succès")
        
    except Exception as e:
        logger.error(f"Erreur lors du peuplement de la base de données: {str(e)}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(populate_database()) 
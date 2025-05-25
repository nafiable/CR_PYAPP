from datetime import date
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete, insert
from schemas.CompositionIndice import CompositionIndice as CompositionIndiceSchema # Importer le modèle Pydantic
from sqlalchemy import Table, MetaData, Column, Integer, String, Float, Date

# Define the table for SQLAlchemy Core usage
metadata = MetaData()
composition_indice_table = Table('CompositionIndice', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('date', Date),
    Column('id_indice', Integer),
    Column('id_titre', Integer),
    Column('quantite', Float),
    Column('prix', Float),
    Column('valeur_marchande', Float),
    Column('dividende', Float)
)

def create_composition(connection: Any, composition_data: Dict[str, Any]) -> int | None:
    """
    Insère une nouvelle composition d'indice dans la base de données SQLite.

    Args:
        connection: L'objet connexion SQLite.
        composition_data: Un dictionnaire contenant les données de la composition
                          (doit contenir 'date', 'id_indice', 'id_titre', 'quantite',
                           'prix', 'valeur_marchande', 'dividende').

    Returns:
        L'ID de la ligne insérée si succès, sinon None.
    """
    try:
        # Ensure date is in the correct format if it's a string
        if isinstance(composition_data.get('date'), str):
 composition_data['date'] = date.fromisoformat(composition_data['date'])

        stmt = insert(composition_indice_table).values(**composition_data)
        with connection.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
            # Pour SQLite, lastrowid est l'ID de la dernière insertion
            return result.lastrowid
    except Exception as e:
        print(f"Erreur lors de l'insertion de la composition d'indice : {e}")
        return None

def get_composition(connection: Any, indice_id: int, date_comp: date) -> List[Dict[str, Any]]:
    """
    Récupère les compositions d'indice pour un indice et une date donnés.

    Args:
        connection: L'engine de connexion SQLAlchemy.
        indice_id: L'ID de l'indice.
        date_comp: La date de la composition.

    Returns:
        Une liste de dictionnaires représentant les compositions.
    """
    try:
        stmt = select(composition_indice_table).where(
            composition_indice_table.c.id_indice == indice_id,
            composition_indice_table.c.date == date_comp
        )
        with connection.connect() as conn:
            result = conn.execute(stmt)
            # Convertir les RowProxy en dictionnaires
            return [dict(row) for row in result.fetchall()]
    except Exception as e:
        print(f"Erreur lors de la récupération de la composition d'indice : {e}")
        return []

def update_composition(connection: Any, indice_id: int, date_comp: date, composition_data: Dict[str, Any]) -> int:
    """
    Met à jour les compositions d'indice pour un indice et une date donnés.

    Args:
        connection: L'engine de connexion SQLAlchemy.
        indice_id: L'ID de l'indice.
        date_comp: La date de la composition.
        composition_data: Un dictionnaire contenant les données à mettre à jour.
                         Ne doit pas contenir 'id', 'id_indice', 'date'.

    Returns:
        Le nombre de lignes affectées.
    """
    # Filtrer les données pour ne garder que les champs modifiables
    update_values = {}
    for key, value in composition_data.items():
        if key in ['quantite', 'prix', 'valeur_marchande', 'dividende']:
            update_values[key] = value

    if not update_values:
        return 0 # Aucune donnée à mettre à jour

    try:
        stmt = update(composition_indice_table).where(
            composition_indice_table.c.id_indice == indice_id,
            composition_indice_table.c.date == date_comp
        ).values(**update_values)
        with connection.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
            return result.rowcount
    except Exception as e:
        print(f"Erreur lors de la mise à jour de la composition d'indice : {e}")
        return 0

def delete_composition(connection: Any, indice_id: int, date_comp: date) -> int:
    """
    Supprime les compositions d'indice pour un indice et une date donnés.

    Args:
        connection: L'engine de connexion SQLAlchemy.
        indice_id: L'ID de l'indice.
        date_comp: La date de la composition.

    Returns:
        Le nombre de lignes supprimées.
    """
    try:
        stmt = delete(composition_indice_table).where(
            composition_indice_table.c.id_indice == indice_id,
            composition_indice_table.c.date == date_comp
        )
        with connection.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
            return result.rowcount
    except Exception as e:
        print(f"Erreur lors de la suppression de la composition d'indice : {e}")
        return 0
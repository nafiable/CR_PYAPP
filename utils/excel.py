# -*- coding: utf-8 -*-

import pandas as pd
import logging

logger = logging.getLogger(__name__)
import openpyxl
from openpyxl.utils import get_column_letter

class ExcelUtils:
    """
    Classe utilitaire pour gérer les opérations sur les fichiers Excel.
    """

    def load_excel_to_dataframe(self, filepath, sheet_name=0):
        """
        Charge une feuille spécifique d'un fichier Excel dans un DataFrame pandas.

        Args:
            filepath (str): Le chemin du fichier Excel.
            sheet_name (str ou int, optionnel): Le nom ou l'index de la feuille à charger. Par défaut, la première feuille (0).

        Returns:
            pandas.DataFrame: Le DataFrame contenant les données de la feuille.
        """
        try:
            df = pd.read_excel(filepath, sheet_name=sheet_name)
            return df
        except FileNotFoundError:
            logger.error(f"Erreur : Le fichier Excel '{filepath}' est introuvable.")
            return None
        except Exception as e:
            logger.error(f"Erreur lors du chargement du fichier Excel '{filepath}': {e}")
            return None

    def write_dataframe_to_excel(self, dataframe, filepath, sheet_name='Sheet1', startrow=None, startcol=None):
        """
        Écrit un DataFrame pandas dans un fichier Excel.
        Si le fichier existe, le DataFrame est écrit dans la feuille spécifiée.
        Si la feuille n'existe pas, elle est créée.

        Args:
            dataframe (pandas.DataFrame): Le DataFrame à écrire.
            filepath (str): Le chemin du fichier Excel de destination.
            sheet_name (str, optionnel): Le nom de la feuille où écrire. Par défaut 'Sheet1'.
            startrow (int, optionnel): La ligne de départ pour l'écriture. Par défaut, le début de la feuille.
            startcol (int, optionnel): La colonne de départ pour l'écriture. Par défaut, le début de la feuille.
        """
        try:
            with pd.ExcelWriter(filepath, engine='openpyxl', mode='a' if pd.io.excel.ExcelFile(filepath).book else 'w') as writer:
                 dataframe.to_excel(writer, sheet_name=sheet_name, index=False, startrow=startrow, startcol=startcol)
        except FileNotFoundError:
             with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                 dataframe.to_excel(writer, sheet_name=sheet_name, index=False, startrow=startrow, startcol=startcol)
        except Exception as e:
            logger.error(f"Erreur lors de l'écriture du DataFrame dans le fichier Excel '{filepath}': {e}")

    def write_to_excel_cell(self, filepath, sheet_name, row, col, value):
        """
        Écrit une valeur dans une cellule spécifique d'un fichier Excel.

        Args:
            filepath (str): Le chemin du fichier Excel.
            sheet_name (str): Le nom de la feuille.
            row (int): Le numéro de la ligne (base 1).
            col (int): Le numéro de la colonne (base 1).
            value: La valeur à écrire.
        """
        try:
            workbook = openpyxl.load_workbook(filepath)
            if sheet_name not in workbook.sheetnames:
                workbook.create_sheet(sheet_name)
            sheet = workbook[sheet_name]
            sheet.cell(row=row, column=col, value=value)
            workbook.save(filepath)
        except FileNotFoundError:
            logger.error(f"Erreur : Le fichier Excel '{filepath}' est introuvable.")
        except Exception as e:
            logger.error(f"Erreur lors de l'écriture dans la cellule ({row}, {col}) de la feuille '{sheet_name}': {e}")

    # NOTE: Les fonctions clear_excel_sheet et clear_excel_range nécessitent une implémentation plus complexe
    # impliquant la suppression du contenu des cellules. Cela sera ajouté ultérieurement si nécessaire.

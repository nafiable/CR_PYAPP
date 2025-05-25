# -*- coding: utf-8 -*-

import csv
import pandas as pd

class CSVUtils:
    """
    Classe utilitaire pour les opérations sur les fichiers CSV.
    """

    @staticmethod
    def load_csv_to_dict(filepath: str) -> list[dict]:
        """
        Charge un fichier CSV et retourne une liste de dictionnaires.

        Args:
            filepath (str): Chemin du fichier CSV.

        Returns:
            list[dict]: Liste de dictionnaires représentant les lignes du CSV.
        """
        data = []
        with open(filepath, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
        return data

    @staticmethod
    def load_csv_to_dataframe(filepath: str) -> pd.DataFrame:
        """
        Charge un fichier CSV et retourne un DataFrame pandas.

        Args:
            filepath (str): Chemin du fichier CSV.

        Returns:
            pd.DataFrame: DataFrame pandas représentant le CSV.
        """
        return pd.read_csv(filepath)

    @staticmethod
    def write_dict_to_csv(data: list[dict], filepath: str):
        """
        Écrit une liste de dictionnaires dans un fichier CSV.

        Args:
            data (list[dict]): Liste de dictionnaires à écrire.
            filepath (str): Chemin du fichier CSV de sortie.
        """
        if not data:
            return # Ne rien faire si les données sont vides
        keys = data[0].keys()
        with open(filepath, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)

    @staticmethod
s.write_dataframe_to_csv(dataframe: pd.DataFrame, filepath: str):
        """
        Écrit un DataFrame pandas dans un fichier CSV.

        Args:
            dataframe (pd.DataFrame): DataFrame à écrire.
            filepath (str): Chemin du fichier CSV de sortie.
        """
        dataframe.to_csv(filepath, index=False)

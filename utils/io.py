# -*- coding: utf-8 -*-

import gzip
import zipfile
import os

class IOUtils:
    """
    Classe utilitaire pour les opérations générales d'entrée/sortie.
    Gère la lecture/écriture de fichiers texte et la compression/décompression.
    """

    @staticmethod
    def read_text_file(filepath: str) -> str:
        """
        Lit le contenu d'un fichier texte.

        Args:
            filepath (str): Chemin complet du fichier texte.

        Returns:
            str: Contenu du fichier.
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()

    @staticmethod
    def write_text_file(filepath: str, content: str):
        """
        Écrit du contenu dans un fichier texte.

        Args:
            filepath (str): Chemin complet du fichier texte.
            content (str): Contenu à écrire dans le fichier.
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    @staticmethod
    def compress_file(filepath: str, output_filepath: str):
        """
        Compresse un fichier en utilisant gzip.

        Args:
            filepath (str): Chemin du fichier à compresser.
            output_filepath (str): Chemin où enregistrer le fichier compressé (.gz).
        """
        with open(filepath, 'rb') as f_in:
            with gzip.open(output_filepath, 'wb') as f_out:
                f_out.writelines(f_in)

    @staticmethod
    def decompress_file(filepath: str, output_filepath: str):
        """
        Décompresse un fichier gzip.

        Args:
            filepath (str): Chemin du fichier compressé (.gz).
            output_filepath (str): Chemin où enregistrer le fichier décompressé.
        """
        with gzip.open(filepath, 'rb') as f_in:
            with open(output_filepath, 'wb') as f_out:
                f_out.writelines(f_in)

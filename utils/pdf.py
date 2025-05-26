# -*- coding: utf-8 -*-

import PyPDF2
from reportlab.pdfgen import canvas
import logging

logger = logging.getLogger(__name__)
from reportlab.lib.pagesizes import letter
import io

class PDFUtils:
    """
    Classe utilitaire pour les opérations sur les fichiers PDF.
    """

    def read_pdf(self, filepath: str) -> list[str]:
        """
        Lit un fichier PDF et retourne le texte de chaque page sous forme de liste de chaînes de caractères.

        Args:
            filepath: Chemin vers le fichier PDF.

        Returns:
            Une liste de chaînes de caractères, où chaque chaîne représente le texte d'une page.
        """
        text_by_page = []
 logger.info(f"Reading PDF file: {filepath}")
 try:
            with open(filepath, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
 logger.info(f"Number of pages in {filepath}: {len(reader.pages)}")
                for page_num in range(len(reader.pages)):
 logger.debug(f"Extracting text from page {page_num + 1}")
                    text_by_page.append(reader.pages[page_num].extract_text())
 logger.info(f"Successfully read PDF file: {filepath}")
 return text_by_page
 except FileNotFoundError:
 logger.error(f"PDF file not found: {filepath}")
 return []
 except Exception as e:
 logger.error(f"Error reading PDF file {filepath}: {e}", exc_info=True)
 return []

    def generate_pdf_from_text(self, text: str, filepath: str):
        """
        Génère un fichier PDF simple à partir d'une chaîne de texte.
        Args:
            text: La chaîne de texte à inclure dans le PDF.
            filepath: Chemin où sauvegarder le fichier PDF généré.
        """
 logger.info(f"Generating PDF from text to file: {filepath}")
        c = canvas.Canvas(filepath, pagesize=letter)
        c.drawString(100, 750, text) # Dessine le texte à une position spécifique
        c.save()

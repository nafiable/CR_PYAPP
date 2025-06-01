"""
Module pour la gestion des opérations PDF (lecture, création, export).
"""

import os
from datetime import datetime
import PyPDF2
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm, mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak, Flowable
from reportlab.graphics.shapes import Circle, Rect, Drawing
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
import pandas as pd
from typing import List, Dict, Optional, Union, Tuple
import fitz  # PyMuPDF pour des fonctionnalités avancées
from PIL import Image as PILImage
import io

class PDFReader:
    """Classe pour la lecture et l'analyse de fichiers PDF."""
    
    @staticmethod
    def extraire_texte(chemin_pdf):
        """Extrait tout le texte d'un fichier PDF."""
        with open(chemin_pdf, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            texte = ""
            for page in reader.pages:
                texte += page.extract_text()
        return texte
    
    @staticmethod
    def extraire_texte_par_page(chemin_pdf):
        """Extrait le texte page par page."""
        with open(chemin_pdf, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            textes = []
            for page in reader.pages:
                textes.append(page.extract_text())
        return textes
    
    @staticmethod
    def extraire_metadata(chemin_pdf):
        """Extrait les métadonnées du PDF."""
        with open(chemin_pdf, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            return reader.metadata
    
    @staticmethod
    def fusionner_pdfs(chemins_pdf, chemin_sortie):
        """Fusionne plusieurs PDF en un seul."""
        merger = PyPDF2.PdfMerger()
        for pdf in chemins_pdf:
            merger.append(pdf)
        merger.write(chemin_sortie)
        merger.close()
    
    @staticmethod
    def extraire_images(chemin_pdf, dossier_sortie: str) -> List[str]:
        """Extrait toutes les images d'un PDF.
        
        Args:
            chemin_pdf: Chemin du fichier PDF
            dossier_sortie: Dossier où sauvegarder les images
        
        Returns:
            Liste des chemins des images extraites
        """
        if not os.path.exists(dossier_sortie):
            os.makedirs(dossier_sortie)
        
        images_extraites = []
        doc = fitz.open(chemin_pdf)
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            images = page.get_images(full=True)
            
            for img_index, img in enumerate(images):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                
                # Déterminer l'extension
                ext = base_image["ext"]
                image_path = os.path.join(
                    dossier_sortie,
                    f"page{page_num+1}_img{img_index+1}.{ext}"
                )
                
                with open(image_path, "wb") as image_file:
                    image_file.write(image_bytes)
                images_extraites.append(image_path)
        
        return images_extraites
    
    @staticmethod
    def extraire_tableaux(chemin_pdf) -> List[pd.DataFrame]:
        """Extrait les tableaux d'un PDF.
        
        Args:
            chemin_pdf: Chemin du fichier PDF
        
        Returns:
            Liste des tableaux extraits sous forme de DataFrames
        """
        # Note: Cette fonction utilise PyMuPDF pour détecter les tableaux
        # Une implémentation plus robuste pourrait utiliser Camelot ou Tabula
        tableaux = []
        doc = fitz.open(chemin_pdf)
        
        for page in doc:
            # Recherche des tableaux dans la page
            tables = page.find_tables()
            for table in tables:
                # Conversion en DataFrame
                df = pd.DataFrame(table.extract())
                tableaux.append(df)
        
        return tableaux
    
    @staticmethod
    def compresser_pdf(chemin_entree: str, chemin_sortie: str, niveau: str = 'normal'):
        """Compresse un fichier PDF.
        
        Args:
            chemin_entree: Chemin du fichier PDF d'entrée
            chemin_sortie: Chemin du fichier PDF compressé
            niveau: Niveau de compression ('minimal', 'normal', 'agressif')
        """
        doc = fitz.open(chemin_entree)
        
        if niveau == 'minimal':
            doc.save(chemin_sortie, garbage=1, deflate=True)
        elif niveau == 'normal':
            doc.save(chemin_sortie, garbage=3, deflate=True, clean=True)
        else:  # agressif
            doc.save(chemin_sortie, garbage=4, deflate=True, clean=True, pretty=False)

class PDFWriter:
    """Classe pour la création et l'export de PDF."""
    
    def __init__(self, chemin_sortie=None, orientation='portrait'):
        """Initialise le générateur de PDF."""
        self.styles = getSampleStyleSheet()
        if chemin_sortie:
            pagesize = A4 if orientation == 'portrait' else landscape(A4)
            self.doc = SimpleDocTemplate(
                chemin_sortie,
                pagesize=pagesize,
                rightMargin=30,
                leftMargin=30,
                topMargin=30,
                bottomMargin=30
            )
    
    def creer_style_titre(self, taille=16, espacement=30, couleur=colors.black):
        """Crée un style personnalisé pour les titres."""
        return ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=taille,
            spaceAfter=espacement,
            textColor=couleur
        )
    
    def creer_graphique_ligne(
        self,
        donnees: List[List[float]],
        labels: List[str],
        titre: str,
        largeur: int = 400,
        hauteur: int = 200
    ) -> Drawing:
        """Crée un graphique en ligne.
        
        Args:
            donnees: Liste des séries de données
            labels: Labels pour la légende
            titre: Titre du graphique
            largeur: Largeur du graphique
            hauteur: Hauteur du graphique
        """
        dessin = Drawing(largeur, hauteur)
        graphique = HorizontalLineChart()
        graphique.x = 50
        graphique.y = 50
        graphique.height = hauteur - 75
        graphique.width = largeur - 100
        
        graphique.data = donnees
        graphique.categoryAxis.categoryNames = labels
        graphique.valueAxis.valueMin = min(min(d) for d in donnees)
        graphique.valueAxis.valueMax = max(max(d) for d in donnees)
        
        dessin.add(graphique)
        return dessin
    
    def creer_graphique_barres(
        self,
        donnees: List[float],
        categories: List[str],
        titre: str,
        largeur: int = 400,
        hauteur: int = 200
    ) -> Drawing:
        """Crée un graphique en barres."""
        dessin = Drawing(largeur, hauteur)
        graphique = VerticalBarChart()
        graphique.x = 50
        graphique.y = 50
        graphique.height = hauteur - 75
        graphique.width = largeur - 100
        
        graphique.data = [donnees]
        graphique.categoryAxis.categoryNames = categories
        
        dessin.add(graphique)
        return dessin
    
    def creer_graphique_camembert(
        self,
        donnees: List[float],
        labels: List[str],
        titre: str,
        largeur: int = 300,
        hauteur: int = 300
    ) -> Drawing:
        """Crée un graphique en camembert."""
        dessin = Drawing(largeur, hauteur)
        graphique = Pie()
        graphique.x = largeur // 2
        graphique.y = hauteur // 2
        graphique.width = min(largeur, hauteur) - 100
        graphique.height = graphique.width
        graphique.data = donnees
        graphique.labels = labels
        
        dessin.add(graphique)
        return dessin
    
    def ajouter_filigrane(self, texte: str, angle: int = 45, couleur=colors.grey):
        """Crée un filigrane pour le PDF."""
        class Filigrane(Flowable):
            def __init__(self, texte, angle, couleur):
                Flowable.__init__(self)
                self.texte = texte
                self.angle = angle
                self.couleur = couleur
            
            def draw(self):
                canvas = self.canv
                canvas.saveState()
                canvas.translate(A4[0]/2, A4[1]/2)
                canvas.rotate(self.angle)
                canvas.setFont("Helvetica", 120)
                canvas.setFillColor(self.couleur)
                canvas.setFillAlpha(0.3)
                canvas.drawCentredString(0, 0, self.texte)
                canvas.restoreState()
        
        return Filigrane(texte, angle, couleur)
    
    def ajouter_signature(self, image_signature: str, position: Tuple[float, float]):
        """Ajoute une signature au PDF."""
        class Signature(Flowable):
            def __init__(self, image_path, position):
                Flowable.__init__(self)
                self.image_path = image_path
                self.position = position
            
            def draw(self):
                canvas = self.canv
                canvas.saveState()
                canvas.drawImage(
                    self.image_path,
                    self.position[0],
                    self.position[1],
                    width=100,
                    height=50,
                    mask='auto'
                )
                canvas.restoreState()
        
        return Signature(image_signature, position)

    def dataframe_vers_tableau(self, df: pd.DataFrame, largeurs_colonnes: Optional[List[float]] = None) -> Table:
        """Convertit un DataFrame en tableau ReportLab.
        
        Args:
            df: DataFrame à convertir
            largeurs_colonnes: Liste des largeurs pour chaque colonne (en cm)
        
        Returns:
            Table: Tableau ReportLab formaté
        """
        # En-têtes
        data = [df.columns.tolist()]
        # Données
        data.extend(df.values.tolist())
        
        # Largeurs par défaut si non spécifiées
        if not largeurs_colonnes:
            largeurs_colonnes = [2*cm] * len(df.columns)
        
        # Création du tableau
        table = Table(data, colWidths=largeurs_colonnes)
        
        # Style du tableau
        style = TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.lightgrey]),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
        ])
        table.setStyle(style)
        
        return table

    def exporter_dataframe(
        self,
        df: pd.DataFrame,
        titre: Optional[str] = None,
        description: Optional[str] = None,
        chemin_sortie: Optional[str] = None,
        largeurs_colonnes: Optional[List[float]] = None
    ):
        """Exporte un DataFrame en PDF.
        
        Args:
            df: DataFrame à exporter
            titre: Titre du document
            description: Description ou commentaires
            chemin_sortie: Chemin du fichier PDF de sortie
            largeurs_colonnes: Liste des largeurs pour chaque colonne (en cm)
        """
        if chemin_sortie:
            self.doc = SimpleDocTemplate(
                chemin_sortie,
                pagesize=A4,
                rightMargin=30,
                leftMargin=30,
                topMargin=30,
                bottomMargin=30
            )
        
        elements = []
        
        # Ajout du titre
        if titre:
            elements.append(Paragraph(titre, self.creer_style_titre()))
            elements.append(Spacer(1, 12))
        
        # Ajout de la description
        if description:
            elements.append(Paragraph(description, self.styles['Normal']))
            elements.append(Spacer(1, 12))
        
        # Ajout de la date
        date_str = datetime.now().strftime("%d/%m/%Y %H:%M")
        elements.append(Paragraph(f"Généré le : {date_str}", self.styles['Normal']))
        elements.append(Spacer(1, 20))
        
        # Ajout du tableau
        elements.append(self.dataframe_vers_tableau(df, largeurs_colonnes))
        
        # Génération du PDF
        self.doc.build(elements)

class RapportPDF(PDFWriter):
    """Classe spécialisée pour la génération de rapports PDF."""
    
    def __init__(self, titre_rapport, chemin_sortie, orientation='portrait'):
        """Initialise le générateur de rapport."""
        super().__init__(chemin_sortie, orientation)
        self.titre_rapport = titre_rapport
        self.elements = []
        
        # Ajout du titre principal
        self.elements.append(Paragraph(titre_rapport, self.creer_style_titre()))
        self.elements.append(Spacer(1, 20))
    
    def ajouter_section(
        self,
        titre: str,
        contenu: Optional[str] = None,
        dataframe: Optional[pd.DataFrame] = None,
        graphique: Optional[str] = None,
        nouvelle_page: bool = False
    ):
        """Ajoute une nouvelle section au rapport."""
        if nouvelle_page:
            self.elements.append(PageBreak())
        
        # Titre de section
        self.elements.append(Paragraph(titre, self.styles['Heading2']))
        self.elements.append(Spacer(1, 12))
        
        # Contenu textuel
        if contenu:
            self.elements.append(Paragraph(contenu, self.styles['Normal']))
            self.elements.append(Spacer(1, 12))
        
        # DataFrame
        if dataframe is not None:
            self.elements.append(self.dataframe_vers_tableau(dataframe))
            self.elements.append(Spacer(1, 12))
        
        # Graphique
        if graphique:
            self.elements.append(self.ajouter_graphique(graphique))
            self.elements.append(Spacer(1, 12))
    
    def ajouter_table_des_matieres(self):
        """Ajoute une table des matières au rapport."""
        toc = []
        for element in self.elements:
            if isinstance(element, Paragraph) and element.style.name.startswith('Heading'):
                niveau = int(element.style.name[-1])
                toc.append((niveau, element.text))
        
        self.elements.insert(1, Paragraph("Table des matières", self.styles['Heading1']))
        for niveau, texte in toc:
            style = ParagraphStyle(
                'TOC_Level' + str(niveau),
                parent=self.styles['Normal'],
                leftIndent=20 * (niveau - 1)
            )
            self.elements.insert(2, Paragraph(texte, style))
        self.elements.insert(len(toc) + 3, PageBreak())
    
    def generer(self, filigrane: Optional[str] = None):
        """Génère le rapport final."""
        if filigrane:
            self.elements.insert(0, self.ajouter_filigrane(filigrane))
        self.doc.build(self.elements)

def exemple_utilisation():
    """Exemple d'utilisation des fonctionnalités PDF."""
    # Lecture d'un PDF
    reader = PDFReader()
    texte = reader.extraire_texte("exemple.pdf")
    print("Texte extrait:", texte[:100])
    
    # Création d'un rapport
    rapport = RapportPDF("Rapport d'Analyse", "rapport.pdf")
    
    # Ajout d'une section avec DataFrame
    df = pd.DataFrame({
        'A': range(1, 6),
        'B': ['a', 'b', 'c', 'd', 'e']
    })
    rapport.ajouter_section(
        "Section 1",
        "Cette section contient un tableau de données.",
        dataframe=df
    )
    
    # Ajout d'un graphique
    donnees = [[1, 2, 3, 4, 5], [2, 3, 4, 5, 6]]
    labels = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai']
    graphique = rapport.creer_graphique_ligne(donnees, labels, "Évolution mensuelle")
    rapport.elements.append(graphique)
    
    # Génération du rapport avec filigrane
    rapport.generer(filigrane="CONFIDENTIEL")

if __name__ == "__main__":
    exemple_utilisation()

"""
Module pour générer des rapports PDF avec des indicateurs visuels et envoi par courriel.
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from datetime import datetime
import matplotlib.pyplot as plt
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.graphics.shapes import Circle, Rect, Drawing
from reportlab.graphics.renderPDF import draw
import pandas as pd
import numpy as np
from sqlalchemy import text
from database.connexionsqlLiter import SQLiteConnection
import seaborn as sns

class IndicateurVisuel:
    """Classe pour gérer les indicateurs visuels."""
    
    @staticmethod
    def creer_cercle(couleur, taille=8):
        """Crée un cercle de couleur."""
        d = Drawing(taille, taille)
        d.add(Circle(taille/2, taille/2, taille/2, fillColor=couleur))
        return d
    
    @staticmethod
    def creer_carre(couleur, taille=8):
        """Crée un carré de couleur."""
        d = Drawing(taille, taille)
        d.add(Rect(0, 0, taille, taille, fillColor=couleur))
        return d

class EmailSender:
    """Classe pour gérer l'envoi des courriels."""
    
    def __init__(self, smtp_server="smtp.gmail.com", smtp_port=587):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
    
    def envoyer_rapport(self, expediteur, mot_de_passe, destinataires, sujet, corps, fichier_pdf):
        """Envoie le rapport par courriel."""
        # Création du message
        message = MIMEMultipart()
        message["From"] = expediteur
        message["To"] = ", ".join(destinataires)
        message["Subject"] = sujet
        
        # Ajout du corps du message
        message.attach(MIMEText(corps, "plain"))
        
        # Ajout de la pièce jointe PDF
        with open(fichier_pdf, "rb") as f:
            pdf = MIMEApplication(f.read(), _subtype="pdf")
            pdf.add_header(
                "Content-Disposition",
                "attachment",
                filename=os.path.basename(fichier_pdf)
            )
            message.attach(pdf)
        
        # Connexion et envoi
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(expediteur, mot_de_passe)
            server.send_message(message)

class RapportGenerator:
    """Classe pour générer des rapports PDF."""
    
    def __init__(self):
        """Initialise le générateur de rapports."""
        self.styles = getSampleStyleSheet()
        self.couleurs = {
            'danger': colors.red,
            'warning': colors.orange,
            'success': colors.green,
            'info': colors.blue
        }
        
        # Création des dossiers nécessaires
        self.rapport_dir = os.path.join(os.path.dirname(__file__), '..', 'rapports')
        self.graph_dir = os.path.join(self.rapport_dir, 'graphiques')
        for directory in [self.rapport_dir, self.graph_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)
    
    def _evaluer_seuils(self, prix, seuils):
        """Évalue le prix par rapport aux seuils et retourne l'indicateur approprié."""
        if prix >= seuils['danger']:
            return self.couleurs['danger'], "Prix critique - Surveillance requise"
        elif prix >= seuils['warning']:
            return self.couleurs['warning'], "Prix élevé - Attention"
        elif prix >= seuils['info']:
            return self.couleurs['info'], "Prix à surveiller"
        else:
            return self.couleurs['success'], "Prix normal"
    
    def _generer_graphiques(self, df):
        """Génère les graphiques pour le rapport."""
        graphiques = []
        
        # Graphique 1: Distribution des prix par fonds
        plt.figure(figsize=(10, 6))
        df.boxplot(column='prix', by='code_fonds')
        plt.title('Distribution des Prix par Fonds')
        plt.ylabel('Prix (€)')
        plt.xticks(rotation=45)
        graph_path = os.path.join(self.graph_dir, 'distribution_prix.png')
        plt.savefig(graph_path, bbox_inches='tight')
        plt.close()
        graphiques.append(graph_path)
        
        # Graphique 2: Nombre de titres par niveau de prix
        plt.figure(figsize=(10, 6))
        df['niveau_prix'] = pd.cut(df['prix'], 
                                 bins=[0, 200, 500, 1000, float('inf')],
                                 labels=['Normal', 'À surveiller', 'Élevé', 'Critique'])
        df['niveau_prix'].value_counts().plot(kind='bar')
        plt.title('Répartition des Titres par Niveau de Prix')
        plt.ylabel('Nombre de Titres')
        plt.xlabel('Niveau de Prix')
        graph_path = os.path.join(self.graph_dir, 'repartition_niveaux.png')
        plt.savefig(graph_path, bbox_inches='tight')
        plt.close()
        graphiques.append(graph_path)
        
        return graphiques
    
    def _generer_statistiques(self, df):
        """Génère les statistiques descriptives."""
        stats = []
        
        # Statistiques globales
        stats.append(Paragraph("Statistiques Globales", self.styles['Heading2']))
        stats.append(Spacer(1, 12))
        
        stats_glob = {
            "Nombre total de titres": len(df),
            "Prix moyen": f"{df['prix'].mean():.2f} €",
            "Prix médian": f"{df['prix'].median():.2f} €",
            "Prix minimum": f"{df['prix'].min():.2f} €",
            "Prix maximum": f"{df['prix'].max():.2f} €"
        }
        
        data = [[k, v] for k, v in stats_glob.items()]
        t = Table(data, colWidths=[4*cm, 4*cm])
        t.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ]))
        stats.append(t)
        stats.append(Spacer(1, 20))
        
        return stats
    
    def _generer_graphiques_historiques(self, conn):
        """Génère les graphiques d'analyse historique."""
        graphiques = []
        
        # Requête pour obtenir l'historique des prix
        query = text("""
            WITH HistoriquePrix AS (
                SELECT 
                    cf.date,
                    f.code as code_fonds,
                    t.code as code_titre,
                    cf.prix,
                    cf.valeur_marchande,
                    LAG(cf.prix) OVER (PARTITION BY f.code, t.code ORDER BY cf.date) as prix_precedent
                FROM composition_fonds cf
                JOIN fonds f ON cf.id_fonds = f.id
                JOIN titre t ON cf.id_titre = t.id
                ORDER BY cf.date
            )
            SELECT 
                date,
                code_fonds,
                code_titre,
                prix,
                valeur_marchande,
                CASE 
                    WHEN prix_precedent IS NOT NULL 
                    THEN ((prix - prix_precedent) / prix_precedent) * 100 
                    ELSE 0 
                END as variation_pct
            FROM HistoriquePrix
        """)
        
        df_historique = pd.read_sql(query, conn)
        
        # Graphique 1: Évolution des prix moyens par fonds
        plt.figure(figsize=(12, 6))
        for fonds in df_historique['code_fonds'].unique():
            data = df_historique[df_historique['code_fonds'] == fonds]
            prix_moyen = data.groupby('date')['prix'].mean()
            plt.plot(prix_moyen.index, prix_moyen.values, label=fonds, marker='o')
        
        plt.title('Évolution des Prix Moyens par Fonds')
        plt.xlabel('Date')
        plt.ylabel('Prix Moyen (€)')
        plt.legend(title='Fonds')
        plt.grid(True)
        plt.xticks(rotation=45)
        
        graph_path = os.path.join(self.graph_dir, 'evolution_prix_moyens.png')
        plt.savefig(graph_path, bbox_inches='tight')
        plt.close()
        graphiques.append(graph_path)
        
        # Graphique 2: Heatmap des variations de prix
        plt.figure(figsize=(12, 8))
        pivot_variations = df_historique.pivot_table(
            values='variation_pct',
            index='date',
            columns='code_fonds',
            aggfunc='mean'
        )
        
        sns.heatmap(pivot_variations, cmap='RdYlGn', center=0,
                    annot=True, fmt='.1f', cbar_kws={'label': 'Variation (%)'})
        plt.title('Heatmap des Variations de Prix par Fonds')
        plt.xlabel('Fonds')
        plt.ylabel('Date')
        
        graph_path = os.path.join(self.graph_dir, 'heatmap_variations.png')
        plt.savefig(graph_path, bbox_inches='tight')
        plt.close()
        graphiques.append(graph_path)
        
        # Graphique 3: Distribution des variations de prix
        plt.figure(figsize=(10, 6))
        for fonds in df_historique['code_fonds'].unique():
            data = df_historique[df_historique['code_fonds'] == fonds]['variation_pct']
            sns.kdeplot(data=data, label=fonds)
        
        plt.title('Distribution des Variations de Prix par Fonds')
        plt.xlabel('Variation (%)')
        plt.ylabel('Densité')
        plt.legend(title='Fonds')
        plt.grid(True)
        
        graph_path = os.path.join(self.graph_dir, 'distribution_variations.png')
        plt.savefig(graph_path, bbox_inches='tight')
        plt.close()
        graphiques.append(graph_path)
        
        return graphiques, df_historique
    
    def _generer_statistiques_historiques(self, df_historique):
        """Génère les statistiques historiques."""
        stats = []
        
        # Statistiques de variation
        stats.append(Paragraph("Analyse Historique des Variations", self.styles['Heading2']))
        stats.append(Spacer(1, 12))
        
        # Calcul des statistiques par fonds
        stats_hist = []
        for fonds in df_historique['code_fonds'].unique():
            data = df_historique[df_historique['code_fonds'] == fonds]
            variations = data['variation_pct']
            
            stats_hist.append([
                fonds,
                f"{variations.mean():.2f}%",
                f"{variations.std():.2f}%",
                f"{variations.min():.2f}%",
                f"{variations.max():.2f}%"
            ])
        
        # Création du tableau de statistiques
        headers = ['Fonds', 'Var. Moyenne', 'Volatilité', 'Var. Min', 'Var. Max']
        data = [headers] + stats_hist
        
        t = Table(data, colWidths=[3*cm, 3*cm, 3*cm, 3*cm, 3*cm])
        t.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ]))
        
        stats.append(t)
        stats.append(Spacer(1, 20))
        
        return stats
    
    def generer_rapport_prix(self, seuils=None):
        """Génère un rapport PDF avec analyse des prix."""
        if seuils is None:
            seuils = {
                'danger': 1000,    # Prix critique
                'warning': 500,    # Prix élevé
                'info': 200        # Prix à surveiller
            }
        
        # Connexion à la base de données
        db = SQLiteConnection()
        
        with db.engine.connect() as conn:
            # Requête pour obtenir les prix des titres par fonds
            query = text("""
                SELECT 
                    f.code as code_fonds,
                    f.nom as nom_fonds,
                    t.code as code_titre,
                    t.nom as nom_titre,
                    cf.prix,
                    cf.date
                FROM composition_fonds cf
                JOIN fonds f ON cf.id_fonds = f.id
                JOIN titre t ON cf.id_titre = t.id
                WHERE cf.date = (SELECT MAX(date) FROM composition_fonds)
                ORDER BY f.code, cf.prix DESC
            """)
            
            df = pd.read_sql(query, conn)
        
            # Génération des graphiques
            graphiques = self._generer_graphiques(df)
            
            # Ajout des graphiques et statistiques historiques
            graphiques_hist, df_historique = self._generer_graphiques_historiques(conn)
            graphiques.extend(graphiques_hist)
            
            # Export Excel
            excel_path = os.path.join(self.rapport_dir, f'analyse_prix_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx')
            df.to_excel(excel_path, index=False)
            
            # Création du PDF
            date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            pdf_path = os.path.join(self.rapport_dir, f'rapport_prix_{date_str}.pdf')
            doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
            
            # Contenu du rapport
            elements = []
            
            # Titre
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=self.styles['Heading1'],
                fontSize=16,
                spaceAfter=30
            )
            elements.append(Paragraph("Rapport d'Analyse des Prix des Titres", title_style))
            elements.append(Paragraph(f"Date du rapport : {datetime.now().strftime('%d/%m/%Y %H:%M')}", self.styles['Normal']))
            elements.append(Spacer(1, 20))
            
            # Ajout des statistiques
            elements.extend(self._generer_statistiques(df))
            
            # Ajout des statistiques historiques au rapport
            elements.extend(self._generer_statistiques_historiques(df_historique))
            
            # Ajout des graphiques
            for graph_path in graphiques:
                elements.append(Paragraph("", self.styles['Heading2']))
                elements.append(Image(graph_path, width=450, height=300))
                elements.append(Spacer(1, 20))
            
            # Création du tableau
            data = []
            # En-têtes
            headers = ['Fonds', 'Titre', 'Prix', 'Indicateur', 'Commentaire']
            data.append(headers)
            
            # Données
            current_fonds = None
            for _, row in df.iterrows():
                if current_fonds != row['code_fonds']:
                    if current_fonds is not None:
                        data.append([''] * 5)
                    current_fonds = row['code_fonds']
                
                couleur, commentaire = self._evaluer_seuils(row['prix'], seuils)
                
                indicateur = IndicateurVisuel.creer_carre(couleur) if row['prix'] >= seuils['danger'] else IndicateurVisuel.creer_cercle(couleur)
                
                data.append([
                    f"{row['code_fonds']} - {row['nom_fonds']}",
                    f"{row['code_titre']} - {row['nom_titre']}",
                    f"{row['prix']:.2f} €",
                    indicateur,
                    commentaire
                ])
            
            # Style du tableau
            table_style = TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.lightgrey]),
                ('ALIGN', (2, 1), (2, -1), 'RIGHT'),
                ('ALIGN', (3, 0), (3, -1), 'CENTER'),
            ])
            
            table = Table(data, colWidths=[4*cm, 4*cm, 2*cm, 1.5*cm, 7*cm])
            table.setStyle(table_style)
            
            elements.append(table)
            
            # Génération du PDF
            doc.build(elements)
            
            return pdf_path, excel_path, graphiques

def generer_et_envoyer_rapport(expediteur=None, mot_de_passe=None, destinataires=None, seuils=None):
    """Fonction utilitaire pour générer et envoyer un rapport."""
    # Génération du rapport
    generator = RapportGenerator()
    pdf_path, excel_path, _ = generator.generer_rapport_prix(seuils)
    
    # Envoi par courriel si les informations sont fournies
    if all([expediteur, mot_de_passe, destinataires]):
        sender = EmailSender()
        sujet = "Rapport d'Analyse des Prix des Titres"
        corps = f"""
        Bonjour,
        
        Veuillez trouver ci-joint le rapport d'analyse des prix des titres généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}.
        
        Ce rapport inclut :
        - Une analyse détaillée des prix par fonds
        - Des graphiques de distribution et de répartition
        - Des statistiques descriptives
        - Un tableau complet avec indicateurs visuels
        
        Le fichier Excel contenant les données brutes est également disponible sur demande.
        
        Cordialement,
        Système d'Analyse Financière
        """
        
        sender.envoyer_rapport(
            expediteur=expediteur,
            mot_de_passe=mot_de_passe,
            destinataires=destinataires,
            sujet=sujet,
            corps=corps,
            fichier_pdf=pdf_path
        )
        print(f"Rapport envoyé par courriel à : {', '.join(destinataires)}")
    
    print(f"Rapport PDF généré : {pdf_path}")
    print(f"Données Excel exportées : {excel_path}")
    return pdf_path, excel_path

if __name__ == "__main__":
    generer_et_envoyer_rapport() 
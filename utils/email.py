"""
Module pour la gestion des emails avec support OAuth et intégration Office 365.
"""

import os
import base64
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Union, Any
import msal
from O365 import Account, FileSystemTokenBackend, Message, MailBox, MSGraphProtocol
import pandas as pd
from email import message_from_bytes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import configparser
import logging
from dotenv import load_dotenv, find_dotenv
import json
import re
from pathlib import Path

logger = logging.getLogger(__name__)

def load_env_credentials():
    """Loads Microsoft 365 credentials from environment variables.
    
    Assumes environment variables are loaded from a .env file.

    Returns:
        dict: A dictionary containing the Microsoft 365 credentials
              (client_id, client_secret, tenant_id).
    """
    load_dotenv(find_dotenv())  # Load environment variables from .env file

def send_email(recipient: Union[str, List[str]], subject: str, body: str) -> bool:
    """Sends an email using the Microsoft 365 account configured in environment variables.

    Args:
        recipient: The email address(es) of the recipient(s).
        subject: The subject of the email.
        body: The body of the email.

    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    try:
        credentials = load_env_credentials()
        if not credentials or not all(credentials.values()):
            logger.error("Email credentials not found in environment variables.")
            return False

        token_backend = FileSystemTokenBackend(token_path='.', token_filename='o365_token.json')
        account = Account(credentials, token_backend=token_backend)

        if account.authenticate(scopes=['basic', 'message_send']):
            m = account.new_message()
            m.to.add(recipient)
            m.subject = subject
            m.body = body
            m.send()
            return True
        else:
            logger.error("Authentication failed.")
            return False
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return False

class OAuth2Config:
    """Configuration pour l'authentification OAuth2."""
    
    def __init__(self, client_id: str, client_secret: str, tenant_id: str):
        """Initialise la configuration OAuth2.
        
        Args:
            client_id: ID client OAuth2
            client_secret: Secret client OAuth2
            tenant_id: ID du tenant Office 365
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self.authority = f"https://login.microsoftonline.com/{tenant_id}"
        self.scopes = [
            'https://graph.microsoft.com/Mail.Read',
            'https://graph.microsoft.com/Mail.Send',
            'https://graph.microsoft.com/Mail.ReadWrite',
            'https://graph.microsoft.com/Group.Read.All',
            'https://graph.microsoft.com/Group.ReadWrite.All',
            'https://graph.microsoft.com/User.Read.All'
        ]
        
        # Configuration du stockage des tokens
        self.token_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'tokens')
        if not os.path.exists(self.token_path):
            os.makedirs(self.token_path)

class EmailManager:
    """Gestionnaire d'emails avec support OAuth et Office 365."""
    
    def __init__(self, oauth_config: OAuth2Config):
        """Initialise le gestionnaire d'emails."""
        self.oauth_config = oauth_config
        self.account = None
        self.mailbox = None
        
        # Initialisation de MSAL pour l'authentification
        self.app = msal.ConfidentialClientApplication(
            oauth_config.client_id,
            authority=oauth_config.authority,
            client_credential=oauth_config.client_secret,
            token_cache=msal.SerializableTokenCache()
        )
    
    def connecter(self):
        """Établit la connexion avec Office 365."""
        protocol = MSGraphProtocol()
        token_backend = FileSystemTokenBackend(
            token_path=self.oauth_config.token_path,
            token_filename='o365_token.txt'
        )
        
        self.account = Account((
            self.oauth_config.client_id,
            self.oauth_config.client_secret
        ), protocol=protocol, token_backend=token_backend)
        
        if not self.account.is_authenticated:
            self.account.authenticate(self.oauth_config.scopes)
        
        self.mailbox = self.account.mailbox()
    
    def envoyer_email(
        self,
        destinataires: List[str],
        sujet: str,
        corps: str,
        pieces_jointes: Optional[List[str]] = None,
        html: bool = False,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
        importance: str = 'normal',
        categories: Optional[List[str]] = None,
        planification: Optional[datetime] = None
    ):
        """Envoie un email avec options avancées.
        
        Args:
            destinataires: Liste des adresses email des destinataires
            sujet: Sujet de l'email
            corps: Corps de l'email
            pieces_jointes: Liste des chemins des fichiers à joindre
            html: True si le corps est au format HTML
            cc: Liste des destinataires en copie
            bcc: Liste des destinataires en copie cachée
            importance: Importance du message ('low', 'normal', 'high')
            categories: Liste des catégories à appliquer
            planification: Date/heure d'envoi planifié
        """
        message = self.mailbox.new_message()
        message.subject = sujet
        message.body = corps
        message.to.add(destinataires)
        
        if cc:
            message.cc.add(cc)
        if bcc:
            message.bcc.add(bcc)
        
        if pieces_jointes:
            for fichier in pieces_jointes:
                message.attachments.add(fichier)
        
        if importance != 'normal':
            message.importance = importance
        
        if categories:
            message.categories = categories
        
        if planification:
            message.send(schedule=planification)
        else:
            message.send()
    
    def creer_regle_email(
        self,
        nom: str,
        conditions: Dict[str, Any],
        actions: Dict[str, Any]
    ):
        """Crée une règle de traitement des emails.
        
        Args:
            nom: Nom de la règle
            conditions: Dictionnaire des conditions
            actions: Dictionnaire des actions à effectuer
        """
        regle = self.mailbox.create_rule(nom)
        
        # Configuration des conditions
        if 'expediteur' in conditions:
            regle.conditions.sender.contains(conditions['expediteur'])
        if 'sujet' in conditions:
            regle.conditions.subject.contains(conditions['sujet'])
        if 'corps' in conditions:
            regle.conditions.body.contains(conditions['corps'])
        if 'piece_jointe' in conditions:
            regle.conditions.has_attachments = True
        
        # Configuration des actions
        if 'dossier' in actions:
            regle.actions.move_to_folder(actions['dossier'])
        if 'marquer_lu' in actions:
            regle.actions.mark_as_read = actions['marquer_lu']
        if 'categorie' in actions:
            regle.actions.assign_categories([actions['categorie']])
        if 'supprimer' in actions:
            regle.actions.delete = actions['supprimer']
        
        regle.save()
    
    def archiver_emails(
        self,
        dossier_source: str,
        dossier_archive: str,
        age_minimum: int = 30,
        conserver_copies: bool = True
    ):
        """Archive les anciens emails.
        
        Args:
            dossier_source: Dossier source des emails
            dossier_archive: Dossier d'archivage
            age_minimum: Âge minimum des emails à archiver (en jours)
            conserver_copies: Conserver une copie dans le dossier source
        """
        source = self.mailbox.get_folder(folder_name=dossier_source)
        archive = self.mailbox.get_folder(folder_name=dossier_archive)
        
        date_limite = datetime.now() - timedelta(days=age_minimum)
        query = source.get_messages().filter(f"receivedDateTime le {date_limite.isoformat()}")
        
        for message in query.fetch():
            if conserver_copies:
                message.copy(archive)
            else:
                message.move(archive)
    
    def recherche_avancee(
        self,
        dossier: str = 'Inbox',
        expediteur: Optional[str] = None,
        sujet: Optional[str] = None,
        contenu: Optional[str] = None,
        piece_jointe: Optional[str] = None,
        date_debut: Optional[datetime] = None,
        date_fin: Optional[datetime] = None,
        categories: Optional[List[str]] = None,
        importance: Optional[str] = None,
        non_lus: Optional[bool] = None
    ) -> List[Dict]:
        """Recherche avancée d'emails avec filtres multiples.
        
        Args:
            dossier: Nom du dossier à rechercher
            expediteur: Filtre sur l'expéditeur
            sujet: Filtre sur le sujet
            contenu: Filtre sur le contenu
            piece_jointe: Filtre sur les pièces jointes
            date_debut: Date de début de la recherche
            date_fin: Date de fin de la recherche
            categories: Liste des catégories à filtrer
            importance: Filtre sur l'importance
            non_lus: True pour ne retourner que les messages non lus
        
        Returns:
            Liste des emails correspondant aux critères
        """
        folder = self.mailbox.get_folder(folder_name=dossier)
        query = folder.get_messages()
        
        # Construction de la requête
        filtres = []
        
        if expediteur:
            filtres.append(f"from/emailAddress/address eq '{expediteur}'")
        
        if sujet:
            filtres.append(f"contains(subject,'{sujet}')")
        
        if date_debut:
            filtres.append(f"receivedDateTime ge {date_debut.isoformat()}")
        
        if date_fin:
            filtres.append(f"receivedDateTime le {date_fin.isoformat()}")
        
        if importance:
            filtres.append(f"importance eq '{importance}'")
        
        if non_lus is not None:
            filtres.append(f"isRead eq {str(not non_lus).lower()}")
        
        if filtres:
            query = query.filter(" and ".join(filtres))
        
        messages = []
        for msg in query.fetch():
            if self._applique_filtres_avances(
                msg,
                contenu=contenu,
                piece_jointe=piece_jointe,
                categories=categories
            ):
                messages.append(self._extraire_info_message(msg))
        
        return messages
    
    def _applique_filtres_avances(
        self,
        message: Message,
        contenu: Optional[str] = None,
        piece_jointe: Optional[str] = None,
        categories: Optional[List[str]] = None
    ) -> bool:
        """Applique des filtres avancés sur un message."""
        if contenu and contenu.lower() not in message.body.lower():
            return False
        
        if piece_jointe:
            piece_jointe_trouvee = False
            for attachment in message.attachments:
                if piece_jointe.lower() in attachment.name.lower():
                    piece_jointe_trouvee = True
                    break
            if not piece_jointe_trouvee:
                return False
        
        if categories:
            msg_categories = set(message.categories or [])
            if not msg_categories.intersection(categories):
                return False
        
        return True
    
    def analyser_tendances_email(
        self,
        dossier: str = 'Inbox',
        periode: int = 30
    ) -> Dict[str, Any]:
        """Analyse les tendances des emails.
        
        Args:
            dossier: Dossier à analyser
            periode: Période d'analyse en jours
        
        Returns:
            Dictionnaire contenant les statistiques d'analyse
        """
        date_debut = datetime.now() - timedelta(days=periode)
        emails = self.recherche_avancee(
            dossier=dossier,
            date_debut=date_debut
        )
        
        df = pd.DataFrame(emails)
        
        # Analyse par expéditeur
        stats_expediteurs = df['expediteur'].value_counts().head(10).to_dict()
        
        # Analyse temporelle
        df['date'] = pd.to_datetime(df['date_reception'])
        emails_par_jour = df.groupby(df['date'].dt.date).size().to_dict()
        
        # Analyse des pièces jointes
        nb_pieces_jointes = sum(len(pj) for pj in df['pieces_jointes'])
        
        return {
            'total_emails': len(df),
            'top_expediteurs': stats_expediteurs,
            'emails_par_jour': emails_par_jour,
            'pieces_jointes_total': nb_pieces_jointes,
            'moyenne_quotidienne': len(df) / periode
        }
    
    def sauvegarder_emails(
        self,
        dossier: str,
        format: str = 'json',
        chemin_sortie: Optional[str] = None
    ):
        """Sauvegarde les emails d'un dossier.
        
        Args:
            dossier: Dossier à sauvegarder
            format: Format de sauvegarde ('json' ou 'excel')
            chemin_sortie: Chemin du fichier de sortie
        """
        if not chemin_sortie:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            chemin_sortie = f"sauvegarde_emails_{timestamp}.{format}"
        
        emails = self.lire_emails(dossier=dossier, limite=None)
        
        if format == 'json':
            with open(chemin_sortie, 'w', encoding='utf-8') as f:
                json.dump(emails, f, ensure_ascii=False, indent=2)
        else:  # excel
            df = pd.DataFrame(emails)
            df.to_excel(chemin_sortie, index=False)
    
    def restaurer_emails(
        self,
        chemin_fichier: str,
        dossier_destination: str
    ):
        """Restaure des emails à partir d'une sauvegarde.
        
        Args:
            chemin_fichier: Chemin du fichier de sauvegarde
            dossier_destination: Dossier de destination
        """
        ext = Path(chemin_fichier).suffix.lower()
        
        if ext == '.json':
            with open(chemin_fichier, 'r', encoding='utf-8') as f:
                emails = json.load(f)
        else:  # excel
            df = pd.read_excel(chemin_fichier)
            emails = df.to_dict('records')
        
        dossier = self.mailbox.get_folder(folder_name=dossier_destination)
        
        for email in emails:
            message = self.mailbox.new_message()
            message.subject = email['sujet']
            message.body = email['corps']
            message.to.add([email['expediteur']])
            message.received = datetime.strptime(
                email['date_reception'],
                "%Y-%m-%d %H:%M:%S"
            )
            
            # Restauration des pièces jointes si disponibles
            if 'pieces_jointes' in email and email['pieces_jointes']:
                for pj in email['pieces_jointes']:
                    if os.path.exists(pj):
                        message.attachments.add(pj)
            
            message.save_draft(dossier)
    
    def lire_emails(
        self,
        dossier: str = 'Inbox',
        limite: int = 100,
        depuis: Optional[datetime] = None,
        filtre_objet: Optional[str] = None,
        filtre_contenu: Optional[str] = None,
        filtre_piece_jointe: Optional[str] = None
    ) -> List[Dict]:
        """Lit les emails d'un dossier avec filtres.
        
        Args:
            dossier: Nom du dossier à lire
            limite: Nombre maximum d'emails à récupérer
            depuis: Date de début pour la recherche
            filtre_objet: Texte à rechercher dans l'objet
            filtre_contenu: Texte à rechercher dans le corps
            filtre_piece_jointe: Nom de fichier à rechercher dans les pièces jointes
        
        Returns:
            Liste de dictionnaires contenant les informations des emails
        """
        messages = []
        folder = self.mailbox.get_folder(folder_name=dossier)
        query = folder.get_messages()
        
        if depuis:
            query = query.filter(f"receivedDateTime ge {depuis.isoformat()}")
        
        for msg in query.fetch(limit=limite):
            if self._applique_filtres(
                msg,
                filtre_objet,
                filtre_contenu,
                filtre_piece_jointe
            ):
                messages.append(self._extraire_info_message(msg))
        
        return messages
    
    def _applique_filtres(
        self,
        message: Message,
        filtre_objet: Optional[str],
        filtre_contenu: Optional[str],
        filtre_piece_jointe: Optional[str]
    ) -> bool:
        """Applique les filtres sur un message.
        
        Args:
            message: Message à filtrer
            filtre_objet: Filtre sur l'objet
            filtre_contenu: Filtre sur le contenu
            filtre_piece_jointe: Filtre sur les pièces jointes
        
        Returns:
            True si le message passe les filtres, False sinon
        """
        if filtre_objet and filtre_objet.lower() not in message.subject.lower():
            return False
        
        if filtre_contenu and filtre_contenu.lower() not in message.body.lower():
            return False
        
        if filtre_piece_jointe:
            piece_jointe_trouvee = False
            for attachment in message.attachments:
                if filtre_piece_jointe.lower() in attachment.name.lower():
                    piece_jointe_trouvee = True
                    break
            if not piece_jointe_trouvee:
                return False
        
        return True
    
    def _extraire_info_message(self, message: Message) -> Dict:
        """Extrait les informations importantes d'un message.
        
        Args:
            message: Message à analyser
        
        Returns:
            Dictionnaire contenant les informations du message
        """
        return {
            'id': message.object_id,
            'sujet': message.subject,
            'expediteur': message.sender.address,
            'date_reception': message.received.strftime("%Y-%m-%d %H:%M:%S"),
            'pieces_jointes': [a.name for a in message.attachments],
            'corps': message.body
        }
    
    def extraire_pieces_jointes(
        self,
        message_id: str,
        dossier_destination: str,
        filtre: Optional[str] = None
    ) -> List[str]:
        """Extrait les pièces jointes d'un message.
        
        Args:
            message_id: ID du message
            dossier_destination: Dossier où sauvegarder les pièces jointes
            filtre: Filtre sur le nom des fichiers
        
        Returns:
            Liste des chemins des fichiers extraits
        """
        message = self.mailbox.get_message(message_id)
        fichiers_extraits = []
        
        for attachment in message.attachments:
            if filtre and filtre.lower() not in attachment.name.lower():
                continue
            
            chemin = os.path.join(dossier_destination, attachment.name)
            attachment.save(chemin)
            fichiers_extraits.append(chemin)
        
        return fichiers_extraits
    
    def lire_emails_groupe(
        self,
        groupe_id: str,
        **kwargs
    ) -> List[Dict]:
        """Lit les emails d'un groupe Office 365.
        
        Args:
            groupe_id: ID du groupe
            **kwargs: Arguments supplémentaires pour lire_emails()
        
        Returns:
            Liste des emails du groupe
        """
        groupe = self.account.groups[groupe_id]
        self.mailbox = groupe.get_mailbox()
        return self.lire_emails(**kwargs)
    
    def exporter_vers_excel(
        self,
        emails: List[Dict],
        chemin_sortie: str
    ):
        """Exporte les emails vers un fichier Excel.
        
        Args:
            emails: Liste des emails à exporter
            chemin_sortie: Chemin du fichier Excel de sortie
        """
        df = pd.DataFrame(emails)
        df.to_excel(chemin_sortie, index=False)

def exemple_utilisation():
    """Exemple d'utilisation du gestionnaire d'emails."""
    # Configuration OAuth
    config = OAuth2Config(
        client_id="votre_client_id",
        client_secret="votre_client_secret",
        tenant_id="votre_tenant_id"
    )
    
    # Initialisation du gestionnaire
    email_manager = EmailManager(config)
    email_manager.connecter()
    
    # Création d'une règle de traitement
    email_manager.creer_regle_email(
        nom="Archivage rapports",
        conditions={
            'sujet': 'Rapport',
            'piece_jointe': True
        },
        actions={
            'dossier': 'Archive/Rapports',
            'marquer_lu': True,
            'categorie': 'Rapports'
        }
    )
    
    # Recherche avancée
    emails = email_manager.recherche_avancee(
        expediteur="contact@example.com",
        date_debut=datetime.now() - timedelta(days=7),
        categories=['Important'],
        non_lus=True
    )
    
    # Analyse des tendances
    tendances = email_manager.analyser_tendances_email(periode=90)
    print(f"Nombre total d'emails : {tendances['total_emails']}")
    print(f"Moyenne quotidienne : {tendances['moyenne_quotidienne']:.2f}")
    
    # Sauvegarde des emails
    email_manager.sauvegarder_emails(
        dossier='Important',
        format='json',
        chemin_sortie='sauvegarde_emails_importants.json'
    )

if __name__ == "__main__":
    exemple_utilisation()

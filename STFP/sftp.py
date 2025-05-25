# Fichier : STFP/sftp.py
# Description : Ce fichier contient les fonctionnalités pour gérer les opérations SFTP.

import paramiko
from constantes.const1 import load_config, SFTP_HOSTNAME, SFTP_PORT, SFTP_USERNAME, SFTP_PASSWORD

class SFTPClient:
    """
    Classe pour gérer les opérations SFTP.
    """
    def __init__(self):
        # S'assurer que la configuration est chargée avant d'utiliser les constantes
        load_config()
        self.transport = None
        self.sftp = None

    def connect(self):
        """
        Établit une connexion SFTP en utilisant les informations de configuration.

        Args:
            hostname (str): Nom d'hôte du serveur SFTP.
            port (int): Port du serveur SFTP.
        Args:
            hostname (str): Nom d'hôte du serveur SFTP.
            port (int): Port du serveur SFTP.
            username (str): Nom d'utilisateur pour la connexion SFTP.
            password (str): Mot de passe pour la connexion SFTP.
        """
        try:
            self.transport = paramiko.Transport((hostname, port))
            self.transport.connect(username=SFTP_USERNAME, password=SFTP_PASSWORD)
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
            print(f"Connexion SFTP établie à {SFTP_HOSTNAME}:{SFTP_PORT}")
        except paramiko.AuthenticationException:
            print("Échec de l'authentification SFTP.")
        except paramiko.SSHException as e:
            print(f"Erreur de connexion SSH : {e}")
        except Exception as e:
            print(f"Erreur inattendue lors de la connexion SFTP : {e}")

    def list_files(self, remote_path):
        """
        Liste les fichiers dans un répertoire distant.

        Args:
            remote_path (str): Chemin du répertoire distant.

        Returns:
            list: Liste des noms de fichiers dans le répertoire distant, ou None en cas d'erreur.
        """
        if self.sftp:
            try:
                return self.sftp.listdir(remote_path)
            except FileNotFoundError:
                print(f"Le répertoire distant '{remote_path}' n'existe pas.")
                return None
            except Exception as e:
                print(f"Erreur lors du listage des fichiers SFTP : {e}")
                return None
        else:
            print("Aucune connexion SFTP établie.")
            return None

    def download_file(self, remote_path, local_path):
        """
        Télécharge un fichier depuis le serveur SFTP.

        Args:
            remote_path (str): Chemin du fichier distant.
            local_path (str): Chemin où enregistrer le fichier localement.
        """
        if self.sftp:
            try:
                self.sftp.get(remote_path, local_path)
                print(f"Fichier '{remote_path}' téléchargé vers '{local_path}'.")
            except FileNotFoundError:
                print(f"Le fichier distant '{remote_path}' n'a pas été trouvé.")
            except Exception as e:
                print(f"Erreur lors du téléchargement du fichier SFTP : {e}")
        else:
            print("Aucune connexion SFTP établie.")

    def disconnect(self):
        """
        Ferme la connexion SFTP.
        """
        if self.sftp:
            self.sftp.close()
            print("Connexion SFTP fermée.")
        if self.transport:
            self.transport.close()
            print("Transport SFTP fermé.")

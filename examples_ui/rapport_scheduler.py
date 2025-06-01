"""
Module pour la planification automatique des rapports.
"""

import schedule
import time
import json
import os
from datetime import datetime, timedelta
from examples_ui.rapport_generator import generer_et_envoyer_rapport

class RapportScheduler:
    """Classe pour gérer la planification des rapports."""
    
    def __init__(self):
        """Initialise le planificateur."""
        self.config_dir = os.path.join(os.path.dirname(__file__), '..', 'config')
        self.config_file = os.path.join(self.config_dir, 'scheduler_config.json')
        
        # Création du dossier config s'il n'existe pas
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
        
        # Chargement de la configuration existante
        self.load_config()
    
    def load_config(self):
        """Charge la configuration depuis le fichier JSON."""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {
                'schedules': [],
                'email_config': {},
                'seuils': {}
            }
    
    def save_config(self):
        """Sauvegarde la configuration dans le fichier JSON."""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)
    
    def ajouter_planification(self, frequence, heure, email_config=None, seuils=None):
        """
        Ajoute une nouvelle planification.
        
        Args:
            frequence (str): 'quotidien', 'hebdomadaire' ou 'mensuel'
            heure (str): Heure d'exécution (format HH:MM)
            email_config (dict): Configuration email
            seuils (dict): Seuils personnalisés
        """
        nouvelle_planif = {
            'id': len(self.config['schedules']) + 1,
            'frequence': frequence,
            'heure': heure,
            'email_config': email_config,
            'seuils': seuils,
            'active': True,
            'derniere_execution': None
        }
        
        self.config['schedules'].append(nouvelle_planif)
        self.save_config()
        
        # Ajout de la tâche au planificateur
        self._ajouter_tache_planifiee(nouvelle_planif)
    
    def _ajouter_tache_planifiee(self, planif):
        """Configure une tâche planifiée dans schedule."""
        job = lambda: self._executer_rapport(planif)
        
        if planif['frequence'] == 'quotidien':
            schedule.every().day.at(planif['heure']).do(job)
        elif planif['frequence'] == 'hebdomadaire':
            schedule.every().monday.at(planif['heure']).do(job)
        elif planif['frequence'] == 'mensuel':
            schedule.every().day.at(planif['heure']).do(self._verifier_premier_jour_mois, job)
    
    def _verifier_premier_jour_mois(self, job):
        """Vérifie si c'est le premier jour du mois avant d'exécuter la tâche."""
        if datetime.now().day == 1:
            job()
    
    def _executer_rapport(self, planif):
        """Exécute la génération et l'envoi du rapport."""
        try:
            # Génération et envoi du rapport
            if planif['email_config']:
                generer_et_envoyer_rapport(
                    expediteur=planif['email_config']['expediteur'],
                    mot_de_passe=planif['email_config']['mot_de_passe'],
                    destinataires=planif['email_config']['destinataires'],
                    seuils=planif['seuils']
                )
            else:
                generer_et_envoyer_rapport(seuils=planif['seuils'])
            
            # Mise à jour de la dernière exécution
            planif['derniere_execution'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.save_config()
            
        except Exception as e:
            print(f"Erreur lors de l'exécution du rapport planifié : {str(e)}")
    
    def supprimer_planification(self, planif_id):
        """Supprime une planification."""
        self.config['schedules'] = [p for p in self.config['schedules'] if p['id'] != planif_id]
        self.save_config()
        schedule.clear()
        self._recharger_planifications()
    
    def _recharger_planifications(self):
        """Recharge toutes les planifications actives."""
        for planif in self.config['schedules']:
            if planif['active']:
                self._ajouter_tache_planifiee(planif)
    
    def demarrer(self):
        """Démarre le planificateur."""
        self._recharger_planifications()
        
        print("Planificateur de rapports démarré...")
        while True:
            schedule.run_pending()
            time.sleep(60)  # Vérifie toutes les minutes
    
    def lister_planifications(self):
        """Affiche la liste des planifications."""
        if not self.config['schedules']:
            print("Aucune planification configurée.")
            return
        
        print("\nPlanifications configurées :")
        print("-" * 50)
        for planif in self.config['schedules']:
            status = "Actif" if planif['active'] else "Inactif"
            derniere_exec = planif['derniere_execution'] or "Jamais"
            print(f"ID: {planif['id']}")
            print(f"Fréquence: {planif['frequence']}")
            print(f"Heure: {planif['heure']}")
            print(f"Statut: {status}")
            print(f"Dernière exécution: {derniere_exec}")
            if planif['email_config']:
                print(f"Destinataires: {', '.join(planif['email_config']['destinataires'])}")
            print("-" * 50)

def demarrer_planificateur():
    """Fonction utilitaire pour démarrer le planificateur."""
    scheduler = RapportScheduler()
    scheduler.demarrer()

if __name__ == "__main__":
    demarrer_planificateur() 
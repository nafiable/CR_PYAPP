"""
Exemple d'utilisation des outils de visualisation.
"""

import pandas as pd
import numpy as np
from sqlalchemy import text
from database.connexionsqlLiter import SQLiteConnection
from examples_ui.dataframe_viewer import affiche_dataframe
from examples_ui.rapport_generator import generer_et_envoyer_rapport
from examples_ui.rapport_scheduler import RapportScheduler

def afficher_analyse_secteurs():
    """Affiche une analyse par secteur."""
    db = SQLiteConnection()
    
    with db.engine.connect() as conn:
        # Requête d'analyse des secteurs
        query = text("""
            WITH PositionsParSecteur AS (
                SELECT 
                    s.nom as secteur,
                    t.code as code_titre,
                    t.nom as nom_titre,
                    cf.quantite,
                    cf.prix,
                    cf.valeur_marchande,
                    (cf.valeur_marchande * 100.0 / SUM(cf.valeur_marchande) OVER ()) as pourcentage
                FROM composition_fonds cf
                JOIN titre t ON cf.id_titre = t.id
                JOIN secteur s ON t.id_secteur = s.id
            )
            SELECT 
                secteur,
                COUNT(DISTINCT code_titre) as nombre_titres,
                SUM(valeur_marchande) as valeur_totale,
                AVG(pourcentage) as pourcentage_portefeuille,
                MIN(prix) as prix_min,
                MAX(prix) as prix_max,
                AVG(prix) as prix_moyen
            FROM PositionsParSecteur
            GROUP BY secteur
            ORDER BY valeur_totale DESC
        """)
        
        df_analyse = pd.read_sql(query, conn)
    
    # Formatage des colonnes numériques
    df_analyse['valeur_totale'] = df_analyse['valeur_totale'].round(2)
    df_analyse['pourcentage_portefeuille'] = df_analyse['pourcentage_portefeuille'].round(2)
    df_analyse['prix_moyen'] = df_analyse['prix_moyen'].round(2)
    
    # Affichage dans une fenêtre séparée
    affiche_dataframe(
        df_analyse,
        title="Analyse par Secteur",
        geometry="1400x600"
    )

def afficher_positions_importantes():
    """Affiche les positions les plus importantes."""
    db = SQLiteConnection()
    
    with db.engine.connect() as conn:
        # Requête pour les positions importantes
        query = text("""
            SELECT 
                f.code as code_fonds,
                f.nom as nom_fonds,
                t.code as code_titre,
                t.nom as nom_titre,
                s.nom as secteur,
                cf.quantite,
                cf.prix,
                cf.valeur_marchande,
                (cf.valeur_marchande * 100.0 / SUM(cf.valeur_marchande) OVER ()) as poids_portefeuille
            FROM composition_fonds cf
            JOIN fonds f ON cf.id_fonds = f.id
            JOIN titre t ON cf.id_titre = t.id
            JOIN secteur s ON t.id_secteur = s.id
            ORDER BY cf.valeur_marchande DESC
            LIMIT 10
        """)
        
        df_positions = pd.read_sql(query, conn)
    
    # Formatage des colonnes numériques
    df_positions['poids_portefeuille'] = df_positions['poids_portefeuille'].round(2)
    df_positions['valeur_marchande'] = df_positions['valeur_marchande'].round(2)
    
    # Affichage dans une fenêtre séparée
    affiche_dataframe(
        df_positions,
        title="Top 10 des Positions",
        geometry="1400x600"
    )

def afficher_evolution_performances():
    """Affiche l'évolution des performances par fonds."""
    db = SQLiteConnection()
    
    with db.engine.connect() as conn:
        # Requête pour l'évolution des performances
        query = text("""
            WITH PerformancesParDate AS (
                SELECT 
                    cf.date,
                    f.code as code_fonds,
                    f.nom as nom_fonds,
                    SUM(cf.valeur_marchande) as valeur_totale,
                    SUM(cf.dividende) as dividendes_totaux,
                    COUNT(DISTINCT t.id) as nombre_titres
                FROM composition_fonds cf
                JOIN fonds f ON cf.id_fonds = f.id
                JOIN titre t ON cf.id_titre = t.id
                GROUP BY cf.date, f.code, f.nom
            ),
            VariationsQuotidiennes AS (
                SELECT 
                    date,
                    code_fonds,
                    nom_fonds,
                    valeur_totale,
                    dividendes_totaux,
                    nombre_titres,
                    (valeur_totale - LAG(valeur_totale) OVER (PARTITION BY code_fonds ORDER BY date)) / 
                    LAG(valeur_totale) OVER (PARTITION BY code_fonds ORDER BY date) * 100 as variation_quotidienne
                FROM PerformancesParDate
            )
            SELECT 
                date,
                code_fonds,
                nom_fonds,
                valeur_totale,
                dividendes_totaux,
                nombre_titres,
                ROUND(variation_quotidienne, 2) as variation_pct,
                ROUND(AVG(variation_quotidienne) OVER (PARTITION BY code_fonds ORDER BY date ROWS BETWEEN 7 PRECEDING AND CURRENT ROW), 2) as moyenne_mobile_7j
            FROM VariationsQuotidiennes
            ORDER BY date DESC, valeur_totale DESC
        """)
        
        df_evolution = pd.read_sql(query, conn)
    
    # Formatage des colonnes numériques
    df_evolution['valeur_totale'] = df_evolution['valeur_totale'].round(2)
    df_evolution['dividendes_totaux'] = df_evolution['dividendes_totaux'].round(2)
    
    # Affichage dans une fenêtre séparée
    affiche_dataframe(
        df_evolution,
        title="Évolution des Performances par Fonds",
        geometry="1600x800"
    )

def calculer_ratios_performance(rendements):
    """Calcule les ratios de performance pour une série de rendements."""
    # Taux sans risque annuel (à adapter selon vos besoins)
    taux_sans_risque = 0.02 / 252  # Converti en quotidien
    
    # Calculs de base
    rendement_moyen = rendements.mean()
    volatilite = rendements.std()
    rendement_excedentaire = rendements - taux_sans_risque
    
    # Ratio de Sharpe
    ratio_sharpe = np.sqrt(252) * (rendement_moyen - taux_sans_risque) / volatilite if volatilite != 0 else 0
    
    # Ratio de Sortino (ne considère que la volatilité négative)
    rendements_negatifs = rendements[rendements < 0]
    volatilite_negative = rendements_negatifs.std()
    ratio_sortino = np.sqrt(252) * (rendement_moyen - taux_sans_risque) / volatilite_negative if volatilite_negative != 0 else 0
    
    # Maximum Drawdown
    cumul_rendements = (1 + rendements).cumprod()
    max_drawdown = ((cumul_rendements.cummax() - cumul_rendements) / cumul_rendements.cummax()).max()
    
    return {
        'rendement_annualise': (1 + rendement_moyen) ** 252 - 1,
        'volatilite_annualisee': volatilite * np.sqrt(252),
        'ratio_sharpe': ratio_sharpe,
        'ratio_sortino': ratio_sortino,
        'max_drawdown': max_drawdown
    }

def afficher_correlations_ratios():
    """Affiche les corrélations entre fonds et leurs ratios de performance."""
    db = SQLiteConnection()
    
    with db.engine.connect() as conn:
        # Requête pour obtenir les rendements quotidiens
        query = text("""
            WITH PerformancesQuotidiennes AS (
                SELECT 
                    cf.date,
                    f.code as code_fonds,
                    SUM(cf.valeur_marchande) as valeur_totale
                FROM composition_fonds cf
                JOIN fonds f ON cf.id_fonds = f.id
                GROUP BY cf.date, f.code
            ),
            Rendements AS (
                SELECT 
                    date,
                    code_fonds,
                    valeur_totale,
                    (valeur_totale - LAG(valeur_totale) OVER (PARTITION BY code_fonds ORDER BY date)) / 
                    LAG(valeur_totale) OVER (PARTITION BY code_fonds ORDER BY date) as rendement_quotidien
                FROM PerformancesQuotidiennes
            )
            SELECT *
            FROM Rendements
            WHERE rendement_quotidien IS NOT NULL
            ORDER BY date, code_fonds
        """)
        
        df_rendements = pd.read_sql(query, conn)
    
    # Création d'une table pivot pour les corrélations
    pivot_rendements = df_rendements.pivot(index='date', columns='code_fonds', values='rendement_quotidien')
    
    # Calcul des corrélations
    correlations = pivot_rendements.corr()
    
    # Calcul des ratios de performance pour chaque fonds
    ratios = {}
    for fonds in pivot_rendements.columns:
        ratios[fonds] = calculer_ratios_performance(pivot_rendements[fonds].dropna())
    
    # Création du DataFrame des ratios
    df_ratios = pd.DataFrame.from_dict(ratios, orient='index')
    df_ratios.index.name = 'code_fonds'
    
    # Formatage des valeurs
    df_ratios = df_ratios.round(4)
    correlations = correlations.round(4)
    
    # Affichage des corrélations
    affiche_dataframe(
        correlations,
        title="Matrice de Corrélation entre Fonds",
        geometry="1200x800"
    )
    
    # Affichage des ratios
    affiche_dataframe(
        df_ratios,
        title="Ratios de Performance par Fonds",
        geometry="1400x600"
    )

def personnaliser_seuils():
    """Permet à l'utilisateur de personnaliser les seuils."""
    print("\nPersonnalisation des seuils de prix")
    print("-" * 30)
    
    try:
        seuils = {
            'danger': float(input("Seuil critique (rouge) : ")),
            'warning': float(input("Seuil d'attention (orange) : ")),
            'info': float(input("Seuil de surveillance (bleu) : "))
        }
        return seuils
    except ValueError:
        print("Erreur : veuillez entrer des nombres valides")
        return None

def configurer_email():
    """Permet à l'utilisateur de configurer l'envoi par courriel."""
    print("\nConfiguration de l'envoi par courriel")
    print("-" * 30)
    
    expediteur = input("Adresse email de l'expéditeur : ")
    mot_de_passe = input("Mot de passe de l'expéditeur : ")
    destinataires = input("Adresses email des destinataires (séparées par des virgules) : ").split(',')
    destinataires = [d.strip() for d in destinataires]
    
    return expediteur, mot_de_passe, destinataires

def configurer_planification():
    """Configure une nouvelle planification de rapport."""
    print("\nConfiguration de la planification")
    print("-" * 30)
    
    # Choix de la fréquence
    print("\nFréquence de génération :")
    print("1. Quotidien")
    print("2. Hebdomadaire")
    print("3. Mensuel")
    
    choix_freq = input("Votre choix (1-3) : ")
    if choix_freq == "1":
        frequence = "quotidien"
    elif choix_freq == "2":
        frequence = "hebdomadaire"
    elif choix_freq == "3":
        frequence = "mensuel"
    else:
        print("Choix invalide")
        return
    
    # Heure d'exécution
    while True:
        try:
            heure = input("Heure d'exécution (HH:MM) : ")
            # Vérification du format
            datetime.strptime(heure, "%H:%M")
            break
        except ValueError:
            print("Format d'heure invalide. Utilisez le format HH:MM")
    
    # Configuration email
    email_config = None
    if input("\nVoulez-vous configurer l'envoi par email ? (o/n) : ").lower() == 'o':
        expediteur = input("Email de l'expéditeur : ")
        mot_de_passe = input("Mot de passe : ")
        destinataires = input("Destinataires (séparés par des virgules) : ").split(',')
        email_config = {
            'expediteur': expediteur,
            'mot_de_passe': mot_de_passe,
            'destinataires': [d.strip() for d in destinataires]
        }
    
    # Seuils personnalisés
    seuils = None
    if input("\nVoulez-vous personnaliser les seuils ? (o/n) : ").lower() == 'o':
        seuils = personnaliser_seuils()
    
    return {
        'frequence': frequence,
        'heure': heure,
        'email_config': email_config,
        'seuils': seuils
    }

def gerer_planifications():
    """Gère les planifications de rapports."""
    scheduler = RapportScheduler()
    
    while True:
        print("\nGestion des planifications")
        print("-" * 30)
        print("1. Lister les planifications")
        print("2. Ajouter une planification")
        print("3. Supprimer une planification")
        print("4. Retour au menu principal")
        
        choix = input("\nVotre choix (1-4) : ")
        
        if choix == "1":
            scheduler.lister_planifications()
        
        elif choix == "2":
            config = configurer_planification()
            if config:
                scheduler.ajouter_planification(
                    frequence=config['frequence'],
                    heure=config['heure'],
                    email_config=config['email_config'],
                    seuils=config['seuils']
                )
                print("Planification ajoutée avec succès")
        
        elif choix == "3":
            scheduler.lister_planifications()
            try:
                planif_id = int(input("\nID de la planification à supprimer : "))
                scheduler.supprimer_planification(planif_id)
                print("Planification supprimée avec succès")
            except ValueError:
                print("ID invalide")
        
        elif choix == "4":
            break
        
        else:
            print("Choix invalide")

if __name__ == "__main__":
    print("Analyse du portefeuille")
    print("-" * 50)
    
    while True:
        print("\nQue souhaitez-vous analyser ?")
        print("1. Analyse par secteur")
        print("2. Top 10 des positions")
        print("3. Évolution des performances")
        print("4. Corrélations et ratios")
        print("5. Générer et envoyer rapport")
        print("6. Gérer les planifications")
        print("7. Quitter")
        
        choix = input("\nVotre choix (1-7) : ")
        
        if choix == "1":
            afficher_analyse_secteurs()
        elif choix == "2":
            afficher_positions_importantes()
        elif choix == "3":
            afficher_evolution_performances()
        elif choix == "4":
            afficher_correlations_ratios()
        elif choix == "5":
            print("\nGénération du rapport PDF...")
            
            # Personnalisation des seuils
            personnaliser = input("Voulez-vous personnaliser les seuils ? (o/n) : ").lower() == 'o'
            seuils = personnaliser_seuils() if personnaliser else None
            
            # Configuration de l'envoi par courriel
            envoyer = input("Voulez-vous envoyer le rapport par courriel ? (o/n) : ").lower() == 'o'
            if envoyer:
                expediteur, mot_de_passe, destinataires = configurer_email()
                pdf_path, excel_path = generer_et_envoyer_rapport(
                    expediteur=expediteur,
                    mot_de_passe=mot_de_passe,
                    destinataires=destinataires,
                    seuils=seuils
                )
            else:
                pdf_path, excel_path = generer_et_envoyer_rapport(seuils=seuils)
            
            print(f"\nRapport généré avec succès :")
            print(f"- PDF : {pdf_path}")
            print(f"- Excel : {excel_path}")
        
        elif choix == "6":
            gerer_planifications()
        
        elif choix == "7":
            print("\nAu revoir !")
            break
        else:
            print("\nChoix invalide. Veuillez réessayer.") 
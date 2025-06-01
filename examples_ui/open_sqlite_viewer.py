"""
Script pour ouvrir SQLite Viewer avec la base de données.
"""

import os
import subprocess
import sys
import webbrowser

def open_with_sqlite_viewer():
    """Ouvre la base de données avec SQLite Viewer."""
    db_path = os.path.abspath("database.db")
    
    # Essaie d'ouvrir avec DB Browser for SQLite s'il est installé
    try:
        if sys.platform == "win32":
            # Chemins possibles pour DB Browser sur Windows
            paths = [
                r"C:\Program Files\DB Browser for SQLite\DB Browser for SQLite.exe",
                r"C:\Program Files (x86)\DB Browser for SQLite\DB Browser for SQLite.exe"
            ]
            for path in paths:
                if os.path.exists(path):
                    subprocess.Popen([path, db_path])
                    return True
        
        # Pour les autres systèmes d'exploitation
        elif sys.platform == "darwin":  # macOS
            subprocess.Popen(["open", "-a", "DB Browser for SQLite", db_path])
            return True
        elif sys.platform.startswith("linux"):  # Linux
            subprocess.Popen(["sqlitebrowser", db_path])
            return True
            
    except Exception as e:
        print(f"Erreur lors de l'ouverture de DB Browser: {str(e)}")
    
    # Si DB Browser n'est pas disponible, ouvre le site de téléchargement
    print("DB Browser for SQLite n'est pas installé.")
    print("Ouverture du site de téléchargement...")
    webbrowser.open("https://sqlitebrowser.org/dl/")
    return False

if __name__ == "__main__":
    open_with_sqlite_viewer() 
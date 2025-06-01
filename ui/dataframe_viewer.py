"""
Module pour l'affichage des DataFrames avec une interface utilisateur.
"""

import logging
import pandas as pd
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

logger = logging.getLogger(__name__)

# Configuration des templates
templates = Jinja2Templates(directory="templates")

# Création du router
router = APIRouter()

class DataFrameViewer:
    """Classe pour l'affichage des DataFrames."""
    
    def __init__(self):
        """Initialisation du viewer."""
        self.current_df: Optional[pd.DataFrame] = None
        self.current_name: str = ""
        self.history: List[Dict[str, Any]] = []
    
    def set_dataframe(self, df: pd.DataFrame, name: str) -> None:
        """
        Définit le DataFrame à afficher.
        
        Args:
            df (pd.DataFrame): DataFrame à afficher
            name (str): Nom du DataFrame
        """
        self.current_df = df
        self.current_name = name
        self.history.append({
            "name": name,
            "shape": df.shape,
            "columns": list(df.columns)
        })
        logger.info(f"DataFrame {name} chargé ({df.shape[0]} lignes, {df.shape[1]} colonnes)")
    
    def get_html(self, request: Request) -> str:
        """
        Génère le HTML pour afficher le DataFrame.
        
        Args:
            request (Request): Requête FastAPI
            
        Returns:
            str: Code HTML
        """
        if self.current_df is None:
            return templates.TemplateResponse(
                "no_data.html",
                {"request": request}
            )
        
        return templates.TemplateResponse(
            "dataframe.html",
            {
                "request": request,
                "df_name": self.current_name,
                "df_html": self.current_df.to_html(
                    classes=["table", "table-striped", "table-hover"],
                    index=True,
                    border=0
                ),
                "shape": self.current_df.shape,
                "columns": list(self.current_df.columns),
                "dtypes": self.current_df.dtypes.to_dict(),
                "history": self.history
            }
        )
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Retourne un résumé du DataFrame.
        
        Returns:
            Dict[str, Any]: Résumé statistique
        """
        if self.current_df is None:
            return {}
        
        return {
            "name": self.current_name,
            "shape": self.current_df.shape,
            "columns": list(self.current_df.columns),
            "dtypes": self.current_df.dtypes.to_dict(),
            "numeric_summary": self.current_df.describe().to_dict(),
            "missing_values": self.current_df.isnull().sum().to_dict()
        }

# Instance globale du viewer
viewer = DataFrameViewer()

@router.get("/view", response_class=HTMLResponse)
async def view_dataframe(request: Request):
    """
    Endpoint pour afficher le DataFrame.
    
    Args:
        request (Request): Requête FastAPI
        
    Returns:
        HTMLResponse: Page HTML
    """
    return viewer.get_html(request)

@router.get("/summary")
async def get_summary():
    """
    Endpoint pour obtenir le résumé du DataFrame.
    
    Returns:
        Dict[str, Any]: Résumé statistique
    """
    return viewer.get_summary()

# Créer les templates HTML nécessaires
def create_templates():
    """Crée les fichiers de templates HTML."""
    templates_dir = Path("templates")
    templates_dir.mkdir(exist_ok=True)
    
    # Template principal
    dataframe_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>{{ df_name }} - DataFrame Viewer</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            .table-container {
                margin: 20px;
                overflow-x: auto;
            }
            .summary-container {
                margin: 20px;
            }
            .history-container {
                margin: 20px;
            }
        </style>
    </head>
    <body>
        <nav class="navbar navbar-dark bg-dark">
            <div class="container-fluid">
                <span class="navbar-brand">DataFrame Viewer</span>
            </div>
        </nav>
        
        <div class="container-fluid">
            <div class="row">
                <div class="col-md-3">
                    <div class="summary-container">
                        <h4>Informations</h4>
                        <ul class="list-group">
                            <li class="list-group-item">Nom: {{ df_name }}</li>
                            <li class="list-group-item">Lignes: {{ shape[0] }}</li>
                            <li class="list-group-item">Colonnes: {{ shape[1] }}</li>
                        </ul>
                        
                        <h4 class="mt-4">Colonnes</h4>
                        <ul class="list-group">
                            {% for col, dtype in dtypes.items() %}
                            <li class="list-group-item">
                                {{ col }} <span class="badge bg-secondary">{{ dtype }}</span>
                            </li>
                            {% endfor %}
                        </ul>
                        
                        <h4 class="mt-4">Historique</h4>
                        <ul class="list-group">
                            {% for item in history %}
                            <li class="list-group-item">
                                {{ item.name }}
                                <small class="text-muted d-block">
                                    {{ item.shape[0] }} lignes, {{ item.shape[1] }} colonnes
                                </small>
                            </li>
                            {% endfor %}
                        </ul>
                    </div>
                </div>
                
                <div class="col-md-9">
                    <div class="table-container">
                        {{ df_html | safe }}
                    </div>
                </div>
            </div>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """
    
    # Template pour aucune donnée
    no_data_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>DataFrame Viewer - Aucune donnée</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <nav class="navbar navbar-dark bg-dark">
            <div class="container-fluid">
                <span class="navbar-brand">DataFrame Viewer</span>
            </div>
        </nav>
        
        <div class="container mt-5">
            <div class="alert alert-info">
                Aucun DataFrame n'est actuellement chargé.
            </div>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """
    
    # Écriture des templates
    with open(templates_dir / "dataframe.html", "w", encoding="utf-8") as f:
        f.write(dataframe_template.strip())
    
    with open(templates_dir / "no_data.html", "w", encoding="utf-8") as f:
        f.write(no_data_template.strip())
    
    logger.info("Templates HTML créés avec succès") 
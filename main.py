"""
Point d'entrée principal de l'application.
Ce module expose l'API FastAPI qui sera utilisée par les clients.
"""

import os
import logging
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from config.logging_config import setup_logging
from routes.data_routes import router as data_router
from database.connexionsqlLiter import SQLiteConnection
from constantes import const1

# Configuration du logging
setup_logging()
logger = logging.getLogger(__name__)

# Chargement des variables d'environnement
load_dotenv("config.env")

# Création de l'application FastAPI
app = FastAPI(
    title="Finance API",
    description="API de gestion des fonds, portefeuilles et données financières",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration des templates et fichiers statiques
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Inclusion des routes
app.include_router(data_router)

@app.on_event("startup")
async def startup_event():
    """Événement exécuté au démarrage de l'application."""
    logger.info("Démarrage de l'application")
    const1.load_config()
    
    # Initialisation de la base SQLite
    sqlite_conn = SQLiteConnection()
    sqlite_conn.init_database()

@app.on_event("shutdown")
async def shutdown_event():
    """Événement exécuté à l'arrêt de l'application."""
    logger.info("Arrêt de l'application")

@app.get("/")
async def home(request: Request):
    """
    Page d'accueil de l'application.
    
    Args:
        request (Request): La requête HTTP
        
    Returns:
        TemplateResponse: La page d'accueil
    """
    return templates.TemplateResponse(
        "dataframe_viewer.html",
        {"request": request}
    )

@app.get("/health")
async def health_check():
    """
    Endpoint de vérification de la santé de l'API.
    
    Returns:
        dict: État de santé de l'API
    """
    return {
        "status": "healthy",
        "version": "1.0.0",
        "environment": os.getenv("ENV_TYPE", "development")
    }

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Middleware pour logger toutes les requêtes entrantes.
    
    Args:
        request (Request): La requête HTTP entrante
        call_next (Callable): La fonction à appeler pour continuer le traitement
        
    Returns:
        Response: La réponse HTTP
    """
    logger.info(f"Requête entrante: {request.method} {request.url}")
    response = await call_next(request)
    return response

if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))
    debug = os.getenv("API_DEBUG", "True").lower() == "true"
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug
    )
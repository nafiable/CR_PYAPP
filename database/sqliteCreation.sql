-- Script de création des tables pour SQLite

-- Création des tables principales

-- Table Gestionnaire
CREATE TABLE IF NOT EXISTS gestionnaire (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code VARCHAR(50) UNIQUE NOT NULL,
    nom VARCHAR(255) NOT NULL,
    description TEXT,
    tel VARCHAR(20),
    contact_principal VARCHAR(100),
    email VARCHAR(255),
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_modification DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table Region
CREATE TABLE IF NOT EXISTS region1 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code VARCHAR(50) UNIQUE NOT NULL,
    nom VARCHAR(255) NOT NULL,
    description TEXT,
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_modification DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table Devise
CREATE TABLE IF NOT EXISTS devise (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code VARCHAR(50) UNIQUE NOT NULL,
    nom VARCHAR(255) NOT NULL,
    description TEXT,
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_modification DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table Pays
CREATE TABLE IF NOT EXISTS pays (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code VARCHAR(50) UNIQUE NOT NULL,
    nom VARCHAR(255) NOT NULL,
    description TEXT,
    id_region INTEGER NOT NULL,
    continent VARCHAR(50),
    id_devise INTEGER NOT NULL,
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_modification DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_region) REFERENCES region1(id),
    FOREIGN KEY (id_devise) REFERENCES devise(id)
);

-- Table Secteur
CREATE TABLE IF NOT EXISTS secteur (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code VARCHAR(50) UNIQUE NOT NULL,
    nom VARCHAR(255) NOT NULL,
    description TEXT,
    code_gics VARCHAR(50),
    code_bics VARCHAR(50),
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_modification DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table TypeActif1
CREATE TABLE IF NOT EXISTS type_actif1 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code VARCHAR(50) UNIQUE NOT NULL,
    nom VARCHAR(255) NOT NULL,
    description TEXT,
    type VARCHAR(50),
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_modification DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table SousTypeActif1
CREATE TABLE IF NOT EXISTS sous_type_actif1 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code VARCHAR(50) UNIQUE NOT NULL,
    nom VARCHAR(255) NOT NULL,
    description TEXT,
    id_type_actif INTEGER NOT NULL,
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_modification DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_type_actif) REFERENCES type_actif1(id)
);

-- Table Classif1
CREATE TABLE IF NOT EXISTS classif1 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code VARCHAR(50) UNIQUE NOT NULL,
    nom VARCHAR(255) NOT NULL,
    description TEXT,
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_modification DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table SousClassif1
CREATE TABLE IF NOT EXISTS sous_classif1 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code VARCHAR(50) UNIQUE NOT NULL,
    nom VARCHAR(255) NOT NULL,
    description TEXT,
    id_classif INTEGER NOT NULL,
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_modification DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_classif) REFERENCES classif1(id)
);

-- Table Titre
CREATE TABLE IF NOT EXISTS titre (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code VARCHAR(50) UNIQUE NOT NULL,
    nom VARCHAR(255) NOT NULL,
    description TEXT,
    cusip VARCHAR(50) UNIQUE,
    isin VARCHAR(50) UNIQUE,
    ticker VARCHAR(50),
    emetteur VARCHAR(255),
    id_type_actif INTEGER,
    id_sous_type_actif INTEGER,
    id_secteur INTEGER,
    id_classif INTEGER,
    id_sous_classif INTEGER,
    id_pays INTEGER,
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_modification DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_type_actif) REFERENCES type_actif1(id),
    FOREIGN KEY (id_sous_type_actif) REFERENCES sous_type_actif1(id),
    FOREIGN KEY (id_secteur) REFERENCES secteur(id),
    FOREIGN KEY (id_classif) REFERENCES classif1(id),
    FOREIGN KEY (id_sous_classif) REFERENCES sous_classif1(id),
    FOREIGN KEY (id_pays) REFERENCES pays(id)
);

-- Table Indice
CREATE TABLE IF NOT EXISTS indice (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code VARCHAR(50) UNIQUE NOT NULL,
    nom VARCHAR(255) NOT NULL,
    description TEXT,
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_modification DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table Fonds
CREATE TABLE IF NOT EXISTS fonds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code VARCHAR(50) UNIQUE NOT NULL,
    nom VARCHAR(255) NOT NULL,
    description TEXT,
    type_fonds VARCHAR(20) NOT NULL CHECK (type_fonds IN ('simple', 'portefeuille')),
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_modification DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tables de liaison
CREATE TABLE IF NOT EXISTS fonds_gestionnaire (
    id_fonds INTEGER,
    id_gestionnaire INTEGER,
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_modification DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_fonds, id_gestionnaire),
    FOREIGN KEY (id_fonds) REFERENCES fonds(id),
    FOREIGN KEY (id_gestionnaire) REFERENCES gestionnaire(id)
);

CREATE TABLE IF NOT EXISTS fonds_indice (
    id_fonds INTEGER,
    id_indice INTEGER,
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_modification DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_fonds, id_indice),
    FOREIGN KEY (id_fonds) REFERENCES fonds(id),
    FOREIGN KEY (id_indice) REFERENCES indice(id)
);

-- Tables de composition
CREATE TABLE IF NOT EXISTS composition_fonds_gestionnaire (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    id_fonds INTEGER NOT NULL,
    id_gestionnaire INTEGER NOT NULL,
    id_titre INTEGER NOT NULL,
    id_devise INTEGER NOT NULL,
    id_pays INTEGER NOT NULL,
    quantite REAL,
    prix REAL,
    valeur_marchande REAL,
    accrued REAL,
    dividende REAL,
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_modification DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_fonds) REFERENCES fonds(id),
    FOREIGN KEY (id_gestionnaire) REFERENCES gestionnaire(id),
    FOREIGN KEY (id_titre) REFERENCES titre(id),
    FOREIGN KEY (id_devise) REFERENCES devise(id),
    FOREIGN KEY (id_pays) REFERENCES pays(id)
);

CREATE TABLE IF NOT EXISTS composition_portefeuille_gestionnaire (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    id_portefeuille INTEGER NOT NULL,
    id_gestionnaire INTEGER NOT NULL,
    id_titre INTEGER NOT NULL,
    id_devise INTEGER NOT NULL,
    id_pays INTEGER NOT NULL,
    quantite REAL,
    prix REAL,
    valeur_marchande REAL,
    accrued REAL,
    dividende REAL,
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_modification DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_portefeuille) REFERENCES fonds(id),
    FOREIGN KEY (id_gestionnaire) REFERENCES gestionnaire(id),
    FOREIGN KEY (id_titre) REFERENCES titre(id),
    FOREIGN KEY (id_devise) REFERENCES devise(id),
    FOREIGN KEY (id_pays) REFERENCES pays(id)
);

CREATE TABLE IF NOT EXISTS composition_indice (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    id_indice INTEGER NOT NULL,
    id_titre INTEGER NOT NULL,
    id_devise INTEGER NOT NULL,
    id_pays INTEGER NOT NULL,
    quantite REAL,
    prix REAL,
    valeur_marchande REAL,
    accrued REAL,
    dividende REAL,
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_modification DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_indice) REFERENCES indice(id),
    FOREIGN KEY (id_titre) REFERENCES titre(id),
    FOREIGN KEY (id_devise) REFERENCES devise(id),
    FOREIGN KEY (id_pays) REFERENCES pays(id)
);

-- Création des index
CREATE INDEX IF NOT EXISTS idx_gestionnaire_code ON gestionnaire(code);
CREATE INDEX IF NOT EXISTS idx_region_code ON region1(code);
CREATE INDEX IF NOT EXISTS idx_pays_code ON pays(code);
CREATE INDEX IF NOT EXISTS idx_devise_code ON devise(code);
CREATE INDEX IF NOT EXISTS idx_secteur_code ON secteur(code);
CREATE INDEX IF NOT EXISTS idx_type_actif_code ON type_actif1(code);
CREATE INDEX IF NOT EXISTS idx_sous_type_actif_code ON sous_type_actif1(code);
CREATE INDEX IF NOT EXISTS idx_classif_code ON classif1(code);
CREATE INDEX IF NOT EXISTS idx_sous_classif_code ON sous_classif1(code);
CREATE INDEX IF NOT EXISTS idx_titre_code ON titre(code);
CREATE INDEX IF NOT EXISTS idx_titre_cusip ON titre(cusip);
CREATE INDEX IF NOT EXISTS idx_titre_isin ON titre(isin);
CREATE INDEX IF NOT EXISTS idx_indice_code ON indice(code);
CREATE INDEX IF NOT EXISTS idx_fonds_code ON fonds(code);

-- Index sur les clés étrangères
CREATE INDEX IF NOT EXISTS idx_pays_region ON pays(id_region);
CREATE INDEX IF NOT EXISTS idx_pays_devise ON pays(id_devise);
CREATE INDEX IF NOT EXISTS idx_sous_type_actif_type ON sous_type_actif1(id_type_actif);
CREATE INDEX IF NOT EXISTS idx_sous_classif_classif ON sous_classif1(id_classif);
CREATE INDEX IF NOT EXISTS idx_titre_relations ON titre(id_type_actif, id_sous_type_actif, id_secteur, id_classif, id_sous_classif, id_pays);

-- Index sur les compositions
CREATE INDEX IF NOT EXISTS idx_comp_fonds_date ON composition_fonds_gestionnaire(date);
CREATE INDEX IF NOT EXISTS idx_comp_fonds_relations ON composition_fonds_gestionnaire(id_fonds, id_gestionnaire, id_titre);
CREATE INDEX IF NOT EXISTS idx_comp_port_date ON composition_portefeuille_gestionnaire(date);
CREATE INDEX IF NOT EXISTS idx_comp_port_relations ON composition_portefeuille_gestionnaire(id_portefeuille, id_gestionnaire, id_titre);
CREATE INDEX IF NOT EXISTS idx_comp_indice_date ON composition_indice(date);
CREATE INDEX IF NOT EXISTS idx_comp_indice_relations ON composition_indice(id_indice, id_titre);

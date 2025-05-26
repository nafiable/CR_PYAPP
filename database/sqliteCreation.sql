-- Script de création des tables pour SQLite

CREATE TABLE TestTable (
 id INTEGER PRIMARY KEY,
 nom TEXT
);

CREATE TABLE Region (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 code TEXT UNIQUE NOT NULL,
 nom TEXT NOT NULL
);

CREATE TABLE Devise (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 code TEXT UNIQUE NOT NULL,
 nom TEXT NOT NULL,
 idPays INTEGER -- Cette colonne est pour la relation Devise-Pays, mais la clé étrangère sera dans la table Pays pour une relation 1:N (un pays a une devise)
 -- Si une devise est liée à un seul pays, la clé étrangère serait ici :
 -- FOREIGN KEY (idPays) REFERENCES Pays(id)
);

CREATE TABLE Pays (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 code TEXT UNIQUE NOT NULL,
 nom TEXT NOT NULL,
 idRegion INTEGER,
 continent TEXT,
 idDevise INTEGER,
 FOREIGN KEY (idRegion) REFERENCES Region(id),
 FOREIGN KEY (idDevise) REFERENCES Devise(id)
);

CREATE TABLE Secteur (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 codeGics TEXT,
 codeBics TEXT,
 nom TEXT NOT NULL
);

CREATE TABLE TypeActif1 (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 type TEXT UNIQUE NOT NULL
);

CREATE TABLE SousTypeActif1 (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 idTypeAcif1 INTEGER,
 nom TEXT NOT NULL,
 FOREIGN KEY (idTypeAcif1) REFERENCES TypeActif1(id)
);

CREATE TABLE Classif1 (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 nom TEXT UNIQUE NOT NULL
);

CREATE TABLE SousClassif1 (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 idClassif1 INTEGER,
 nom TEXT NOT NULL,
 FOREIGN KEY (idClassif1) REFERENCES Classif1(id)
);

CREATE TABLE Titre (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 nom TEXT NOT NULL,
 cusip TEXT,
 isin TEXT UNIQUE,
 ticker TEXT,
 emetteur TEXT,
 idTypeTitre1 INTEGER,
 idSousTypeTitre1 INTEGER,
 idTypeTitre2 INTEGER, -- Supposons un autre type de titre si TypeTitre1 ne suffit pas
 idSecteur INTEGER,
 idClassification1 INTEGER,
 idSousClassification1 INTEGER,
 classification2 TEXT, -- Supposons une autre classification textuelle
 idNotation INTEGER, -- Supposons une table Notation
 idPays INTEGER,
 FOREIGN KEY (idSecteur) REFERENCES Secteur(id),
 FOREIGN KEY (idClassification1) REFERENCES Classif1(id),
 FOREIGN KEY (idSousClassification1) REFERENCES SousClassif1(id),
 -- Ajoutez les clés étrangères pour TypeTitre1, SousTypeTitre1, TypeTitre2, idNotation, idPays si ces tables existent
 -- FOREIGN KEY (idTypeTitre1) REFERENCES TypeTitre1(id),
 -- FOREIGN KEY (idSousTypeTitre1) REFERENCES SousTypeTitre1(id),
 -- FOREIGN KEY (idPays) REFERENCES Pays(id)
);

CREATE TABLE Indice (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 nom TEXT UNIQUE NOT NULL
);

-- Les tables de composition seront ajoutées ensuite.

CREATE TABLE CompositionFondsGestionnaire (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 date TEXT,
 id_fonds INTEGER,
 id_gestionnaire INTEGER,
 id_Titre INTEGER,
 id_devise INTEGER,
 id_pays INTEGER,
 quantite REAL,
 prix REAL,
 valeur_marchande REAL,
 accrued REAL,
 dividende REAL,
 FOREIGN KEY (id_fonds) REFERENCES Fonds(id),
 FOREIGN KEY (id_gestionnaire) REFERENCES Gestionnaires(id),
 FOREIGN KEY (id_Titre) REFERENCES Titre(id),
 FOREIGN KEY (id_devise) REFERENCES Devise(id),
 FOREIGN KEY (id_pays) REFERENCES Pays(id)
);

CREATE TABLE CompositionIndice (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 date TEXT,
 id_indice INTEGER,
 id_Titre INTEGER,
 poids REAL,
 FOREIGN KEY (id_indice) REFERENCES Indice(id),
 FOREIGN KEY (id_Titre) REFERENCES Titre(id)
);

CREATE TABLE CompositionPortefeuilleGestionnaire (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 date TEXT,
 id_fonds_portefeuille INTEGER,
 id_gestionnaire INTEGER,
 id_Titre INTEGER,
 id_devise INTEGER,
 id_pays INTEGER,
 quantite REAL,
 prix REAL,
 valeur_marchande REAL,
 accrued REAL,
 dividende REAL,
 FOREIGN KEY (id_fonds_portefeuille) REFERENCES Fonds(id),
 FOREIGN KEY (id_gestionnaire) REFERENCES Gestionnaires(id),
 FOREIGN KEY (id_Titre) REFERENCES Titre(id),
 FOREIGN KEY (id_devise) REFERENCES Devise(id),
 FOREIGN KEY (id_pays) REFERENCES Pays(id)
);

CREATE TABLE FondsGestionnaire (
 id_fonds INTEGER,
 id_gestionnaire INTEGER,
 date_debut_affectation TEXT,
 date_fin_affectation TEXT,
 PRIMARY KEY (id_fonds, id_gestionnaire) -- Composite primary key
);

CREATE TABLE CompositionIndice (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 date TEXT,
 id_indice INTEGER,
 id_Titre INTEGER,
 poids REAL,
 FOREIGN KEY (id_indice) REFERENCES Indice(id),
 FOREIGN KEY (id_Titre) REFERENCES Titre(id)
);

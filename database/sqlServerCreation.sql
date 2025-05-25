-- Script de création des tables pour SQL Server

CREATE TABLE TestTable (
 id INT PRIMARY KEY,
    nom VARCHAR(255)
);

CREATE TABLE Region (
 id INT PRIMARY KEY IDENTITY(1,1),
 code VARCHAR(50) UNIQUE NOT NULL,
 nom VARCHAR(255) NOT NULL
);

CREATE TABLE Devise (
 id INT PRIMARY KEY IDENTITY(1,1),
 code VARCHAR(10) UNIQUE NOT NULL,
 nom VARCHAR(50) NOT NULL,
 idPays INT -- Cette colonne est pour la relation Devise-Pays, mais la clé étrangère sera dans la table Pays pour une relation 1:N (un pays a une devise)
);

CREATE TABLE Pays (
 id INT PRIMARY KEY IDENTITY(1,1),
 code VARCHAR(10) UNIQUE NOT NULL,
 nom VARCHAR(255) NOT NULL,
 idRegion INT,
 continent VARCHAR(100),
 idDevise INT,
 FOREIGN KEY (idRegion) REFERENCES Region(id),
 FOREIGN KEY (idDevise) REFERENCES Devise(id)
);

-- Mettre à jour la table Devise pour ajouter la contrainte de clé étrangère si nécessaire, ou ajuster le modèle si la relation est 1:1
-- ALTER TABLE Devise ADD CONSTRAINT FK_Devise_Pays FOREIGN KEY (idPays) REFERENCES Pays(id); -- Si une devise est liée à un seul pays

CREATE TABLE Secteur (
 id INT PRIMARY KEY IDENTITY(1,1),
 codeGics VARCHAR(50),
 codeBics VARCHAR(50),
 nom VARCHAR(255) NOT NULL
);

CREATE TABLE TypeActif1 (
 id INT PRIMARY KEY IDENTITY(1,1),
 type VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE SousTypeActif1 (
 id INT PRIMARY KEY IDENTITY(1,1),
 idTypeAcif1 INT,
 nom VARCHAR(255) NOT NULL,
 FOREIGN KEY (idTypeAcif1) REFERENCES TypeActif1(id)
);

CREATE TABLE Classif1 (
 id INT PRIMARY KEY IDENTITY(1,1),
 nom VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE SousClassif1 (
 id INT PRIMARY KEY IDENTITY(1,1),
 idClassif1 INT,
 nom VARCHAR(255) NOT NULL,
 FOREIGN KEY (idClassif1) REFERENCES Classif1(id)
);

CREATE TABLE Titre (
 id INT PRIMARY KEY IDENTITY(1,1),
 nom VARCHAR(255) NOT NULL,
 cusip VARCHAR(50),
 isin VARCHAR(50) UNIQUE,
 ticker VARCHAR(50),
 emetteur VARCHAR(255),
 idTypeTitre1 INT,
 idSousTypeTitre1 INT,
 idTypeTitre2 INT, -- Supposons un autre type de titre si TypeTitre1 ne suffit pas
 idSecteur INT,
 idClassification1 INT,
 idSousClassification1 INT,
 classification2 VARCHAR(255), -- Supposons une autre classification textuelle
 idNotation INT, -- Supposons une table Notation
 idPays INT,
 FOREIGN KEY (idSecteur) REFERENCES Secteur(id),
 FOREIGN KEY (idClassification1) REFERENCES Classif1(id),
 FOREIGN KEY (idSousClassification1) REFERENCES SousClassif1(id),
 -- Ajoutez les clés étrangères pour TypeTitre1, SousTypeTitre1, TypeTitre2, idNotation, idPays si ces tables existent
 -- FOREIGN KEY (idTypeTitre1) REFERENCES TypeTitre1(id),
 -- FOREIGN KEY (idSousTypeTitre1) REFERENCES SousTypeTitre1(id),
 -- FOREIGN KEY (idPays) REFERENCES Pays(id)
);

CREATE TABLE Indice (
 id INT PRIMARY KEY IDENTITY(1,1),
 nom VARCHAR(255) UNIQUE NOT NULL
);

-- Les tables de composition seront ajoutées ensuite.

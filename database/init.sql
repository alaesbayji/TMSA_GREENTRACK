-- Création de la base de données
CREATE DATABASE tmsa_greentrack;

\c tmsa_greentrack;

-- Création des tables principales
CREATE TABLE utilisateur (
    id SERIAL PRIMARY KEY,
    nom_complet VARCHAR(100),
    email VARCHAR(100) UNIQUE NOT NULL,
    mot_de_passe VARCHAR(100) NOT NULL,
    role VARCHAR(50),
    date_creation TIMESTAMP DEFAULT NOW()
);

CREATE TABLE entreprise (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(150),
    secteur_dominant VARCHAR(100),
    montant_investissement NUMERIC,
    nombre_emploi INT,
    responsable_id INT REFERENCES utilisateur(id)
);

CREATE TABLE milieu (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100),
    description TEXT
);

CREATE TABLE engagement (
    id SERIAL PRIMARY KEY,
    entreprise_id INT REFERENCES entreprise(id),
    milieu_id INT REFERENCES milieu(id),
    frequence_suivi VARCHAR(50),
    responsable_id INT REFERENCES utilisateur(id),
    date_creation TIMESTAMP DEFAULT NOW()
);

-- Exemple de données initiales
INSERT INTO utilisateur (nom_complet, email, mot_de_passe, role)
VALUES ('Admin TMSA', 'admin@tmsa.ma', 'password123', 'ADMIN');

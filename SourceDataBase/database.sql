
-----------| Création des tables |-----------
CREATE TABLE TypeVoie(
IdTV serial PRIMARY KEY,
nom varchar(25),
description varchar(999)
);


CREATE TABLE difficulte(
FR varchar(2) PRIMARY KEY,
AM varchar(5),
EN varchar(4)
);

CREATE TABLE localite(
CodePostal varchar(5) PRIMARY KEY,
nom varchar(45)
);



CREATE TABLE SiteEsca (
    IdSE serial PRIMARY KEY,
    nom varchar(45),
    CodePostal varchar(5),
    FOREIGN KEY (CodePostal) REFERENCES localite(CodePostal)
);

CREATE TABLE Voie(
IdV serial PRIMARY KEY,
nom varchar(25),
longueur int,
idTV int,
FR varchar(2),
IdSE int,
FOREIGN KEY (IDTV) REFERENCES TYPEVOIE(IDTV),
FOREIGN KEY (FR) REFERENCES difficulte(FR),
FOREIGN KEY (IdSe) REFERENCES SiteEsca(IdSe)
);


CREATE TABLE deboucheVers(
IdV1 int, 
IdV2 int,
Primary KEY (IdV1, IdV2),
FOREIGN KEY (idV1) REFERENCES Voie(IdV),
FOREIGN KEY (idV2) REFERENCES Voie(IdV)
);

CREATE TABLE typeEsca(
IdTE serial PRIMARY KEY,
nom varchar(25),
description varchar(999)
);



CREATE TABLE CORDEE (
idcordee serial PRIMARY KEY
);

CREATE TABLE grimper(
IdTE int,
IdCordee int,
IdV int,
dateg date,
PRIMARY KEY (IdTE,IdCordee, IdV),
FOREIGN KEY (IdTE) REFERENCES typeEsca(IdTE),
FOREIGN KEY (Idcordee) REFERENCES cordee(Idcordee),
FOREIGN KEY (IdV) REFERENCES voie(IdV)
);

CREATE TABLE utilisateur(
mail varchar(320) PRIMARY KEY,
mdp varchar(60),
nom varchar(25),
prenom varchar(25),
fr varchar(2),
FOREIGN KEY (fr) REFERENCES difficulte(fr)
);

CREATE TABLE PartieC(
idCordee int ,
mail varchar(320),
PRIMARY KEY (idcordee,mail),
FOREIGN KEY (idcordee) REFERENCES cordee(idcordee),
FOREIGN KEY (mail) REFERENCES utilisateur(mail)
);

CREATE TABLE proposition(
IdPropo serial PRIMARY KEY,
description varchar(999),
datep date,
nb_max int CHECK (nb_max>0),
mail varchar(320),
fr varchar(2),
idse integer,
FOREIGN KEY (mail) REFERENCES utilisateur(mail),
FOREIGN KEY (fr) REFERENCES difficulte(FR),
FOREIGN KEY (idse) REFERENCES siteesca(idse)
);

CREATE TABLE participe(
mail varchar(320),
Idpropo int,
PRIMARY KEY (mail,Idpropo),
FOREIGN KEY (mail) REFERENCES utilisateur(mail),
FOREIGN KEY (Idpropo) REFERENCES proposition(Idpropo)
);

CREATE TABLE EstGuideDe(
mail varchar(320),
Codepostal varchar(5),
PRIMARY KEY (mail,codepostal),
FOREIGN KEY (mail) REFERENCES utilisateur(mail),
FOREIGN KEY (codepostal) references localite(codepostal)
);

-----------| Création des vues |-----------

--Top 5 site esca dans la dernière année 
CREATE MATERIALIZED VIEW topFiveSiteEsca AS (
    WITH lstparticipe AS (
        SELECT proposition.Idpropo, COUNT(participe.Idpropo) as nb_participation, proposition.idse FROM proposition
        JOIN participe
        ON participe.Idpropo = proposition.Idpropo
        AND proposition.datep > NOW() - interval '1 year'
        GROUP BY (proposition.Idpropo)
    )
    SELECT idse, SUM(nb_participation) as nb_climber_last_year FROM lstparticipe
    GROUP BY (idse, nb_participation)
    ORDER BY lstparticipe.nb_participation DESC
    LIMIT 5
);

--Liste des guides inactif entre maintenant et 1 ans en arrière
CREATE VIEW listInactiveGuides AS (
    SELECT estguidede.mail, nom prenom FROM EstGuideDe NATURAL JOIN utilisateur
    WHERE EstGuideDe.mail NOT IN(
        SELECT utilisateur.mail
        FROM utilisateur NATURAL JOIN EstGuideDe JOIN proposition
        ON EstGuideDe.mail = proposition.mail
        AND proposition.datep > NOW() - interval '1 year'
    )
);
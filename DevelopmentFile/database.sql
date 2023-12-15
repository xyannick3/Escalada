DROP TABLE IF EXISTS CORDEE CASCADE;
DROP TABLE IF EXISTS deboucheVers CASCADE;
DROP TABLE IF EXISTS difficulte CASCADE;
DROP TABLE IF EXISTS EstGuideDe CASCADE;
DROP TABLE IF EXISTS grimper CASCADE;
DROP TABLE IF EXISTS localite CASCADE;
DROP TABLE IF EXISTS participe CASCADE;
DROP TABLE IF EXISTS PartieC CASCADE;
DROP TABLE IF EXISTS proposition CASCADE;
DROP TABLE IF EXISTS siteesca CASCADE;
DROP TABLE IF EXISTS typeEsca CASCADE;
DROP TABLE IF EXISTS TypeVoie CASCADE;
DROP TABLE IF EXISTS utilisateur CASCADE;
DROP TABLE IF EXISTS voie CASCADE;


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
idcordee serial PRIMARY KEY,
nomcordee varchar(20)
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

INSERT INTO difficulte VALUES ('1','5.1','Easy');
INSERT INTO difficulte VALUES ('2','5.3','M');
INSERT INTO difficulte VALUES ('3','5.4','D');
INSERT INTO difficulte VALUES ('4','5.5','HVD');
INSERT INTO difficulte VALUES ('5a','5.6','MS');
INSERT INTO difficulte VALUES ('5b','5.7','VS');
INSERT INTO difficulte VALUES ('5c','5.8','HVS');
INSERT INTO difficulte VALUES ('6a','5.9','E1');
INSERT INTO difficulte VALUES ('6b','5.10c','E2');
INSERT INTO difficulte VALUES ('6c','5.11a','E3');
INSERT INTO difficulte VALUES ('7a','5.11d','E4');
INSERT INTO difficulte VALUES ('7b','5.12b','E5');
INSERT INTO difficulte VALUES ('7c','5.12d','E6');
INSERT INTO difficulte VALUES ('8a','5.13b','E7');
INSERT INTO difficulte VALUES ('8b','5.13d','E8');
INSERT INTO difficulte VALUES ('8c','5.14b','E9');
INSERT INTO difficulte VALUES ('9a','5.14d','E10');
INSERT INTO difficulte VALUES ('9b','5.15b','E11');
INSERT INTO difficulte VALUES ('9c','5.15d','E12');


INSERT INTO localite VALUES ('77300','Fontainebleau');
INSERT INTO localite VALUES ('24520', 'Mouleydier');
INSERT INTO localite VALUES ('13009','Marseille 9eme arroundissement');

INSERT INTO localite VALUES ('42920','Chalmazel');


INSERT INTO utilisateur VALUES ('leroux.leo32@yahoo.fr','$2b$12$qWWjsfYGgIBd9tTYUFa5w.9N0ccjsiHZ5miSon16h.OrmzVhIb8..','leroux','leo','9c');
INSERT INTO utilisateur VALUES ('guerin.oceane30@live.com','$2b$12$Rly3TJsiPm1Vb/INbEK7feA3aN.Bfby3uoVeQi0EArP/lom3L0/sa','guerin','oceane','9b');
INSERT INTO utilisateur VALUES ('noah67@hotmail.com','$2b$12$6rvRrfdsPm1sIEel/OQUruUCcLaZ8TsY9eAOPpKeHgjg0bRd9/mAa','guerin','noah','5a');
INSERT INTO utilisateur VALUES ('adam74@laposte.net','$2b$12$okEobfm9R8UnfI8h8lpq9uIVpWtZeLSaELz0U5VHei3I5KmeQvkZO','laurent','adam','8b');
INSERT INTO utilisateur VALUES ('perez.leo38@live.com','$2b$12$xxtVvM7qvrDH/VG7SdT/.uD61/pKsPSPd/wtBO75OGuPFY6jYlykC','perez','leo','2');
INSERT INTO utilisateur VALUES ('noah55@hotmail.com','$2b$12$eATN85UeLxm0OBw34DAkkOvi6Pmnh71LUPLwFFCnRnIW754yjHl12','langlois','noah','7b');
INSERT INTO utilisateur VALUES ('moreau.lucas35@gmail.com','$2b$12$zndHNBS3Wn6UjD8DJpIWcOXKVgRVyjbxowrZEBaDHxzLp7EJrM38.','moreau','lucas','5b');
INSERT INTO utilisateur VALUES ('blanc.jade72@yahoo.fr','$2b$12$.3szFD6B.coyUWHOHvKKV.zCIhk3XWimML1AvaSL9o3pzIXjs.5UO','blanc','jade','2');
INSERT INTO utilisateur VALUES ('dupuy.adam28@live.com','$2b$12$H.yeGik7WYXKfhbhyPGTouvJFvqNVLanOHJL59FTlimGwWgtwYeN6','dupuy','adam','7c');
INSERT INTO utilisateur VALUES ('amy66@live.com','$2b$12$bF6N5g9YSV25afu9jDj5Reo6dVePVRU1hReY0JyResQBbf1G5qfnu','david','amy','9c');
INSERT INTO utilisateur VALUES ('vincent.lucas64@gmail.com','$2b$12$O9rXdJ7bz8FIV7YVrdLbpeHcaaCA0PUn6B.rqOGK/HaS2q/dXtzAW','vincent','lucas','5b');
INSERT INTO utilisateur VALUES ('anna54@live.com','$2b$12$auUSEOX5t.F1kDO5ztOjFOksbN0wFmEZTOklSGWlCfaUQtZ/IJhji','dupuy','anna','9b');
INSERT INTO utilisateur VALUES ('alex57@laposte.net','$2b$12$Y70TxqiuJDGvA/Xow3Tgs.Zy6LblLYZr16wtkxjwV7GhftsTAYZ7K','lopez','alex','6c');
INSERT INTO utilisateur VALUES ('guerin.mael93@laposte.net','$2b$12$Lt7yNYFvpHj8cYo7BQe/Qujhze1XHFmebFSWAHrK7IFfUCqqYHv.K','guerin','mael','6c');
INSERT INTO utilisateur VALUES ('jean.amy20@laposte.net','$2b$12$Dt.FoO3mNltv5hsvl4bBd.DwguPXH34r2nDkPS13MCHiq90segSOK','jean','amy','8c');
INSERT INTO utilisateur VALUES ('deschamps.leo8@yahoo.fr','$2b$12$XT5q2.w40gTTRZy8/S0NxuhRu4y.jPI5XHZw6teLBwUXWqfIuUkx2','deschamps','leo','8c');
INSERT INTO utilisateur VALUES ('jean.gabriel17@yahoo.fr','$2b$12$R9UhaEjLwmz5QKks8fx/7./UXAEV2iMfVR3J/F03g9BogZuox8unO','jean','gabriel','9a');
INSERT INTO utilisateur VALUES ('romy84@laposte.net','$2b$12$CfQnVfg2b/AdNeDR7UmowOG0xyBLuyyrmtIUWze3YqkfPLSep96jm','lopez','romy','8b');
INSERT INTO utilisateur VALUES ('david.emma29@gmail.com','$2b$12$dzWIXFkF/0fCVeGUXUct6ui6bqKpA2bCNhcETfADEhemo95K0FZvG','david','emma','9c');
INSERT INTO utilisateur VALUES ('simon.alex8@yahoo.fr','$2b$12$W5w9wYccUBmguqJcsXeJTuGO0bok./hFWIfcB5ALKBDGHPk7RYVN2','simon','alex','3');
INSERT INTO utilisateur VALUES ('noah81@yahoo.fr','$2b$12$9xdfsXv0TxR3WQOUvXd2zO9p0l0sqQ8K841WHoKL6WNnl3uxGRFg.','sanchez','noah','8c');
INSERT INTO utilisateur VALUES ('louise56@laposte.net','$2b$12$ojvoSgMpRBgpqrTjvu3qUeEi/eXry7bNiYw9GXoySVOLftnEvN7Yy','dupuy','louise','8b');
INSERT INTO utilisateur VALUES ('oceane91@hotmail.com','$2b$12$reFxgq12ifofOSs33IxA9uLuCubwd.TxQgNT6iu7qBFeXQb5c7dM6','lopez','oceane','6a');
INSERT INTO utilisateur VALUES ('louis58@laposte.net','$2b$12$YfsPteTrFigbHWGBcaOwLOM6IvGOaNPCS3IYZLnqQQcg4kXW/I0XC','laurent','louis','3');
INSERT INTO utilisateur VALUES ('blanc.rose70@gmail.com','$2b$12$DqjUg5AviX5f9P/nSJ3sAOvPftQh3jdqW0.Cn7KndFOa2b/NwuexG','blanc','rose','8a');
INSERT INTO utilisateur VALUES ('alba53@gmail.com','$2b$12$6pCVLLIaQfngPhoSW0ZmjOvp7sWgLbd8EOcb/6tJvzmhrSMi3s1Rq','garnier','alba','8b');
INSERT INTO utilisateur VALUES ('lefevre.louise72@hotmail.com','$2b$12$GGfnZKI9WiWpkwDjQt./zerclALqzmKrnfRttVc9Xgf2wmKLW1/dK','lefevre','louise','5c');
INSERT INTO utilisateur VALUES ('martin.alice96@laposte.net','$2b$12$4fN9ATOVs.BSsgGHIQ.jv.FycZry0si9XspfQ7arg3IWqynq.buhO','martin','alice','9a');
INSERT INTO utilisateur VALUES ('lopez.emma11@yahoo.fr','$2b$12$X3aO/3RcdmPZQtyjW20..eLY0OUWGApegjnpqG/2XUamnJ.usaRJm','lopez','emma','7c');
INSERT INTO utilisateur VALUES ('alice88@gmail.com','$2b$12$annL6lmSbJWQnl6gB3dFA.tNZbX68CJdCQv.Mt8P/zl1Roj.yG/K2','durand','alice','6b');



INSERT INTO SITEESCA (nom, CodePostal) VALUES ('Circuit de Bas Cuivrer','77300');
INSERT INTO SITEESCA (nom, CodePostal) VALUES ('La Canche aux merciers','77300');
INSERT INTO SITEESCA (nom, CodePostal) VALUES ('Rocher Canon','77300');

INSERT INTO SITEESCA (nom, CodePostal) VALUES ('Apremont','77300');
INSERT INTO SITEESCA (nom, CodePostal) VALUES ('Cul du Chien', '77300');
INSERT INTO SITEESCA (nom, CodePostal) VALUES ('Paradis', '77300'); 

INSERT INTO SITEESCA (nom, CodePostal) VALUES ('Cuisiniere','77300');
INSERT INTO SITEESCA (nom, CodePostal) VALUES ('Isatis','77300');
INSERT INTO SITEESCA (nom, CodePostal) VALUES ('Le 95 2','77300');

INSERT INTO SITEESCA (nom, CodePostal) VALUES ('Le Roc de L Olme','42920');
INSERT INTO TYPEVOIE (nom, description) VALUES ('Verticale','Voie en angle de 90 degres avec le sol.');
INSERT INTO TYPEVOIE (nom, description) VALUES ('Dalle','Voie en inclinaison positive.');
INSERT INTO TYPEVOIE (nom, description) VALUES ('Devers','Voie en inclinaison negative.');
INSERT INTO TYPEVOIE (nom, description) VALUES ('Toit','Paroi horizontale parallele au sol.');
INSERT INTO TYPEVOIE (nom, description) VALUES ('Cheminee','Deux parois face a face.');
INSERT INTO TYPEVOIE (nom, description) VALUES ('Diedre','Deux parois cote a cote qui font un angle de 90 degrees.');
INSERT INTO TYPEVOIE (nom, description) VALUES ('Marche','De la marche');
 
INSERT INTO VOIE (nom,longueur,IDTV,FR,IdSE) VALUES ('Bloc1',1,1,'1',1);
INSERT INTO VOIE (nom,longueur,IDTV,FR,IdSE) VALUES ('Bloc2',2,2,'2',1);
INSERT INTO VOIE (nom,longueur,IDTV,FR,IdSE) VALUES ('Pierre pendante',4,3,'4',1);

INSERT INTO VOIE (nom,longueur,IDTV,FR,IdSE) VALUES ('Chemin sablee',500,7,'1',2);
INSERT INTO VOIE (nom,longueur,IDTV,FR,IdSE) VALUES ('La grimpade',50,1,'3',2);

INSERT INTO VOIE (nom,longueur,IDTV,FR,IdSE) VALUES ('La marche au canon',3000,7,'1',3);
INSERT INTO VOIE (nom,longueur,IDTV,FR,IdSE) VALUES ('Le mur','50',1,'4',3);



INSERT INTO VOIE (nom,longueur,IDTV,FR,IdSE) VALUES ('Route de Barbizon',500,7,'1',4);
INSERT INTO VOIE (nom,longueur,IDTV,FR,IdSE) VALUES ('La flèche',50,3,'5b',4);

INSERT INTO VOIE (nom,longueur,IDTV,FR,IdSE) VALUES ('Le Chien',100,4,'6a',5);
INSERT INTO VOIE (nom,longueur,IDTV,FR,IdSE) VALUES ('Le Sableux',100,4,'6a',5);

INSERT INTO VOIE (nom,longueur,IDTV,FR,IdSE) VALUES ('Everest',8,1,'6c',6);
INSERT INTO VOIE (nom,longueur,IDTV,FR,IdSE) VALUES ('Olympe',8,2,'6c',6);

INSERT INTO VOIE (nom,longueur,IDTV,FR,IdSE) VALUES ('La soupe',10,1,'7a',7);
INSERT INTO VOIE (nom,longueur,IDTV,FR,IdSE) VALUES ('Socoupe',10,1,'7b',7);
INSERT INTO VOIE (nom,longueur,IDTV,FR,IdSE) VALUES ('Dessert',10,1,'7c',7);

INSERT INTO VOIE (nom,longueur,IDTV,FR,IdSE) VALUES ('Lhumide',50,2,'7a',8);

INSERT INTO VOIE (nom,longueur,IDTV,FR,IdSE) VALUES ('La Fin', 20, 2,'7c',8);


INSERT INTO VOIE (nom,longueur,IDTV,FR,IdSE) VALUES ('Pas dlezard',20,3,'4',10);
INSERT INTO VOIE (nom,longueur,IDTV,FR,IdSE) VALUES ('Pin Up',50,5,'4',10);
INSERT INTO VOIE (nom,longueur,IDTV,FR,IdSE) VALUES ('Tango',5,3,'5b',10); 
INSERT INTO VOIE (nom,longueur,IDTV,FR,IdSE) VALUES ('Normale',50,'2','1',10);


INSERT INTO DEBOUCHEVERS (IdV1,IdV2) VALUES (1,2);
INSERT INTO DEBOUCHEVERS (IdV1,IdV2) VALUES (2,3);

INSERT INTO DEBOUCHEVERS (IdV1,IdV2) VALUES (4,5);

INSERT INTO DEBOUCHEVERS (IdV1,IdV2) VALUES (6,7);

INSERT INTO DEBOUCHEVERS (IdV1,IdV2) VALUES (8,9);

INSERT INTO DEBOUCHEVERS (IdV1,IdV2) VALUES (10,11);

INSERT INTO DEBOUCHEVERS (IdV1,IdV2) VALUES (12,13);

INSERT INTO DEBOUCHEVERS (IdV1,IdV2) VALUES (14,15);
INSERT INTO DEBOUCHEVERS (IdV1,IdV2) VALUES (15,16);


INSERT INTO DEBOUCHEVERS (IdV1,IdV2) VALUES(19,20);
INSERT INTO DEBOUCHEVERS (IdV1,IdV2) VALUES(20,21);
INSERT INTO DEBOUCHEVERS (IdV1,IdV2) VALUES(21,22);

INSERT INTO ESTGUIDEDE (mail,CodePostal) VALUES ('leroux.leo32@yahoo.fr','77300');
INSERT INTO ESTGUIDEDE (mail,CodePostal) VALUES ('guerin.oceane30@live.com','77300');
INSERT INTO ESTGUIDEDE (mail,CodePostal) VALUES ('noah67@hotmail.com','77300');
INSERT INTO ESTGUIDEDE (mail,CodePostal) VALUES ('adam74@laposte.net','77300');
INSERT INTO ESTGUIDEDE (mail,CodePostal) VALUES ('noah55@hotmail.com','42920');

INSERT INTO PROPOSITION (description,datep,nb_max,mail,fr,idse) VALUES ('Petite session tranquille au bas Cuivrer.','2023-11-16',5,'leroux.leo32@yahoo.fr','4',1);
INSERT INTO PROPOSITION (description,datep,nb_max,mail,fr,idse) VALUES ('Session au Chien.','2021-11-16',5,'guerin.oceane30@live.com','6a',5);
INSERT INTO PROPOSITION (description,datep,nb_max,mail,fr,idse) VALUES ('Session au merciers.','2023-07-09',5,'guerin.oceane30@live.com','3',2);
INSERT INTO PROPOSITION (description,datep,nb_max,mail,fr,idse) VALUES ('Session au mur','2020-09-07',5,'noah67@hotmail.com','4','3');
INSERT INTO PROPOSITION (description,datep,nb_max,mail,fr,idse) VALUES ('Apremont :)','2019-04-01',5,'adam74@laposte.net','5b','4');
INSERT INTO PROPOSITION (description,datep,nb_max,mail,fr,idse) VALUES ('Apremomt :p','2022-04-01',5,'noah55@hotmail.com','5b','4');
INSERT INTO PROPOSITION (description,datep,nb_max,mail,fr,idse) VALUES ('balade a Apremont','2023-04-01',5,'noah55@hotmail.com','5b','4');
INSERT INTO PROPOSITION (description,datep,nb_max,mail,fr,idse) VALUES ('balade','2023-06-07',5,'noah55@hotmail.com','6a',5);
INSERT INTO PROPOSITION (description,datep,nb_max,mail,fr,idse) VALUES ('promenade','2023-07-07',5,'noah55@hotmail.com','3',2);


INSERT INTO PARTICIPE (mail,IdPropo) VALUES ('simon.alex8@yahoo.fr',1);
INSERT INTO PARTICIPE (mail,IdPropo) VALUES ('noah81@yahoo.fr',1);
INSERT INTO PARTICIPE (mail,IdPropo) VALUES ('jean.gabriel17@yahoo.fr',1);

INSERT INTO PARTICIPE (mail,IdPropo) VALUES ('blanc.rose70@gmail.com',2);
INSERT INTO PARTICIPE (mail,IdPropo) VALUES ('louis58@laposte.net',2);
INSERT INTO PARTICIPE (mail,IdPropo) VALUES ('martin.alice96@laposte.net',2);

INSERT INTO PARTICIPE (mail,IdPropo) VALUES ('leroux.leo32@yahoo.fr',3);
INSERT INTO PARTICIPE (mail,IdPropo) VALUES ('noah55@hotmail.com',3);
INSERT INTO PARTICIPE (mail,IdPropo) VALUES ('amy66@live.com',3);
INSERT INTO PARTICIPE (mail,IdPropo) VALUES ('guerin.oceane30@live.com',3);
INSERT INTO PARTICIPE (mail,IdPropo) VALUES ('deschamps.leo8@yahoo.fr',3);

INSERT INTO PARTICIPE (mail,IdPropo) VALUES ('deschamps.leo8@yahoo.fr',4);
INSERT INTO PARTICIPE (mail,IdPropo) VALUES ('guerin.oceane30@live.com',4);
INSERT INTO PARTICIPE (mail,IdPropo) VALUES ('noah55@hotmail.com',4);
INSERT INTO PARTICIPE (mail,IdPropo) VALUES ('noah67@hotmail.com',4);
INSERT INTO PARTICIPE (mail,IdPropo) VALUES ('blanc.jade72@yahoo.fr',4);

INSERT INTO PARTICIPE (mail,IdPropo) VALUES ('deschamps.leo8@yahoo.fr',5);
INSERT INTO PARTICIPE (mail,IdPropo) VALUES ('jean.gabriel17@yahoo.fr',5);

INSERT INTO PARTICIPE (mail,IdPropo) VALUES ('deschamps.leo8@yahoo.fr',6);
INSERT INTO PARTICIPE (mail,IdPropo) VALUES ('perez.leo38@live.com',6);
INSERT INTO PARTICIPE (mail,IdPropo) VALUES ('jean.gabriel17@yahoo.fr',6);

INSERT INTO PARTICIPE (mail,IdPropo) VALUES ('noah67@hotmail.com',7);
INSERT INTO PARTICIPE (mail,IdPropo) VALUES ('blanc.jade72@yahoo.fr',7);
INSERT INTO PARTICIPE (mail,IdPropo) VALUES ('deschamps.leo8@yahoo.fr',7);

INSERT INTO PARTICIPE (mail,IdPropo) VALUES ('deschamps.leo8@yahoo.fr',8);

INSERT INTO PARTICIPE (mail,IdPropo) VALUES ('blanc.jade72@yahoo.fr',9);
INSERT INTO PARTICIPE (mail,IdPropo) VALUES ('deschamps.leo8@yahoo.fr',9);
INSERT INTO PARTICIPE (mail,IdPropo) VALUES ('jean.gabriel17@yahoo.fr',9);
INSERT INTO PARTICIPE (mail,IdPropo) VALUES ('vincent.lucas64@gmail.com',9);
INSERT INTO PARTICIPE (mail,IdPropo) VALUES ('dupuy.adam28@live.com',9);

INSERT INTO TYPEESCA (nom,description) VALUES ('Escalade sportive','Utilise des points d ancrage preexistants pour la protection, avec une corde d assurance.');
INSERT INTO TYPEESCA (nom,description) VALUES ('Escalade Traditionnelle', 'Les grimpeurs placent leur propre equipement de protection tout en progressant');
INSERT INTO TYPEESCA (nom,description) VALUES ('Solo Integral','Escalade sans equipement de protection, meme sans corde. Tres dangereux');
INSERT INTO TYPEESCA (nom,description) VALUES ('duo','Deux grimpeurs partagent la responsabilité de la conduite et de l assurage.');

INSERT INTO cordee (nomcordee) VALUES ('falcon');
INSERT INTO cordee (nomcordee) VALUES ('vautour');

INSERT INTO PARTIEC  (idcordee,mail) VALUES (1,'simon.alex8@yahoo.fr');
INSERT INTO PARTIEC  (idcordee,mail) VALUES (1,'noah81@yahoo.fr');
INSERT INTO PARTIEC VALUES (1,'jean.gabriel17@yahoo.fr');

INSERT INTO PARTIEC VALUES (2,'blanc.rose70@gmail.com');
INSERT INTO PARTIEC VALUES (2,'louis58@laposte.net');
INSERT INTO PARTIEC VALUES (2,'martin.alice96@laposte.net');

INSERT INTO GRIMPER (IdTE,Idcordee,IdV,dateg) VALUES (1,1,1,'2023-11-16');
INSERT INTO GRIMPER (IdTE,Idcordee,IdV,dateg) VALUES (2,2,5,'2021-11-16');



REFRESH MATERIALIZED VIEW topFiveSiteEsca;

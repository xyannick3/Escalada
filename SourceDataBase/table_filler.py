

"""
This program is used to make fake mail (for DataBase examples)
"""
from passlib.context import CryptContext
from random import choice, randint, seed
password_ctx=CryptContext(schemes=['bcrypt'])

#mail, mdp, nom, prenom, lvl
seed_value=42
seed(seed_value)
NAME_LIST = [
    "deschamps",
    "martin",
    "petit",
    "durand",
    "dubois",
    "moreau",
    "laurent",
    "simon",
    "michel",
    "lefevre",
    "roux",
    "dupont",
    "vincent",
    "guerin",
    "blanc",
    "garnier",
    "sanchez",
    "perez",
    "renault",
    "schneider",
    "leroux",
    "langlois",
    "baron",
    "vasseur",
    "carpentier",
    "dupuy",
    "jean",
    "lopez",
    "david"
]

FIRST_NAME_LIST = [
    "alex",
    "oceane",
    "gabriel",
    "leo",
    "raphael",
    "mael",
    "louis",
    "noah",
    "jules",
    "arthur",
    "adam",
    "lucas",
    "jade",
    "louise",
    "ambre",
    "alba",
    "emma",
    "rose",
    "alice",
    "romy",
    "amy",
    "anna",
    "lina"
    
]

MAIL_TYPE_LIST = [
    "gmail.com",
    "yahoo.fr",
    "laposte.net",
    "hotmail.com",
    "live.com"
]

LST_DIFFICULTE = [
    "1",
    "2",
    "3",
    "4",
    "5a",
    "5b",
    "5c",
    "6a",
    "6b",
    "6c",
    "7a",
    "7b",
    "7c",
    "8a",
    "8b",
    "8c",
    "9a",
    "9b",
    "9c"
]
def stringify(num:int)-> int:
    return str(num) if len(str(num)) > 1 else f"0{num}"

NB_profile = 30

i, mail_list, res = 0, [], ""
# Partie ci dessous gère les difficultés 
res += (
    r"""
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


""")
#Partie ci dessous gère les utilisateurs
while i<NB_profile:
    nom, prenom, birthday, departement = (
        choice(NAME_LIST),
        choice(FIRST_NAME_LIST),
        [stringify(randint(1, 29)),
         stringify(randint(1, 12)),
         str(randint(1950, 2001))],
        randint(1, 98))
    mail = choice([
        f"{nom}.{prenom}{departement}@{choice(MAIL_TYPE_LIST)}",
        f"{prenom}{str(birthday[2])[2:]}@{choice(MAIL_TYPE_LIST)}"
    ])
    mdpuncrypted = choice([
        f"{prenom}{birthday[0]}{birthday[1]}?",
        f"{prenom}{birthday[0]}{birthday[1]}!"
    ])
    mdp=password_ctx.hash(mdpuncrypted)
    if mail not in mail_list:
        mail_list.append(f"{mail},")
        res += f"INSERT INTO utilisateur VALUES ('{mail}','{mdp}','{nom}','{prenom}','{choice(LST_DIFFICULTE)}');\n"
        i += 1

res += "\n"

#Partie pour générer les sites d'escalades 
# 
#SiteEsca(IdSE,nom,CodePostal)
#Primary Key : IdSE
#Foreign Key : CodePostal de Localite
#IdSE serial,
#nom varchar(45),
#Codepostal varchar(5)
#On commence avec ceux de Fontainebleau
# source : https://www.larivieredoree.com/fr/escalade-fontainebleau
# source : https://www.rendezvousenforez.com/equipement/le-roc-de-lolme-site-descalade-chalmazel-jeansagniere/
#On pourra sans doute réutiliser le site pour des niveaux de difficultés
res+=r"""

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
"""

#Ici on ajoute les types de voies
# TypeVoie(IdTV,nom,description)
# primary key : IdTV
# IdTV serial
# nom varchar(25)
# description varchar(999)
#source : https://climbcamp.fr/differents-types-parois-escalade/
TYPE_VOIE_NOM=['Verticale','Dalle','Devers','Toit','Cheminee','Diedre','Marche']
TYPE_VOIE_DESCRIPTION=['Voie en angle de 90 degres avec le sol.',
                       'Voie en inclinaison positive.',
                       'Voie en inclinaison negative.',
                       'Paroi horizontale parallele au sol.',
                       'Deux parois face a face.',
                       'Deux parois cote a cote qui font un angle de 90 degrees.',
                       'De la marche']

for i in range(len(TYPE_VOIE_NOM)) : 
    res+=f"INSERT INTO TYPEVOIE (nom, description) VALUES ('{TYPE_VOIE_NOM[i]}','{TYPE_VOIE_DESCRIPTION[i]}');\n"


#Ici on ajoute des vois 
# Voie(IdV,nom,longueur,IdTV,FR,IdSE)
# primary key : IdV
# foreign key : IdTV de TypeVoie, FR de difficulté, IdSE de SiteEsca
# IdV serial,
# IdTV integer,
# FR varchar(2),
# IdSE integer,

res+=r""" 
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

"""

#Ici on marque les connexions entre voies du même site 
# DeboucheVers(IdV1,IdV2)
# Primary key : (IdV)
# foreign key : IdV1 et IdV2 qui sont des clés différentes IdV de Voie
# IdV1 integer;
# IdV2 interger;


res+=r"""
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
"""


#Ici on va remplir les guides et leur localité
#EstGuideDe(mail,CodePostal)
#Primary Key : (mail,CodePostal)
#Foreign Key : mail d'utilisateur, CodePostal de Localite
#mail varchar (320)
#Codepostal varchar(5)

res+= r"""
INSERT INTO ESTGUIDEDE (mail,CodePostal) VALUES ('leroux.leo32@yahoo.fr','77300');
INSERT INTO ESTGUIDEDE (mail,CodePostal) VALUES ('guerin.oceane30@live.com','77300');
INSERT INTO ESTGUIDEDE (mail,CodePostal) VALUES ('noah67@hotmail.com','77300');
INSERT INTO ESTGUIDEDE (mail,CodePostal) VALUES ('adam74@laposte.net','77300');
INSERT INTO ESTGUIDEDE (mail,CodePostal) VALUES ('noah55@hotmail.com','42920');
""" 



#Ici on va remplir les propositions 
#Proposition(IdPropo,description,datep,nb_max,mail,FR,IdSE)
#Primary Key : IdPropo
#Foreign key : mail de l'utilisateur qui organise, FR de Difficulté, IdSE de SiteEsca
#Idpropo integer,
#description varchar(999),
#datep date
#nb_max integer,
#mail varchar(320),
#fr varchar(2),
#idse integer,
#contrainte nb_max doit être positif.
res+=r"""
INSERT INTO PROPOSITION (description,datep,nb_max,mail,fr,idse) VALUES ('Petite session tranquille au bas Cuivrer.','2023-11-16',5,'leroux.leo32@yahoo.fr','4',1);
INSERT INTO PROPOSITION (description,datep,nb_max,mail,fr,idse) VALUES ('Session au Chien.','2021-11-16',5,'guerin.oceane30@live.com','6a',5);
INSERT INTO PROPOSITION (description,datep,nb_max,mail,fr,idse) VALUES ('Session au merciers.','2023-07-09',5,'guerin.oceane30@live.com','3',2);
INSERT INTO PROPOSITION (description,datep,nb_max,mail,fr,idse) VALUES ('Session au mur','2020-09-07',5,'noah67@hotmail.com','4','3');
INSERT INTO PROPOSITION (description,datep,nb_max,mail,fr,idse) VALUES ('Apremont :)','2019-04-01',5,'adam74@laposte.net','5b','4');
INSERT INTO PROPOSITION (description,datep,nb_max,mail,fr,idse) VALUES ('Apremomt :p','2022-04-01',5,'noah55@hotmail.com','5b','4');
INSERT INTO PROPOSITION (description,datep,nb_max,mail,fr,idse) VALUES ('balade a Apremont','2023-04-01',5,'noah55@hotmail.com','5b','4');
INSERT INTO PROPOSITION (description,datep,nb_max,mail,fr,idse) VALUES ('balade','2023-06-07',5,'noah55@hotmail.com','6a',5);
INSERT INTO PROPOSITION (description,datep,nb_max,mail,fr,idse) VALUES ('promenade','2023-07-07',5,'noah55@hotmail.com','3',2);

"""

#Ici on va remplir participe 
#Participe(mail,IdPropo)
#Primary Key : (mail,IdPropo)
#Foreign Key : mail d'utilisateur, IdPropo de Proposition.
#mail varchar(320),
#Idpropo integer,
res+=r"""
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
"""

#Ici on va définir les différents types d'escalades 
#TypeEsca(IdTE,nom,description)
#Primary key :IdTE
#IdTe integer,
#nom varchar(25),
#description varchar(999),
res+= r"""
INSERT INTO TYPEESCA (nom,description) VALUES ('Escalade sportive','Utilise des points d ancrage preexistants pour la protection, avec une corde d assurance.');
INSERT INTO TYPEESCA (nom,description) VALUES ('Escalade Traditionnelle', 'Les grimpeurs placent leur propre equipement de protection tout en progressant');
INSERT INTO TYPEESCA (nom,description) VALUES ('Solo Integral','Escalade sans equipement de protection, meme sans corde. Tres dangereux');
INSERT INTO TYPEESCA (nom,description) VALUES ('duo','Deux grimpeurs partagent la responsabilité de la conduite et de l assurage.');

"""

#Ici on va définir des cordées 
#Cordée(IdCordée)
#Primary key : IdCordée
#idCordée integer,

for i in range(1,3) :
    res+="INSERT INTO cordee DEFAULT VALUES;\n"


#Ici on va définir PartieC
#PartieC(idCordée,mail) 
#Primary Key : (idCordée,mail)
#Foreign key : idCordée de Cordée, mail de Utilisateur
#idcordée integer,
#mail varchar(320)
#mdp varchar(25)
res+=r"""
INSERT INTO PARTIEC  (idcordee,mail) VALUES (1,'simon.alex8@yahoo.fr');
INSERT INTO PARTIEC  (idcordee,mail) VALUES (1,'noah81@yahoo.fr');
INSERT INTO PARTIEC VALUES (1,'jean.gabriel17@yahoo.fr');

INSERT INTO PARTIEC VALUES (2,'blanc.rose70@gmail.com');
INSERT INTO PARTIEC VALUES (2,'louis58@laposte.net');
INSERT INTO PARTIEC VALUES (2,'martin.alice96@laposte.net');
"""

#Ici on va définir grimper 
#Grimper(IdTE,IdCordée,IdV,date)
#Primary key : (IdTE,IdCordée,IdV,date)
#Foreign key : IdTe de TypeEsca, IdCordée de Cordée, IdV de Voie
#IdTE integer,
#IdCordée integer,
#IdV integer,
#date date,

res+=r"""
INSERT INTO GRIMPER (IdTE,Idcordee,IdV,dateg) VALUES (1,1,1,'2023-11-16');
INSERT INTO GRIMPER (IdTE,Idcordee,IdV,dateg) VALUES (2,2,5,'2021-11-16');

"""


#Partie actualisation des vues
res +=r"""

REFRESH MATERIALIZED VIEW topFiveSiteEsca;
"""
print(res)
print(mail_list)
#crée sql
with open("table_filler.sql", 'w', encoding='utf-8') as file:
    file.write(res)
    file.close()

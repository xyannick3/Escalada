# Ceci est le répositoire de développement de la base de donnée. 

1. Comment initialiser la database : 

Pour pouvoir faire fonctionner le site il faut utiliser l'application SQL shell sur windows. après l'avoir ouvert une fenêtre s'ouvre il faut selectionner le défaut pour : 
- `Server` = `localhost`
- `Database` = `postgres` 
- `Port` = `5432`
- `Username` = `Postgres` (c'est le superuser)

La seule variable est le password, par defaut le mot de passe est 12345678.
Il est possible de le modifier mais si le fichier database.ini est modifié pour accomoder une database locale NE PAS PUSH LES CHANGEMENTS SUR database.ini (ce serait chiant).

ensuite il faut entrer la commande `CREATE DATABASE master;`

puis `\c master`

puis on colle le contenu du fichier `database.sql` depuis `/DevelopmentFile`

normalement la database est initialisée :). 




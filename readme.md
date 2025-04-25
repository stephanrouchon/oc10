# SoftDesk Project Management API

SoftDesk est une API de gestion de projets permettant aux utilisateurs de créer des projets, de gérer des issues (problèmes) et de collaborer avec d'autres contributeurs.

## Fonctionnalités

- **Gestion des projets** : Créez, mettez à jour et supprimez des projets.
- **Gestion des issues** : Ajoutez, modifiez et supprimez des issues liées à un projet.
- **Collaboration** : Ajoutez des contributeurs à vos projets.
- **Authentification JWT** : Authentification sécurisée avec JSON Web Tokens.
- **Permissions** : Contrôlez l'accès aux projets et aux issues en fonction des rôles des utilisateurs.

## Prérequis

- Python 3.13 ou supérieur
- [Pipenv](https://pipenv.pypa.io/en/latest/) pour la gestion des dépendances
- SQLite pour la base de données

## Installation

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/stephanrouchon/Oc10
   cd Oc10

2. Installez les dépendances avec Pipenv
    pipenv install

3. Activez l'environnement virtuel
    pipenv shell

4. Appliquer les migrations
    python manage.py migrate

5. Lancez le serveur de développement
    python manage.py runserver


## Configuration

1. Créer un fichier .env à la racine du projet pour définir les variables d'environnement :

    SECRET_KEY=django-insecure-votre-cle-secrete
    DEBUG=True
    ALLOWED_HOSTS=127.0.0.1,localhost

2. Assurez-vous que le fichier .env est ignoré par Git en ajoutant cette ligne dans .gitignore :
    .env

## Utilisation

1. Création d'un utilisateur

2. Connexion de l'utilisateur :

    l'API utilise JWT pour l'authentification. pour obtenir un Token d'accès, utilisez l'endpoint suivant :
    {
    "username": "votre_nom_utilisateur",
    "password": "votre_mot_de_passe"
    }   

    vous obtiendrez en réponse :

    {
    "access": "votre_token_access",
    "refresh": "votre_token_refresh"
    }

    Ajoutez le token dans les en-têtes des requêtes pour accéder aux endpoints protégés :
    Authorization: Bearer <votre_token_access>

## Endpoints

Endpoints
Projets
GET /api/projects/ : Liste des projets.
POST /api/projects/ : Créer un projet.
GET /api/projects/{id}/ : Détails d'un projet.
PUT /api/projects/{id}/ : Mettre à jour un projet.
DELETE /api/projects/{id}/ : Supprimer un projet.

Issues
GET /api/projects/{project_id}/issues/ : Liste des issues d'un projet.
POST /api/projects/{project_id}/issues/ : Créer une issue.
GET /api/projects/{project_id}/issues/{issue_id}/ : Détails d'une issue.
PUT /api/projects/{project_id}/issues/{issue_id}/ : Mettre à jour une issue.
DELETE /api/projects/{project_id}/issues/{issue_id}/ : Supprimer une issue.

Contributeurs
GET /api/projects/{project_id}/contributors/ : Liste des contributeurs d'un projet.
POST /api/projects/{project_id}/contributors/ : Ajouter un contributeur.
DELETE /api/projects/{project_id}/contributors/{user_id}/ : Supprimer un contributeur.

##Licence
Ce projet est sous licence MIT. Consultez le fichier LICENSE pour plus d'informations.
# P9 Blog LITReview
## LITReview - Plateforme de Critiques Littéraires

Bienvenue sur **LITReview**, une application web Django qui permet aux utilisateurs de demander, publier et consulter des critiques de livres dans un environnement social et collaboratif. Que vous soyez un lecteur passionné ou un critique en herbe, LITReview est conçu pour faciliter vos échanges autour de la littérature.

## Table des Matières
- [Fonctionnalités](#fonctionnalités)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [Auteur](#auteur)

## Fonctionnalités
### Gestion des utilisateurs

- **Création de compte** : Inscription et connexion sécurisées.
- **Gestion du profil** : Modifiez le mot de passe.
- **Suivi d'utilisateurs** : Suivez d'autres utilisateurs pour voir leurs critiques.

### Gestion des critiques

- **Demande de critiques** : Créez des tickets avec un titre, une description et une image de couverture (optionnelle) pour demander des critiques.
- **Publication de critiques** : Répondez aux tickets avec une critique comprenant une note sur 5 étoiles, un titre et un commentaire détaillé.
- **Un critique par ticket** : Chaque ticket ne peut avoir qu'une critique publiée.

### Interactions sociales

- **Flux personnalisé** : Consultez un flux des critiques des utilisateurs que vous suivez.
- **Fonction de blocage** : Bloquez des utilisateurs pour ne plus voir leurs publications.
- **Gestion des publications** : Modifiez ou supprimez vos propres critiques et tickets.

## Prérequis

Avant de commencer, assurez-vous d'avoir les éléments suivants installés sur votre machine :

- **Python 3.12.4** ou supérieur
- **pip** (gestionnaire de paquets Python)
- **Git** pour cloner le dépôt
- Un terminal ou une invite de commande

## Installation

1. Clonez le dépôt:
```bash
git clone https://github.com/antogro/P9-LITRevu-Django-app.git
cd P9-LITRevu-Django-app
```

2. Créez et activez un environnement virtuel:

    ### Windows
```bash
python -m venv env
env\Scripts\activate
```

### Linux/MacOS
```bash
python3 -m venv env
source env/bin/activate
```

3. Installez les dépendances du projet :
```bash
pip install -r requirements.txt
```

## Configuration

Avant de lancer l'application, assurez-vous d'avoir configuré la base de données et appliqué les migrations nécessaires. Voici les étapes à suivre :

1. **Appliquer les migrations de la base de données** :

```bash
cd config
```
```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```

**Explication** : Cette commande applique les migrations, qui sont des modifications de la structure de la base de données définies dans les fichiers de migration. Elle s'assure que la base de données est à jour avec les modèles Django.

2. **Lancer le serveur de développement** :

```bash
python manage.py runserver
```

**Explication** : Cette commande démarre le serveur de développement Django, qui vous permet d'accéder à l'application localement via votre navigateur à l'adresse suivante : `http://127.0.0.1:8000/`. Vous pouvez l'utiliser pour tester l'application sur votre machine avant de la déployer en production.

## Utilisation

- **Inscription et Connexion** : Créez un compte ou connectez-vous si vous en avez déjà un.
- **Demander une critique** : Créez un nouveau ticket pour demander une critique sur un livre.
- **Publier une critique** : Évaluez un ticket avec votre propre critique.
- **Gérer vos publications** : Accédez à votre profil pour modifier ou supprimer vos critiques et tickets.
- **Gérer vos abonnements** : Abonnez-vous à d'autres utilisateurs pour suivre leurs publications, et bloquez les utilisateurs indésirables.

## Auteur

[@antogro](https://github.com/antogro)

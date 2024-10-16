# P9 Blog LITReview

```markdown
# LITReview - Plateforme de Critiques Littéraires
## Bienvenue sur LITReview !
Une application web Django permettant aux utilisateurs de demander, publier et consulter des critiques de livres dans un environnement social et collaboratif.
```

```markdown
## Table des Matières
- [Fonctionnalités](#fonctionnalités)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [Contribution](#contribution)
- [Licence](#licence)
```

```markdown
## Prérequis
- Python 3.12.4 ou supérieur
- pip (gestionnaire de paquets Python)
- Un terminal ou invite de commande
- Git
```

```markdown
## Fonctionnalités

### Gestion des Utilisateurs
- Création et gestion de compte utilisateur
- Système d'authentification sécurisé
- Modification du mot de passe

### Gestion des Critiques
- Création de demandes de critiques avec:
  - Titre
  - Description
  - Image de couverture (optionnelle)
- Publication de critiques avec:
  - Note sur 5 étoiles
  - Titre
  - Commentaire détaillé

### Interactions Sociales
- Système d'abonnement aux autres utilisateurs
- Flux personnalisé des critiques
- Fonction de blocage d'utilisateurs
- Gestion des publications personnelles
```


```markdown
## Installation

1. Clonez le dépôt
```bash
git clone https://github.com/antogro/P9-LITRevu-Django-app.git
cd P9-LITRevu-Django-app
```

2. Créez et activez l'environnement virtuel
```bash
# Windows
python -m venv env
env\Scripts\activate

# Linux/MacOS
python3 -m venv env
source env/bin/activate
```

3. Installez les dépendances
```bash
pip install -r requirements.txt
```

4. Configurez la base de données
```bash
python manage.py migrate
```

5. Lancez le serveur
```bash
cd config
python manage.py runserver
```

L'application sera accessible à l'adresse: http://127.0.0.1:8000/



```markdown
## Configuration

### Variables d'Environnement
Créez un fichier `.env` à la racine du projet:
```env
DEBUG=True
SECRET_KEY=votre_clé_secrète
```


## Autheur
[@antogro](https://github.com/antogro)

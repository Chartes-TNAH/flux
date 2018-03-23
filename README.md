# L'application PythouNews, un flux d'informations

## Installation

Le présent flux d'informations, nommé PythouNews, a été créé par Fanny Mézard, Anne-Laure Huet, Marie-Gaëlle Gourio, Amandine Heathcote, Alexandre Gaudin.

Pour installer PythouNews en local, le plus simple est de procéder dans un environnement virtuel :

### Sous Linux

Pré-requis : installer Python3 et MySQL

Pour mettre l'environnement virtuel en place :
* créer un dossier
* dans ce dossier, créer un environnement virtuel. Pour cela :
  * Ouvrir le terminal et se placer dans le dossier créé
  * Taper la commande `python3 -m venv env` (à exécuter une fois seulement)
* Initier le dossier créé en repository local avec la commande `git init`
* Cloner le dossier PythouNews en tapant `git clone`+url du code
* Activer l'environnement virtuel avec la commande `source env/bin/activate`. Cette commande sera nécessaire à chaque fois afin d'activer l'environnement virtuel pour pouvoir utiliser PythouNews
* Exécuter les fichiers datamodel.sql et valeurs_flux.sql
* Installer les packages nécessaires au fonctionnement de PythouNews avec `pip install -r requirements.txt`
* Se déplacer dans le dossier flux
* Pour lancer PythouNews taper `python run.py`

A taper dans le terminal pour lancer PythouNews les fois suivantes :
* `source env/bin/activate`
* `python run.py`

### Sous iOS

Pré-requis : installer Python3 et MySQL

Pour mettre l'environnement virtuel en place :
* créer un dossier
* dans ce dossier, créer un environnement virtuel. Pour cela :
  * Ouvrir le terminal et se placer dans le dossier créé
  * Taper la commande `virtualenv ~/.env -p python3` (à exécuter une fois seulement)
* Initier le dossier créé en repository local avec la commande `git init`
* Cloner le dossier PythouNews en tapant `git clone`+url du code
* Activer l'environnement virtuel avec la commande `source ~/.env/bin/activate`. Cette commande sera nécessaire à chaque fois afin d'activer l'environnement virtuel pour pouvoir utiliser PythouNews
* Exécuter les fichiers datamodel.sql et valeurs_flux.sql
* Installer les packages nécessaires au fonctionnement de PythouNews avec `pip install -r requirements.txt`
* Se déplacer dans le dossier flux
* Pour lancer PythouNews taper `python run.py`

A taper dans le terminal pour lancer PythouNews les fois suivantes :
* `source ~/.env/bin/activate`
* `python run.py`

## Consignes

L'application PythouNews a été développée en mars 2018 dans le cadre du devoir final des cours de Python, dispensés en master 2 "Technologies numériques appliquées à l'histoire" à l'Ecole des chartes. Les consignes à suivre étaient les suivantes :

Dans le cadre du master, il serait utile d'avoir un outil de flux d'informations. On développera l'application avec un système de compte utilisateur où:
* L'utilisateur a sa promotion comme information
* On peut créer des thèmes pour les nouvelles à partager
* Quand on partage une URL, l'application va récupérer les informations `<meta name="description" />` et `<title />` de la page (voir BeautifulSoup en plus de requests)
* Des flux RSS sont mis à disposition par catégories (et une catégorie totale)
* On peut ajouter un texte court pour accompagner le partage
* On peut chercher dans les titres, descriptions et textes d'accompagnement
* On peut afficher chaque flux directement dans l'application

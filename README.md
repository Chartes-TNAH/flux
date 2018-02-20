# Devoir Python - Application Flux d'information

Rendu le 15 Avril

## Consignes globales

* Les rendus se feront via git et github en particulier sur des dépôts de https://github.com/Chartes-TNAH .
* La notation peut différer d'un membre à l'autre du groupe.
* Une documentation pour la mise en place du projet (installation) sera mise à disposition. Le README de ce dépôt peut être utilisé comme référence.
* Des données de tests seront fournies afin d'utiliser l'application.
* (Optionnel) Des tests unitaires seront fournis Note: cet encart dépendra de l'évolution du cours.
* Le design final ne sera pas évalué bien qu'il soit recommandé que l'ensemble reste lisible et utilisable.

## Consignes pour Flux d'information

Dans le cadre du master, il serait utile d'avoir un outil de flux d'information. On développera l'application avec un système de compte utilisateur où:

* l'utilisateur a sa promotion comme information
* on peut créer des thèmes pour les nouvelles à partager
* Quand on partage une URL, l'application va récupérer les informations `<meta name="description" />` et `<title />` de la page (voir BeautifulSoup en plus de request)
* Des flux RSS sont mis à disposition par catégories (et une catégorie Totale)
* On peut ajouter un texte court pour accompagner le partage
* On peut chercher dans les titres, descriptions et textes d'accompagnement
* On peut afficher chaque flux directement dans l'application

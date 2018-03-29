from..app import db
from bs4 import BeautifulSoup
import requests
import time
import datetime
from flask_login import current_user
from .utilisateurs import User

#Table pour stocker les publication des utilisateurs
class Publication(db.Model):
    publication_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    publication_date = db.Column(db.Text, nullable=False)
    publication_nom = db.Column(db.String(40), nullable=True)
    publication_lien = db.Column(db.Integer, nullable=True)
    publication_texte = db.Column(db.Text, nullable=False, unique=True)
    publication_titre_url = db.Column(db.Text, nullable=True, unique=True)
    publication_description_url = db.Column(db.Text, nullable=True, unique=True)
    sujetpublis = db.relationship("Sujet_publi", back_populates="publication")
    publi_user_id= db.Column(db.Integer, db.ForeignKey('user.user_id'),nullable=False)


    @staticmethod
    def creer_publication(titre, lien, texte, auteur):
        """ Crée une nouvelle publication et renvoie les informations rentrées par l'utilisateur.

        :param titre: Titre de la publication
        :param lien: URL partagé par l'utilisateur
        :param texte: Texte écrit par l'utilisateur
        :returns: Si réussite, publication de l'utilisateur. Sinon None
        :rtype: Publication or None
        """
        erreurs = []


        if not titre:
            erreurs.append("Veuillez ajouter un titre à votre publication")

        if not lien:
            erreurs.append("Veuillez ajouter un lien à votre publication")

        if len(erreurs) > 0:
            return False, erreurs

        # on récupére avec requests la page html du lien entré par l'utilisateur
        page_html = requests.get(lien)
        #  avec BS on insére dans la variable soup le contenu de la page html en utilisant le parser de python
        soup = BeautifulSoup(page_html.text, 'html.parser')
        # on crée une variable qui récupère dans notre page html les balises <meta/> qui ont un attribut name
        # avec une valeur "description". (.find avec BeautifulSoup)
        balise_meta_desc = soup.find("meta", attrs={"name": u"description"})
        # on crée une variable description_url qui récupère la valeur de l'attr content
        if balise_meta_desc:
            description_url = balise_meta_desc.get("content")
        else:
            description_url = "Aucune description n'est disponible"
        balise_titre = soup.title
        titre_url = balise_titre.get_text()

        date = datetime.date.today()
        publication = Publication(
            publication_nom=titre,
            publication_date=date,
            publication_lien=lien,
            publication_texte=texte,
            publi_user_id=auteur,
            publication_description_url=description_url,
            publication_titre_url=titre_url)

        try:
            db.session.add(publication)

            db.session.commit()

            return True, publication
        except Exception as erreur:
            return False, [str(erreur)]


    @staticmethod
    def afficher_publications(pagination):
        """ Affiche les publications des utilisateurs

        :return: affichage des publications
        """
        # si ce n'est pas un objet pagination
        liste_publications = []
        # si ce n'est pas un objet pagination
        for item in pagination.items:
            titre = item.publication_nom
            date = item.publication_date
            lien = item.publication_lien
            texte = item.publication_texte
            auteur = User.query.get(item.publi_user_id)
            description_url = item.publication_description_url
            titre_url = item.publication_titre_url

            liste_publications.append(
                {"titre": titre, "date": date, "lien": lien, "texte": texte, "titre_url": titre_url,
                 "description_url": description_url, "auteur": auteur})

        return liste_publications

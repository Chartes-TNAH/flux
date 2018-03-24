from..app import db
from bs4 import BeautifulSoup
import requests
import time
import datetime
from flask_login import current_user

#Table pour stocker les publication des utilisateurs
class Publication(db.Model):
    publication_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    publication_date = db.Column(db.Text, nullable=False)
    publication_nom = db.Column(db.String(40), nullable=True)
    publication_lien = db.Column(db.Integer, nullable=True)
    publication_texte = db.Column(db.Text, nullable=False, unique=True)
    sujetpublis = db.relationship("Sujet_publi", back_populates="publication")
    #publi_auteur_id = db.relationship("User", back_populates="user_publication_id")


    @staticmethod
    def creer_publication(titre, date, lien, texte, auteur):
        """ Crée une nouvelle publication et renvoie les informations rentrées par l'utilisateur.

        :param titre: Titre de la publication
        :param date: Date de la publication
        :param lien: URL partagé par l'utilisateur
        :param texte: Texte écrit par l'utilisateur
        :returns: Si réussite, publication de l'utilisateur. Sinon None
        :rtype: Publication or None
        """
        erreurs = []

        #auteur = current_user.user_id
        print(auteur)
        if not titre:
            erreurs.append("Veuillez ajouter un titre à votre publication")

        if not lien:
            erreurs.append("Veuillez ajouter un lien à votre publication")

        if len(erreurs) > 0:
            return False, erreurs

        date = datetime.date.today()
        publication = Publication(
            publication_nom=titre,
            publication_date=date,
            publication_lien=lien,
            publication_texte=texte)

        try:
            db.session.add(publication)

            db.session.commit()

            return True, publication
        except Exception as erreur:
            return False, [str(erreur)]

    @staticmethod
    def afficher_publications(page):
        """ Affiche les publications des utilisateurs

        :return: affichage des publications
        """
        liste_publications =[]
        if isinstance(page, str) and page.isdigit():
            page = int(page)
        else:
            page = 1
        pagination = Publication.query.order_by(Publication.publication_date.desc()).paginate(page=page, per_page=8)
        for item in pagination.items:
            titre = item.publication_nom
            date = item.publication_date
            lien = item.publication_lien
            texte = item.publication_texte
            auteur_info = item.publication_id
            auteur = auteur_info.user_nom
            print (auteur)
            page_html = requests.get(lien)
            soup = BeautifulSoup(page_html.text, 'html.parser')
            description_url = soup.find("meta", attrs={"name": u"description"})
            titre_url = soup.title
            publi = titre, date, lien, texte, titre_url.get_text(), description_url, auteur
            liste_publications.append(publi)
            print(liste_publications)

        return liste_publications, pagination

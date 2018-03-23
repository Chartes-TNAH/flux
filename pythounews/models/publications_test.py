from..app import db
from bs4 import BeautifulSoup
import requests
import time
import datetime

#Table pour stocker les publication des utilisateurs
class Publications_test(db.Model):
    publications_test_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    publications_test_date = db.Column(db.Text, nullable=False)
    publications_test_nom = db.Column(db.String(40), nullable=True)
    publications_test_lien = db.Column(db.Integer, nullable=True)
    publications_test_texte = db.Column(db.Text, nullable=False, unique=True)
    sujetpublis = db.relationship("Sujet_publi", back_populates="publication")

    @staticmethod
    def afficher_publications_test():
        """ Affiche les publications standards de test

        :return: affichage des publications de test
        """
        liste_publications_test = []
        publication_test = Publications_test.query.all()
        for item in publications_test:
            titre = item.publications_test_nom
            date = item.publications_test_date
            lien = item.publications_test_lien
            texte = item.publications_test_texte
            page_html = requests.get(lien)
            soup = BeautifulSoup(page_html.text, 'html.parser')
            description_url = soup.find("meta", attrs={"name":u"description"})
            titre_url = soup.title
            publi = titre, date, lien, texte, titre_url.get_text(), description_url
            liste_publications_test.append(publi)

        return liste_publications_test
from ..app import db
from .publications import Publication

# Table pour stocker les mots-clés
class Motscles(db.Model):
    motscles_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    motscles_nom = db.Column(db.Text, nullable=False)
    sujetpublis = db.relationship("Sujet_publi", back_populates="motscles")
    sujetfluxrss = db.relationship("Sujet_fluxrss", back_populates="motscles")



class Sujet_publi(db.Model):
    sujet_publi_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    sujet_publi_publication_id = db.Column(db.Integer, db.ForeignKey('publication.publication_id'), nullable=False)
    sujet_publi_motscles_id = db.Column(db.Integer, db.ForeignKey('motscles.motscles_id'), nullable=False)
    motscles = db.relationship("Motscles", back_populates="sujetpublis")
    publication = db.relationship("Publication", back_populates="sujetpublis")

    @staticmethod
    def ajouter_categorie(categorie, donnees):
        """ Ajout de la catégorie de la publication en fonction de ce que l'utilisateur a coché

                :param categorie: mots clés choisis par l'utilisateur
                :type motscles_id: list
                :param donnees: données rentrées par l'utilisateur (A CHANGER !!!)
                :type donnees: list
                :return: page de publication correspond au mot clé
            """
        for mot in categorie:
            if mot != None:
                mot_id = Motscles.query.filter(Motscles.motscles_nom == mot).first()
                sujetpubli = Sujet_publi(
                    sujet_publi_publication_id=donnees.publication_id,
                    sujet_publi_motscles_id=mot_id.motscles_id
                )
        db.session.add(sujetpubli)
        db.session.commit()

    @staticmethod
    #attention : j'ai peur qu'on ait une erreur si la base de données est vide.
    def afficher_publi_categorie(motcle):
        sujet_publi = Sujet_publi.query.filter(Sujet_publi.sujet_publi_motscles_id == motcle.motscles_id).all()
        liste_publications = []
        for sujet in sujet_publi:
            publications = Publication.query.filter(Publication.publication_id == sujet.sujet_publi_publication_id)
            for publication in publications:
                liste_publications.append(publication)
        return liste_publications

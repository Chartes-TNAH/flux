from ..app import db
from .publications import Publication
from .utilisateurs import User

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
    def afficher_publi_categorie(motcle):
        """ Permet la récupération des publications selon le mot-clé de la page

        :param motcle: correspond à l'id du mot-clé, correspondant au motcle_id du chemin de la page
        :type motscle: int
        :return liste_publications : liste des publications correspondantes au mot-clé sélectionné par l'utilisateur
        :type liste_publications : list

        """
        liste_publications = []
        #Récupère le sujet de la publication en fonction du mot clé sélectionné
        sujet_publi = Sujet_publi.query.filter(Sujet_publi.sujet_publi_motscles_id == motcle.motscles_id).all()
        #On boucle le sujet de la publication
        for publi in sujet_publi:
            #On récupère toutes les publications ayant pour mot-clé le même précédement sélectionné
            publications = Publication.query.filter(Publication.publication_id==publi.sujet_publi_publication_id).all()
            #POur chaque publication, on récupère tous les éléments nécessaires pour chaque publication
            for item in publications:
                titre = item.publication_nom
                date = item.publication_date
                lien = item.publication_lien
                texte = item.publication_texte
                auteur = User.query.get(item.publi_user_id)
                description_url = item.publication_description_url
                titre_url = item.publication_titre_url
                #On insère au début de la liste la publication, pour qu'elles soient en ordre décroissant
                liste_publications.insert(0,
                    {"titre": titre, "date": date, "lien": lien, "texte": texte, "titre_url": titre_url,
                     "description_url": description_url, "auteur": auteur})
        return liste_publications

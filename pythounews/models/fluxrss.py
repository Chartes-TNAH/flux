from feedparser import parse
from ..app import db

class Fluxrss(db.Model):
    fluxrss_id=db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    fluxrss_lien=db.Column(db.String(150), nullable=True)
    fluxrss_titre=db.Column(db.String(40), nullable=True)
    fluxrss_adresse_site=db.Column(db.String(40), nullable=True)
    sujetfluxrss = db.relationship("Sujet_fluxrss", back_populates="fluxrss_a")

    @staticmethod
    def read_rss():
        """ Lit un flux RSS et les retourne sous un format simplifié (titre, sujet, date, lien)

        :param feeds : liste de flux RSS
        :type feeds: list
        :return liste_rss: Liste des premiers flux rss par date
        :type liste_rss : list
        """
        liste_rss=[]
        liste_rss_bnf=[]
        #On récupère l'ensemble des informations qui se trouvent dans la classe Fluxrss
        feeds=Fluxrss.query.all()
        #On boucle sur la liste des flux rss enregistrés dans valeurs_flux.sql
        for feed in feeds:
            institution = feed.fluxrss_titre
            adresse_site = feed.fluxrss_adresse_site
            #On récupère pour chaque flux le lien vers les flux rss, puis on le parse
            feed = feed.fluxrss_lien
            feed = parse(feed)
            #On distingue les flux rss de la BNF, qui ne sont pas classés par ordre de date, et les autres flux rss.
            if institution.startswith("BNF"):
                for item in feed["items"]:
                    titre = (item["title_detail"]["value"])
                    sujet = (item["summary_detail"]["value"])
                    #On limite le nombre de caractères affichés à 400, en récupérant les 400 premiers caractères.
                    if len(sujet)>400:
                        sujet = sujet[0:400]
                        sujet = sujet + " ..."
                    lien = (item["link"])
                    date = (item["published"])
                    rss=titre, sujet, lien, date, institution, adresse_site
                    #On ajoute chaque actualité présente dans la page flux rss de chaque site dans une liste.
                    liste_rss_bnf.append(rss)
                #Après avoir récupéré toutes les actualités, on les classe par ordre de date.
                liste_rss_bnf.sort(key=lambda liste: liste[4])
                #On récupère le dernier, qui est le plus récent.
                liste_rss.append(liste_rss_bnf[-1])
            else:
                #On ne traite uniquement ici que le premier flux rss, puisqu'il est le plus récent.
                item = feed["items"][0]
                titre = (item["title_detail"]["value"])
                sujet = (item["summary_detail"]["value"])
                #La condition suivante permet de limiter le nombre de caractères affichés sur la page html.
                if len(sujet)>400:
                    sujet = sujet[0:400]
                    sujet = sujet + "..."
                lien = (item["link"])
                date = (item["published"])
                #La variable rss prend les cinq valeurs ci-dessus.
                rss = titre, sujet, lien, date, institution, adresse_site
                #Chaque item du flux est ajouté dans une liste.
            #On ne récupère ici que le tout premier élément du flux rss, puisqu'il s'agit du plus récent.
                liste_rss.append(rss)
            #On retourne une liste qui contient pour chaque flux l'actualité la plus récente.
        return liste_rss

#Cette classe permet de faire le lien entre les flux rss et les mots-clés.
class Sujet_fluxrss(db.Model):
    sujet_fluxrss_id=db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    sujet_fluxrss_motscles_id=db.Column(db.Integer, db.ForeignKey('motscles.motscles_id'), nullable=False)
    sujet_fluxrss_fluxrss_id=db.Column(db.Integer, db.ForeignKey('fluxrss.fluxrss_id'), nullable=False)
    motscles = db.relationship("Motscles", back_populates="sujetfluxrss")
    fluxrss_a = db.relationship("Fluxrss", back_populates="sujetfluxrss")


    @staticmethod
    def afficher_rss(flux):
        """ A partir de l'id correspondant à un mot-clé, récupère tous les flux ayant le même mot-clé

        :param flux : nombre entier correspondant à l'id du mot-clé d'un flux
        :type flux : int
        :return liste_flux: Liste des flux rss ayant le même id d'un mot-clé
        :type liste_flux : list
        """
        #En premier lieu, on compare l'id des mots-clés : celui entré en paramètre de la méthode statique et ceux présents dans la table Sujet_fluxrss
        #On récupère toutes les informations de la classe Sujet_fluxrss dont l'id du sujet du flux rss entré dans la table Sujet_fluxrss correspond à l'id qui est en paramètre de la méthode statique.
        sujet_flux = Sujet_fluxrss.query.filter(Sujet_fluxrss.sujet_fluxrss_motscles_id == flux.motscles_id).all()
        liste_flux = []
        #On boucle pour chaque élément sujet_flux récupéré plus haut.
        for rss in sujet_flux:
            #En second lieu, on récupère tous les flux dont l'id des mots-clés correspond à celui recherché.
            #On récupère dans la table Fluxrss toutes les informations pour chaque flux dont l'id du flux correspond à l'id des flux entrés dans la table Sujet_flux
            rss = Fluxrss.query.filter(Fluxrss.fluxrss_id == rss.sujet_fluxrss_fluxrss_id)
            #On boucle pour obtenir chaque information, comme dans la méthode statique read_rss, définie plus haut.
            for rss_unique in rss:
                institution = rss_unique.fluxrss_titre
                adresse_site = rss_unique.fluxrss_adresse_site
                feed = rss_unique.fluxrss_lien
                feed = parse(feed)
                liste_rss_bnf = []
                #On distingue les flux rss de la BNF, qui ne sont pas classés par ordre de date, et les autres flux rss.
                if institution.startswith("BNF"):
                    for item in feed["items"]:
                        titre = (item["title_detail"]["value"])
                        sujet = (item["summary_detail"]["value"])
                        if len(sujet)>400:
                            sujet = sujet[0:400]
                            sujet = sujet + " ..."
                        lien = (item["link"])
                        date = (item["published"])
                        rss=titre, sujet, lien, date, institution, adresse_site
                        liste_rss_bnf.append(rss)
                    liste_rss_bnf.sort(key=lambda liste: liste[4])
                    liste_flux.append(liste_rss_bnf[-1])
                else:
        # On boucle sur chaque item du flux rss
                    item = feed["items"][0]
                    titre = (item["title_detail"]["value"])
                    sujet = (item["summary_detail"]["value"])
                    #La condition suivante permet de limiter le nombre de caractères affichés sur la page html.
                    if len(sujet)>400:
                        sujet = sujet[0:400]
                        sujet = sujet + " ..."
                    lien = (item["link"])
                    date = (item["published"])
                    #La variable rss prend les cinq valeurs ci-dessus.
                    rss = titre, sujet, lien, date, institution, adresse_site
                    #Chaque item du flux est ajouté dans une liste.
                #On ne récupère ici que le tout premier élément du flux rss, puisqu'il s'agit du plus récent.
                    liste_flux.append(rss)
        #On ne retourne finalement que les flux rss dont l'id des mots-clés correspondent à l'id utilisé en paramètre de la méthode statique. 
        return liste_flux

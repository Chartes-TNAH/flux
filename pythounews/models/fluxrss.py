from feedparser import parse
from ..app import db

class Fluxrss(db.Model):
    fluxrss_id=db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    fluxrss_lien=db.Column(db.String(150), nullable=True)
    fluxrss_titre=db.Column(db.String(40), nullable=True)
    fluxrss_adresse_site=db.Column(db.String(40), nullable=True)


#Cette fonction ne traite que les flux rss qui sont classés dans l'ordre du plus récent au plus ancien.
    @staticmethod
    def read_rss():
        """ Lit un flux RSS et les retourne sous un format simplifié (titre, sujet, date, lien)

        :param address: Adresse URI du flux RSS
        :type address: str
        :return: Tuple constitué du Titre, Sujet, Lien, Date
        :type titre, sujet, lien, date: str
        """
        liste_rss=[]
        liste_rss_bnf=[]

        #On parse l'adresse

        feeds=Fluxrss.query.all()
        i=0

        for feed in feeds:
            institution = feed.fluxrss_titre
            adresse_site = feed.fluxrss_adresse_site
            feed = feed.fluxrss_lien
            feed = parse(feed)
            #On distingue les flux rss de la BNF, qui ne sont pas classés par ordre de date, et les autres flux rss.
            if institution.startswith("BNF"):
                for item in feed["items"]:
                    titre = (item["title_detail"]["value"])
                    sujet = (item["summary_detail"]["value"])
                    if len(sujet)>500:
                        sujet = sujet[0:500]
                        sujet = sujet + " ..."
                    lien = (item["link"])
                    date = (item["published"])
                    rss=titre, sujet, lien, date, institution, adresse_site
                    liste_rss_bnf.append(rss)
                liste_rss_bnf.sort(key=lambda liste: liste[4])
                liste_rss.append(liste_rss_bnf[-1])
            else:
    # On boucle sur chaque item du flux rss
                item = feed["items"][0]
                titre = (item["title_detail"]["value"])
                sujet = (item["summary_detail"]["value"])
                #La série de if permet de traiter différemment les images des textes.
                #Le html n'affichait que les balises <img>. La condition suivante permet de récupérer le lien de l'image. La variable image prend comme valeur ce lien, sous forme de chaînes de caractères.

                #La condition suivante permet de limiter le nombre de caractères affichés sur la page html.
                if len(sujet)>500:
                    sujet = sujet[0:500]
                    sujet = sujet + " ..."
                lien = (item["link"])
                date = (item["published"])
                #La variable rss prend les cinq valeurs ci-dessus.
                rss = titre, sujet, lien, date, institution, adresse_site
                #Chaque item du flux est ajouté dans une liste.
            #On ne récupère ici que le tout premier élément du flux rss, puisqu'il s'agit du plus récent.
                liste_rss.append(rss)
        print(liste_rss)
        return liste_rss
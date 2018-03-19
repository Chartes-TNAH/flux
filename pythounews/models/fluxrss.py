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

        #On parse l'adresse

        feeds=Fluxrss.query.all()
        i=0

        for feed in feeds:
            institution = feed.fluxrss_titre
            adresse_site = feed.fluxrss_adresse_site
            feed = feed.fluxrss_lien
            feed = parse(feed)


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

#Les flux de la BnF n'étant pas classés par ordre de temps, il était nécessaire de créer une autre fonction permettant de récupérer l'information la plus récente.
"""
def read_rss_bnf(address):
     Lit un flux RSS et les retourne sous un format simplifié (titre, sujet, date, lien)

    :param address: Adresse URI du flux RSS
    :type address: str
    :return: Tuple constitué du Titre, Sujet, Lien, Date
    :type titre, sujet, lien, date: str
    
    liste=[]
    feed = parse(address)
    # On boucle sur chaque item du flux rss
    for item in feed["items"]:
        titre = (item["title_detail"]["value"])
        sujet = (item["summary_detail"]["value"])
        #La série de if permet de traiter différemment les images des textes.
        #Le html n'affichait que les balises <img>. La condition suivante permet de récupérer le lien de l'image. La variable image prend comme valeur ce lien, sous forme de chaînes de caractères.
        if sujet.startswith("<img"):
            sujet = sujet.split("\"")
            sujet = sujet[1]
            image = sujet
            sujet = ""
        #Ici, le sujet est un texte. La variable "image" ne prend alors aucune valeur
        else :
            sujet = (item["summary_detail"]["value"])
            image = ""
        

        #La condition suivante permet de limiter le nombre de caractères affichés sur la page html.
        if len(sujet)>500:
            sujet = sujet[0:500]
            sujet = sujet + " ..."

        lien = (item["link"])
        date = (item["published"])
        #La variable rss prend les cinq valeurs ci-dessus.
        rss = titre, sujet, image, lien, date
        #Chaque item d'un même flux rss est ajouté à une liste.
        liste.append(rss)
    #On classe par ordre de date l'ensemble des items rss de la liste.
    liste.sort(key=lambda liste: liste[4])
    #On récupère le dernier item, le plus récent, pour ensuite l'afficher dans la page html
    titre, sujet, image, lien, date = liste[-1]
    return titre, sujet, image, lien, date`
    """
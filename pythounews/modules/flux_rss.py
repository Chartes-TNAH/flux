from feedparser import parse

def read_rss(address):
    """ Lit un flux RSS et les retourne sous un format simplifié (titre, sujet, date, lien)

    :param address: Adresse URI du flux RSS
    :type address: str
    :return: Tuple constitué du Titre, Sujet, Lien, Date
    :type titre, sujet, lien, date: str
    """
    liste=[]
    feed = parse(address)
    for item in feed["items"]:
        titre = (item["title_detail"]["value"])
        sujet = (item["summary_detail"]["value"])
        if sujet.startswith("<img"):
            sujet = sujet.split("\"")
            sujet = sujet[1]
            image = sujet
            sujet = ""
        else :
            sujet = (item["summary_detail"]["value"])
            image = ""
        lien = (item["link"])
        date = (item["published"])
        rss = titre, sujet, image, lien, date
        liste.append(rss)
    titre, sujet, image, lien, date = liste[0]
    return titre, sujet, image, lien, date

def read_rss_bnf(address):
    """ Lit un flux RSS et les retourne sous un format simplifié (titre, sujet, date, lien)

    :param address: Adresse URI du flux RSS
    :type address: str
    :return: Tuple constitué du Titre, Sujet, Lien, Date
    :type titre, sujet, lien, date: str
    """
    liste=[]
    feed = parse(address)
    for item in feed["items"]:
        titre = (item["title_detail"]["value"])
        sujet = (item["summary_detail"]["value"])
        if sujet.startswith("<img"):
            sujet = sujet.split("\"")
            sujet = sujet[1]
            image = sujet
            sujet = ""
        else :
            sujet = (item["summary_detail"]["value"])
            image = ""
        if sujet.startswith("<p>"):
            sujet = sujet.replace("<p>", "")
            sujet = sujet.replace("</p>", "")

        lien = (item["link"])
        date = (item["published"])
        rss = titre, sujet, image, lien, date
        liste.append(rss)
    liste.sort(key=lambda liste: liste[4])
    titre, sujet, image, lien, date = liste[-1]
    return titre, sujet, image, lien, date

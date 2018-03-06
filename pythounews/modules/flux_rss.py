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
        lien = (item["link"])
        date = (item["published"])
        rss = titre, sujet, lien,  date
        liste.append(rss)
    titre, sujet, lien, date = liste[0]
    return titre, sujet, lien, date

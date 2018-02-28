from feedparser import parse

def read_rss(address):
    """ Read a RSS feed and returns a simpler format

    :param address: URI Address of the RSS Feed
    :type address: str
    :yields: Tuple of (Title, Summary, Link, Published)
    """
    liste=[]
    feed = parse(address)
    for item in feed["items"]:
        titre = (item["title_detail"]["value"])
        sujet = (item["summary_detail"]["value"])
        lien = (item["link"])
        date = (item["published"])
        rss = titre, sujet, lien, date
        liste.append(rss)
    rss_final = liste[0]
    return rss_final

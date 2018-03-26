INSERT INTO fluxrss 

VALUES (NULL, 'http://www.chartes.psl.eu/fr/rss', 'Ecole des chartes', 'http://www.chartes.psl.eu/fr' ),
(NULL, 'https://www.inha.fr/_plugins/web/inha/fr/filter/INHA-news/rss.xml', 'INHA', 'https://www.inha.fr/fr/index.html'),
(NULL, 'http://www.bnf.fr/Satellite?c=Page&cid=1237374444944&locale=1194947514616&p=1237374444944&pagename=bnf_dev%2FRss&typeRss=professionnelles', 'BNF : actualités professionnelles', 'http://www.bnf.fr/fr/acc/x.accueil.html'),
(NULL, 'http://www.bnf.fr/Satellite?c=Page&cid=1237374444944&locale=1194947514616&p=1237374444944&pagename=bnf_dev%2FRss&typeRss=Biblio', 'BNF : les bibliothèques', 'http://www.bnf.fr/fr/acc/x.accueil.html'),
(NULL, 'http://feeds2.feedburner.com/Biblioemplois', 'Biblioemplois', 'https://biblioemplois.wordpress.com'),
(NULL, 'https://siaf.hypotheses.org/feed', 'SIAF - Modernisation et Archives', 'https://siaf.hypotheses.org/');

INSERT INTO motscles

VALUES (NULL, 'Bibliothèques' ),
(NULL, 'Musées'),
(NULL, 'Archives'),
(NULL, 'Emploi'),
(NULL, 'Recherche');

INSERT INTO sujet_fluxrss

VALUES (NULL, 1, 1),
(NULL, 1, 2),
(NULL, 1, 3),
(NULL, 1, 5), 
(NULL, 2, 2),
(NULL, 2, 5), 
(NULL, 3, 1), 
(NULL, 3, 4), 
(NULL, 4, 1), 
(NULL, 4, 5), 
(NULL, 5, 1), 
(NULL, 5, 4), 
(NULL, 6, 3), 
(NULL, 6, 5);

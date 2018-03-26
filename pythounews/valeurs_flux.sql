INSERT INTO fluxrss 

VALUES (NULL, 'http://www.chartes.psl.eu/fr/rss', 'Ecole des chartes', 'http://www.chartes.psl.eu/fr' ),
(NULL, 'https://www.inha.fr/_plugins/web/inha/fr/filter/INHA-news/rss.xml', 'INHA', 'https://www.inha.fr/fr/index.html'),
(NULL, 'http://www.bnf.fr/Satellite?c=Page&cid=1237374444944&locale=1194947514616&p=1237374444944&pagename=bnf_dev%2FRss&typeRss=professionnelles', 'BNF : actualités professionnelles', 'http://www.bnf.fr/fr/acc/x.accueil.html'),
(NULL, 'http://www.bnf.fr/Satellite?c=Page&cid=1237374444944&locale=1194947514616&p=1237374444944&pagename=bnf_dev%2FRss&typeRss=Biblio', 'BNF : les bibliothèques', 'http://www.bnf.fr/fr/acc/x.accueil.html'),
(NULL, 'http://www.anhima.fr/spip.php?page=rss-actualites', 'ANHIMA', 'http://www.anhima.fr/'), 
(NULL, 'https://siaf.hypotheses.org/feed', 'SIAF - Modernisation et Archives', 'https://siaf.hypotheses.org/'),
(NULL, 'http://feeds2.feedburner.com/Biblioemplois', 'Biblioemplois', 'https://biblioemplois.wordpress.com');

INSERT INTO motscles

VALUES (NULL, 'Bibliothèques' ),
(NULL, 'Histoire de l\'Art'),
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
(NULL, 5, 2), 
(NULL, 5, 5),
(NULL, 6, 3), 
(NULL, 6, 5),
(NULL, 7, 1), 
(NULL, 7, 4);

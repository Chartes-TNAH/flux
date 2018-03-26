INSERT INTO user

VALUES 
('1', 'Marie-Gaëlle Gourio', 'Magg', 'Ministre de la magie', '2018', 'Archives', 'magg@pythounews.com', 'pbkdf2:sha256:50000$kA1x2kKT$2891b380597cae3d9e1b3bb67ecd956b82c09fa1a01431bdd010b08afa66763d', NULL),
('2', 'Alexandre Gaudin', 'Alex', 'Rescapé du Titanic par magie', '2012', 'Archives', 'alex@pythounews.com', 'pbkdf2:sha256:50000$4aiN5BCk$0a7d3dbf6178129fca6eacb665da02d9a602e922b1884db4f3bb6888ddef281f', NULL),
('3', 'Amandine Heathcote', 'Amandine', 'Evadée de la prison d\'azkaban et vainqueur de la coupe du monde de quidditch 2014', '2012', 'Archives', 'Amandinedu38@pythounews.com', 'pbkdf2:sha256:50000$6AahpDzU$e721fd2c8916c68c182d8dfdff6fc6d5ba486d3c9babfbd49c50dc6dffecffe0', NULL),
('4', 'Fanny Mézard', 'Fanny', 'Professeur d\'histoire de la magie et spécialiste de la mandragore', '1930', 'Archives', 'Fanny@pythounews.com', 'pbkdf2:sha256:50000$RlIj4Dog$4f7f644f066bbaec34a140389935f2cbb36d655ad91be456e54ee585a61555de', NULL),
('5', 'Anne-Laure Huet', 'Anne-Laure', 'Eleveuse d\'Hippogriffes', '2014', 'Histoire de l\'art', 'annelaure@pythounews.com', 'pbkdf2:sha256:50000$VV3rSUea$3056d7bdecf206f21e571ff1dae865e052ecfadb830989e0f2b9446b8d45e941', NULL);


INSERT INTO publication

VALUES (NULL, '2018-03-01','Open data et protection des donnees personnelles','https://www.archivistes.org/Open-data-et-protection-des-donnees-personnelles-ou-en-sommes-nous','L’AAF organise, à la suite de son Assemblée générale, le 30 mars 2018, une journée d’études sur l’Open data et le Règlement général sur la protection des données (RGPD).', '3'),
(NULL, '2018-03-11','Transcription collaborative','https://testaments-de-poilus.huma-num.fr/#!/','Le projet Testaments de Poilus vise à produire une édition électronique d’un millier de testaments des Poilus de la Première Guerre mondiale retrouvés dans les fonds des Archives nationales et des Archives Départementales des Yvelines.', '2'),
(NULL, '2018-03-21','UN QUEBECOIS DANS LES TRANCHEES', 'http://oasselin.omeka.net','bibliothèque numérique de correspondance du "poilu" québecois Olivar Asselin, visualisation de lettres, transcriptions, exports, exposition virtuelle', '1'),
(NULL, '2018-03-31','Webdev with Python and Flask','https://www.meetup.com/fr-FR/Canton-Python/events/246485923/?eventId=246485923','Dave Collins will be continuing the webdev track with Python and Flask. Now that we have our development tools setup we are ready to dig into building out our first app.', '4');

INSERT INTO sujet_publi 

VALUES (NULL, 1, 3),
(NULL, 2, 3),
(NULL, 2, 2),
(NULL, 3, 3),
(NULL, 4, 2)
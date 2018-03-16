from..app import db


class Publication(db.Model):
    publication_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    publication_date = db.Column(db.Text, nullable=False)
    publication_nom = db.Column(db.String(40), nullable=True)
    publication_lien = db.Column(db.Integer, nullable=True)
    publication_texte = db.Column(db.Text, nullable=False, unique=True)

    @staticmethod
    def creer_publication(titre, date, lien, texte):
        """ Crée une nouvelle publication et renvoie les informations rentrées par l'utilisateur.

        :param titre: Titre de la publication
        :param date: Date de la publication
        :param lien: URL partagé par l'utilisateur
        :param texte: Texte écrit par l'utilisateur
        :returns: Si réussite, publication de l'utilisateur. Sinon None
        :rtype: Publication or None
        """
        erreurs = []

        if not titre:
            erreurs.append("Le titre de votre publication n'est pas renseigné")
        if not date:
            erreurs.append("La date du jour doit être renseignée")
        if not lien:
            erreurs.append("Veuillez ajouter un lien à votre publication")

        if len(erreurs) > 0:
            return False, erreurs

        publication = Publication(
            publication_nom=titre,
            publication_date=date,
            publication_lien=lien,
            publication_texte=texte)

        try:
            db.session.add(publication)

            db.session.commit()

            return True, publication
        except Exception as erreur:
            return False, [str(erreur)]



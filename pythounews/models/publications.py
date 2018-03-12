from .. app import db, login

class publication(UserMixin, db.Model):
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
        

        
        titre = publication.query.filter(publication.publication_nom == titre).all()
        print(titre)
        date = publication.query.filter(publication.publication_date == date).all()
        print(date)
        lien = publication.query.filter(publication.publication_nom == titre).all()
        print(titre)
        print(motdepasse)
        print(utilisateur.user_password)
        if utilisateur and check_password_hash(utilisateur.user_password, motdepasse):
            return utilisateur
        return None
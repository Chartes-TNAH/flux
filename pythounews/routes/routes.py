# -*- coding: utf-8 -*-

from flask import render_template, request, flash, redirect
from flask_login import login_user, current_user, logout_user, login_required
from feedparser import parse
from bs4 import BeautifulSoup
import requests
from ..app import db
from ..app import app, login
from ..models import fluxrss
from ..models.utilisateurs import User
from ..models.publications import Publication
from ..models.motscles import Motscles, Sujet_publi
from ..models.fluxrss import Fluxrss
from ..models.fluxrss import Sujet_fluxrss


@app.route("/")
def accueil():
    """ Route permettant l'affichage de la page d'accueil

    :return: page html d'accueil
    """
    if current_user.is_authenticated is True:
        # n'ayant pas envie de refaire une nouvelle route, j'ai gardé tout le code la pagination de la page publication,
        # mais je n'affiche que les deux premiers éléments.
        pagination = Publication.query.order_by(Publication.publication_date.desc()).paginate(page=1, per_page=8)
        publications = Publication.afficher_publications(pagination)
        publications = publications[:2]
        liste_rss = Fluxrss.read_rss()
        return render_template("pages/accueil.html", liste_rss=liste_rss, publications=publications)
    else:
        liste_rss = Fluxrss.read_rss()
        return render_template("pages/accueil.html", liste_rss=liste_rss)


@app.route("/inscription", methods=["GET", "POST"])
def inscription():
    """ Route gérant les inscriptions des utilisateurs

    :return: page html inscription
    """
    # Si on est en POST, cela veut dire que le formulaire a été envoyé
    if request.method == "POST":
        statut, donnees = User.creer(
            login=request.form.get("login", None),
            email=request.form.get("email", None),
            bio=request.form.get("bio", None),
            nom=request.form.get("nom", None),
            spe=request.form.get("spe", None),
            promo=request.form.get("promo", None),
            motdepasse=request.form.get("motdepasse", None)
        )

        if statut is True:
            flash("Enregistrement effectué. Identifiez-vous maintenant", "success")
            return render_template("pages/connexion.html")
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "danger")
            return render_template("pages/inscription.html")
    else:
        return render_template("pages/inscription.html")


@app.route("/connexion", methods=["POST", "GET"])
def connexion():
    """ Route gérant les connexions des utilisateurs

    :return: page html de connexion au site
    """
    if current_user.is_authenticated is True:
        flash("Vous êtes connecté-e", "info")
        return redirect("/")
    if request.method == "POST":
        utilisateur = User.identification(
            login=request.form.get("login", None),
            motdepasse=request.form.get("motdepasse", None)
        )
        if utilisateur:
            flash("Connexion effectuée", "success")
            login_user(utilisateur)
            return redirect("/")
        else:
            flash("Les identifiants n'ont pas été reconnus", "danger")
            return render_template("pages/connexion.html")
    return render_template("pages/connexion.html")

    login.login_view = 'connexion'


@app.route("/deconnexion", methods=["POST", "GET"])
def deconnexion():
    """ Route permettant à l'utilisateur de se déconnecter

    :return: page html d'accueil, utilisateur déconnecté
    """
    if current_user.is_authenticated is True:
        logout_user()
    flash("Vous êtes déconnecté-e", "info")
    return redirect("/")


@app.route("/profil")
@login_required
def profil():
    """ Route permettant l'affichage du profil de l'utilisateur et l'affichage de ses publications.

    :return: page html profil de l'utilisateur
    """
    # On récupère l'id de l'utilisateur connecté
    id_utilisateur = current_user.user_id
    # On ne sélectionne parmi les publications que celles dont
    # l'id de l'auteur correspond à l'id de l'utilisateur, et on les classes par date.
    publications = Publication.query.filter(Publication.publi_user_id==id_utilisateur).order_by(Publication.publication_date.desc()).paginate(page=1)
    # On récupère l'ensemble des informations concernant les publications que l'on va afficher
    publications = Publication.afficher_publications(publications)

    return render_template("pages/profil.html", publications=publications)


@app.route("/modif_profil/<int:user_id>", methods=["POST", "GET"])
@login_required
def modif_profil(user_id):
    """ Route permettant à l'utilisateur de modifier les informations de son profil

    :param user_id: id de l'utilisateur
    :type user_id: integer
    :return: page html de modification du profil de l'utilisateur
    """

    if request.method == "POST":
        statut, donnees = User.modif_profil(
            user_id=user_id,
            email=request.form.get("email", None),
            login=request.form.get("login", None),
            nom=request.form.get("nom", None),
            bio=request.form.get("bio", None),
            spe=request.form.get("spe", None),
            promo=request.form.get("promo", None)
        )
        if statut is True:
            flash("Votre modification a bien été acceptée", "success")
            return redirect("/")

        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ", ".join(donnees), "danger")
            nouvel_utilisateur = User.query.get(user_id)
            return render_template("pages/modif_profil.html", user=nouvel_utilisateur)
    else:
        return render_template("pages/modif_profil.html", user=current_user)


@app.route("/afficher_profil_utilisateur/<int:user_id>")
@login_required
def afficher_profil_utilisateur(user_id):
    """ Route permettant d'afficher le profil d'un utilisateur lorsque l'on est connecté, et
    les publications attachées à cet utilisateur.

    :param user_id: ID de l'utilisateur connecté
    :type user_id: int
    :return: page html profil d'un utilisateur
    """
    # On récupère l'id de l'utilisateur
    utilisateur = User.query.get(user_id)
    # On ne sélectionne parmi les publications que celles dotn l'id de l'auteur correspond à l'id
    # de l'utilisateur, et on les classes par date.
    publications = Publication.query.filter(Publication.publi_user_id == utilisateur.user_id).order_by(Publication.publication_date.desc()).paginate(page=1)
    # On récupère l'ensemble des informations concernant les publications que l'on va afficher
    publications = Publication.afficher_publications(publications)

    return render_template("pages/profil_utilisateur.html", utilisateur=utilisateur, publications=publications)


@app.route("/recherche")
@login_required
def recherche():
    """ Route permettant la recherche plein-texte

    :return: page html résultats de la recherche
    """
    motclef = request.args.get("keyword", None)
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    if motclef:
        pagination = Publication.query.filter(db.or_(Publication.publication_nom.like("%{}%".format(motclef)),
                                                     Publication.publication_texte.like("%{}%".format(motclef)), Publication.publication_description_url.like("%{}%".format(motclef)))).paginate(page=page, per_page=3)
        publications = Publication.afficher_publications(pagination)
        return render_template("pages/recherche.html", publications=publications, keyword=motclef, pagination=pagination)


@app.route("/publication", methods=["GET", "POST"])
@login_required
def publication():
    """ Route permettant de poster une publication

    :return: page html de formulaire d'envoi des publications
    """

    # Si on est en POST, cela veut dire que le formulaire a été envoyé
    motscles = Motscles.query.all()
    categories = []
    if request.method == "POST":
        statut, donnees = Publication.creer_publication(
            titre=request.form.get("titre", None),
            lien=request.form.get("lien", None),
            texte=request.form.get("texte", None),
            auteur=current_user.user_id)
        for mot in motscles:
            mot = request.form.get(mot.motscles_nom, None)
            categories.append(mot)

        if statut is True:
            flash("publication effectuée.", "success")
            Sujet_publi.ajouter_categorie(categories, donnees)
            return redirect("/afficherpublis")
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + " , ".join(donnees), "danger")
            return render_template("pages/publication.html", motscles=motscles)
    else:
        return render_template("pages/publication.html", motscles=motscles)


@app.route("/afficherpublis")
@login_required
def afficherpublis():
    """ Route permettant l'affichage de l'ensemble des publications postées par les utilisateurs + pagination de la page

    :return: page html publications
    """

    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    pagination = Publication.query.order_by(Publication.publication_date.desc()).paginate(page=page, per_page=3)
    publications = Publication.afficher_publications(pagination)
    motscles = Motscles.query.all()

    return render_template("pages/afficherpublis.html", publications=publications, pagination=pagination, motscles=motscles)


@app.route("/afficherpublisCategorie/<int:motscles_id>")
@login_required
def afficherpublisCategorie(motscles_id):
    """ Route permettant l'affichage des publications des utilisateurs par mots clés

    :param motscles_id: id du mot clé
    :type motscles_id: integer
    :return: page html de publications selon les mots clefs
    """
    motcle = Motscles.query.get(motscles_id)
    motscles = Motscles.query.all()
    publications = Sujet_publi.afficher_publi_categorie(motcle)

    return render_template("pages/afficherpublisCategories.html", publications=publications, motscles=motscles, motcle=motcle)


@app.route('/rss')
def afficherrss():
    """ Route permettant l'affichage de l'ensemble des flux rss entrés dans la base

    :return: page html des flux rss
    """
    liste_rss = Fluxrss.read_rss()
    motscles = Motscles.query.all()
    return render_template("pages/afficherRss.html", liste_rss=liste_rss, motscles=motscles)


@app.route('/rss/<int:motscles_id>')
def afficherrssCategorie(motscles_id):
    """ Route permettant l'affichage des flux rss par mots clés entrés dans la base

    :return: page html des flux rss par mots clefs
    """
    motscles = Motscles.query.all()
    #On récupère l'id correspondant au mot-clé dont on souhaite avoir les flux correspondants.
    motcle = Motscles.query.get(motscles_id)
    #On récupère les flux rss qui ont un mot-clé dont l'id correspond à celui recherché.
    rss = Sujet_fluxrss.afficher_rss(motcle)

    return render_template("pages/afficherrssCategories.html", motcle=motcle, fluxrss=rss, motscles=motscles)


@app.route("/rsociaux")
def reseauxsociaux():
    """Route permettant d'afficher des fils d'actu twitter et facebook

    :return: page html avec plusieurs iframe
    """
    return render_template("pages/reseauxsociaux.html")


@app.route("/tnah")
def tnah():
    """ Route permettant l'affichage de la page 'A propos du master et du projet'

    :return: page html à propos
    """
    return render_template("pages/tnah.html", nom="A propos")


@app.route("/404")
@app.errorhandler(404)
def page_not_found(e):
    """Route permettant l'affichage d'un page 404 personnalisée

    :return: page html erreur 404
    """
    return render_template('pages/404.html'), 404

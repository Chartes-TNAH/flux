from flask import render_template, request, flash, redirect
from ..models import fluxrss
from feedparser import parse
from ..app import db

from bs4 import BeautifulSoup
import requests
from ..app import app, login
from flask_login import login_user, current_user, logout_user, login_required
from ..models.utilisateurs import User
from ..models.publications import Publication
from ..models.motscles import Motscles, Sujet_publi
from ..models.fluxrss import Fluxrss
from ..models.fluxrss import Sujet_fluxrss



@app.route("/tnah")
def tnah():
    """ Route permettant l'affichage de la page 'A propos du master et du projet'

    :return: page 'A propos du master et du projet'
    """
    return render_template("pages/tnah.html", nom="A propos")


@app.route("/connexion", methods=["POST", "GET"])
def connexion():
    """ Route gérant les connexions des utilisateurs

    :return: page de connexion au site
    """
    if current_user.is_authenticated is True:
        flash("Vous êtes connecté-e", "info")
        return redirect("/")
    if request.method == "POST":
        utilisateur=User.identification(
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


@app.route("/inscription", methods=["GET", "POST"])
def inscription():
    """ Route gérant les inscriptions des utilisateurs

    :return: page inscription
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
        print("donnee",donnees)
        print("statut", statut)

        if statut is True:
            flash("Enregistrement effectué. Identifiez-vous maintenant", "success")
            return render_template("pages/connexion.html")
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "danger")
            return render_template("pages/inscription.html")
    else:
        return render_template("pages/inscription.html")


@app.route("/deconnexion", methods=["POST", "GET"])
def deconnexion():
    """ Route permettant à l'utilisateur de se déconnecter

    :returns: page déconnexion
    """
    if current_user.is_authenticated is True:
        logout_user()
    flash("Vous êtes déconnecté-e", "info")
    return redirect("/")


@app.route("/")
def accueil():
    """ Route permettant l'affichage de la page d'accueil

    :returns: page d'accueil
    """
    if current_user.is_authenticated is True:
        #n'ayant pas envie de refaire une nouvelle route, j'ai gardé tout le code la pagination de la page publication,
        #mais je n'affiche que les 2 1ers éléments.
        pagination = Publication.query.order_by(Publication.publication_date.desc()).paginate(page=1, per_page=8)
        publications = Publication.afficher_publications(pagination)
        publications = publications[:2]
        liste_rss = Fluxrss.read_rss()
        return render_template ("pages/accueil.html", liste_rss=liste_rss, publications=publications)
    else:
        liste_rss = Fluxrss.read_rss()
        return render_template("pages/accueil.html", liste_rss=liste_rss)


@app.route("/modif_profil/<int:user_id>", methods=["POST", "GET"])
@login_required
def modif_profil(user_id) :
    """ Route permettant à l'utilisateur de modifier les informations de son profil

    :param user_id: id de l'utilisateur
    :type user_id: integer
    :returns: page de modification du profil de l'utilisateur
    """
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
        flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
        nouvel_utilisateur = User.query.get(user_id)
        return render_template("pages/modif_profil.html", user=nouvel_utilisateur)


@app.route("/profil")
@login_required
def profil():
    """ Route permettant l'affichage du profil de l'utilisateur

    :return: page profil de l'utilisateur
    """
    return render_template("pages/profil.html")


@app.route("/publication", methods=["GET", "POST"])
@login_required
def publication():
    """ Route permettant de poster une publication

    :returns: page de formulaire d'envoi des publications
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

@app.route('/rss')
def rss():
    """ Route permettant l'affichage de l'ensemble des flux rss entrés dans la base
    """
    liste_rss = Fluxrss.read_rss()
    motscles = Motscles.query.all()
    return render_template("pages/rss.html", liste_rss=liste_rss, motscles=motscles)


@app.route('/rss/<int:motscles_id>')
def afficherrss(motscles_id):
    """ Route permettant l'affichage des flux rss par mots clés entrés dans la base
    """
    motscles = Motscles.query.all()
    #On récupère l'id correspondant au mot-clé dont on souhaite avoir les flux correspondants.
    motcle = Motscles.query.get(motscles_id)
    #On récupère les flux rss qui ont un mot-clé dont l'id correspond à celui recherché.
    rss = Sujet_fluxrss.afficher_rss(motcle)

    return render_template("pages/afficherrssCategories.html", motcle=motcle, fluxrss=rss, motscles=motscles)


@app.route("/afficherpublis")
@login_required
def afficherpublis():
    """ Route permettant l'affichage de l'ensemble des publications postées par les utilisateurs + pagination de la page
    :returns: page publications
    """
    pagination = Publication.query.order_by(Publication.publication_date.desc()).paginate(page=1, per_page=8)
    publications = Publication.afficher_publications(pagination)
    motscles = Motscles.query.all()

    return render_template("pages/afficherpublis.html", publications=publications, pagination=pagination, motscles=motscles)

@app.route("/afficher_profil_utilisateur/<int:user_id>")
@login_required
def afficher_profil_utilisateur(user_id) :
    """ Route permettant d'afficher le profil d'un utilisateur lorsque l'on est connecté
    :returns: retourne la page profil d'un utilisateur
    """

    utilisateur = User.query.get(user_id)

    return render_template("pages/profil_utilisateur.html", utilisateur=utilisateur)


@app.route("/afficherpublisCategorie/<int:motscles_id>")
@login_required
def afficherpublisCategorie(motscles_id):
    """ Route permettant l'affichage des publications des utilisateurs par mots clés

    :param motscles_id: id du mot clé
    :type motscles_id: integer
    :return: page de publication correspond au mot clé
    """
    motcle = Motscles.query.get(motscles_id)
    motscles = Motscles.query.all()
    publications = Sujet_publi.afficher_publi_categorie(motcle)

    return render_template("pages/afficherpublis_categories.html", publications=publications, motscles=motscles)


@app.route("/recherche")
@login_required
def recherche():
    """ Route permettant la recherche plein-texte

    :returns: page résultats de la recherche
    """
    motclef = request.args.get("keyword", None)
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    resultats = []

    if motclef:
        resultats = Publication.query.filter(db.or_(Publication.publication_nom.like("%{}%".format(motclef)), Publication.publication_texte.like("%{}%".format(motclef)), Publication.publication_description_url.like("%{}%".format(motclef)))).paginate(page=page, per_page=3)

    return render_template("pages/recherche.html", resultats=resultats, keyword=motclef)


@app.route("/404")
@app.errorhandler(404)
def page_not_found(e):
    return render_template('pages/404.html'), 404

@app.route("/rsociaux")
def reseauxsociaux():
    """Route permettant d'afficher des fils d'actu twitter et facebook

    :returns : page avec plusieurs iframe
    """
    return render_template("pages/reseauxsociaux.html")

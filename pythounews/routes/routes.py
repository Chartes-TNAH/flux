from flask import render_template, request, flash, redirect
from pythounews.modules import flux_rss
from pythounews.modules.flux_rss import read_rss
from feedparser import parse

from ..app import app, login
from flask_login import login_user, current_user, logout_user, login_required
from ..models.utilisateurs import User


@app.route("/tnah")
def tnah():
    """Route permettant l'affichage de la page 'A propos du master et du projet'
    """
    return render_template("pages/tnah.html", nom="A propos")

@app.route("/connexion", methods=["POST", "GET"])
def connexion():
    """ Route gérant les connexions
    """
    if current_user.is_authenticated is True:
        flash("Vous êtes déjà connecté-e", "info")
        return redirect("/")
    # Si on est en POST, cela veut dire que le formulaire a été envoyé
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
            flash("Les identifiants n'ont pas été reconnus", "alert")

    return render_template("pages/connexion.html")

    login.login_view = 'connexion'


@app.route("/inscription", methods=["GET", "POST"])
def inscription():
    """ Route gérant les inscriptions
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
            return redirect("/")
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "alert")
            return render_template("pages/inscription.html")
    else:
        return render_template("pages/inscription.html")

@app.route("/deconnexion", methods=["POST", "GET"])
def deconnexion():
    """
    Route permettant à l'utilisateur de se déconnecter
    :return:

    """
    if current_user.is_authenticated is True:
        logout_user()
    flash("Vous êtes déconnecté-e", "info")
    return redirect("/")

@app.route("/")
def accueil():
    titre_chartes, sujet_chartes, image_chartes, lien_chartes, date_chartes = flux_rss.read_rss("http://www.chartes.psl.eu/fr/rss")
    titre_inha, sujet_inha, image_inha, lien_inha, date_inha = flux_rss.read_rss("https://www.inha.fr/_plugins/web/inha/fr/filter/INHA-news/rss.xml")
    titre_bnf, sujet_bnf, image_bnf, lien_bnf, date_bnf = flux_rss.read_rss_bnf("http://www.bnf.fr/Satellite?c=Page&cid=1237374444944&locale=1194947514616&p=1237374444944&pagename=bnf_dev%2FRss&typeRss=Biblio")
    titre_bnf_1, sujet_bnf_1, image_bnf_1, lien_bnf_1, date_bnf_1 = flux_rss.read_rss_bnf("http://www.bnf.fr/Satellite?c=Page&cid=1237374444944&locale=1194947514616&p=1237374444944&pagename=bnf_dev%2FRss&typeRss=professionnelles")
    return render_template("pages/accueil.html", titre_chartes=titre_chartes, sujet_chartes=sujet_chartes, lien_chartes=lien_chartes, date_chartes=date_chartes,
        titre_inha=titre_inha, sujet_inha=sujet_inha, image_inha=image_inha, lien_inha=lien_inha, date_inha=date_inha,
        titre_bnf=titre_bnf, sujet_bnf=sujet_bnf, image_bnf=image_bnf, lien_bnf=lien_bnf, date_bnf=date_bnf,
        titre_bnf_1=titre_bnf_1, sujet_bnf_1=sujet_bnf_1, image_bnf_1=image_bnf_1, lien_bnf_1=lien_bnf_1, date_bnf_1=date_bnf_1)

@app.route("/modif_profil/<int:user_id>", methods=["POST", "GET"])
@login_required
def modif_profil(user_id) :
    """
    Route permettant à l'utilisateur de modifier les informations de son profil
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
        return redirect("/")  # vers le lieu qu'il vient de créer.

    else:
        flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
        nouvel_utilisateur = User.query.get(user_id)
        return render_template("pages/modif_profil.html", user=nouvel_utilisateur)

@app.route("/profil")
@login_required
def profil():
    return render_template("pages/profil.html")

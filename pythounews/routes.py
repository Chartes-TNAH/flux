from flask import render_template, request, flash, redirect


from .app import app, login
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/tnah")
def tnah():
    """Route permettant l'affichage de la page 'A propos du master et du projet'
    """
    return render_template("pages/tnah.html", nom="A propos")

@app.route("/")
def connexion():
	return render_template("pages/connexion.html")

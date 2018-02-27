from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

chemin_actuel = os.path.dirname(os.path.abspath(__file__))
templates = os.path.join(chemin_actuel, "templates")
statics = os.path.join(chemin_actuel, "static")

# On initie l'extension
db = SQLAlchemy()

# On met en place la gestion d'utilisateur-rice-s
login = LoginManager()

app = Flask(
    __name__,
    template_folder=templates,
    static_folder=statics
)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://pythounews_user:password@localhost/pythounews'

from .routes import routes




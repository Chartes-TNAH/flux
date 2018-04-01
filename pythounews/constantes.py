# -*- coding: utf-8 -*-

from warnings import warn

SECRET_KEY = "J'AIME BEAUCOUP LES PYTHONS"

if SECRET_KEY == "JE SUIS UN SECRET !":
    warn("Le secret par défaut n'a pas été changé, vous devriez le faire", Warning)

# -*- coding: utf-8 -*-
"""
Flask-Login example
===================
This is a small application that provides a trivial demonstration of
Flask-Login, including remember me functionality.

:copyright: (C) 2011 by Matthew Frazier.
:license:   MIT/X11, see LICENSE for more details.
"""
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin,
                            confirm_login, fresh_login_required)

from flask_bootstrap import Bootstrap

try:
    from flask_login import AnonymousUser
except:
    from flask_login import AnonymousUserMixin as AnonymousUser

############################################################
############################################################
############################################################

## Setup a class for Users, then global dict to store users
## -> global dict of users is used to search for GET POST events

class User(UserMixin):
    def __init__(self, name, id, active = True):
        self.name = name
        self.id = id
        self.active = active

    def is_active(self):
        return self.active


class Anonymous(AnonymousUser):
    name = u"Anonymous"

USERS = {
    1 : User(u"Olives", 1),
    2 : User(u"JB", 2),
    3 : User(u"Miao", 3, False),
}

USER_NAMES = dict((u.name, u) for u in USERS.values())


############################################################
############################################################
############################################################

# Here we create global dictonary of authors to search on
# ...this part would be in a database
#
# Authors are created as class instances
class Author:
    def __init__(self, name, id):
        self.name = name
        self.id = id

        # Maybe we could link the Author.id
        # to a place (like a key) to the database
        # where the actual papers associated with
        # them would be.

    def getId(self):
        return self.id

AUTHORSS = {
    1 : Author(u"Getz", 1),
    2 : Author(u"Darwin", 2),
    3 : Author(u"Muellerklein", 3),
}

AUTHOR_NAMES = dict((u.name, u) for u in AUTHORSS.values())

############################################################
############################################################
############################################################

## Init the app

app = Flask(__name__)
Bootstrap(app)

SECRET_KEY = "stars_and_moon"
DEBUG = True

app.config.from_object(__name__)

login_manager = LoginManager()

login_manager.anonymous_user = Anonymous
login_manager.login_view = "login"
login_manager.login_message = u"Please log in to access this page."
login_manager.refresh_view = "reauth"

############################################################
############################################################
############################################################

## Setup Middleware / routes to each web page

@login_manager.user_loader
def load_user(id):
    return USERS.get(int(id))


login_manager.setup_app(app)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/secret")
@fresh_login_required
def secret():
    return render_template("secret.html")

# Creeate route for foo html
@app.route("/foo", methods = ["GET", "POST"])
def foo():
    if request.method == "POST":
        if "authorName" in request.form:
            authorName = request.form["authorName"]
        else:
            authorName = False
        if "keyWord" in request.form:
            keyWordd = request.form["keyWord"]
        else:
            keyWordd = False

        # Simple search if the string entered is in global dictonary
        if authorName in AUTHOR_NAMES:
            flash("Looking up author...")
            return render_template("bar.html", authorName = authorName, keyWord = keyWordd)
        else:
            flash(u"Sorry - we could not find that author. Please enter an author. E.g. 'Getz', 'Darwin', 'Muellerklein' etc.")
            return render_template("foo.html")

    return render_template("foo.html")

# Creeate route for bar html
@app.route("/bar", methods = ["GET", "POST"])
def bar():
    return render_template("bar.html")


@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST" and "username" in request.form:
        username = request.form["username"]
        if username in USER_NAMES:
            remember = request.form.get("remember", "no") == "yes"
            if login_user(USER_NAMES[username], remember = remember):
                flash("Logged in!")
                return redirect(request.args.get("next") or url_for("index"))
            else:
                flash("Sorry, but you could not log in.")
        else:
            flash(u"Invalid username.")
    return render_template("login.html")


@app.route("/reauth", methods = ["GET", "POST"])
@login_required
def reauth():
    if request.method == "POST":
        confirm_login()
        flash(u"Reauthenticated.")
        return redirect(request.args.get("next") or url_for("index"))
    return render_template("reauth.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for("index"))


## Note: this script is doing the equivalent of a NodeJS project
# files 'app.js' and all render middlewares in 'routes/'

# Create new pages with Middleware augment via
# '@app.route("/FOOBAR") ... def FOOBAR(): ... '

if __name__ == "__main__":
    app.run(port = 8888)

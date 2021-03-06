from flask import Blueprint, flash, redirect, render_template, request, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from flask_login import login_required, login_user, logout_user
from logbook.models import User, db
from peewee import fn

auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    return render_template("login.html")


@auth.route("/login", methods=["POST"])
def login_post():
    username = request.form.get("username")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    user = User.get_or_none(fn.Lower(User.username) == username.lower())

    # inform the user if the username/password is wrong
    if user is None or not check_password_hash(user.password, password):
        flash("Please check your login details and try again.")
        return redirect(url_for("logbook.index_next_pages"))

    login_user(user, remember=remember)
    return redirect(url_for("logbook.index_next_pages"))


@auth.route("/signup")
def signup():
    return render_template("signup.html")


@auth.route("/signup", methods=["POST"])
def signup_post():

    username = request.form.get("username").lower()
    password = request.form.get("password")

    user = User.get_or_none(
        fn.Lower(User.username) == username
    )  # if this returns a user, then the email already exists in database

    if user is not None:
        flash("Username already exists")
        return redirect(url_for("auth.signup"))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(
        username=username, password=generate_password_hash(password, method="sha256")
    )
    new_user.save()

    return redirect(url_for("auth.login"))


@auth.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

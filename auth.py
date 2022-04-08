from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from db import db
from constants import EMPLOYEE_ROLE
from forms.SignUp import SignUp
from models import User
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint("auth", __name__, url_prefix="/auth/")


@bp.route("/login")
def login():
    """Login page"""
    return render_template("auth/login.html")


@bp.route("/login", methods=["POST"])
def login_post():
    """
    Perform login
    Check user exists in db
    Check passwords match
    """
    # login code goes here
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash("login-error")
        return redirect(
            url_for("auth.login")
        )  # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=False)
    return redirect(url_for("views.home"))


@bp.route("/signup", methods=["GET", "POST"])
def signup():
    """
    Signup form
    Form throws error if user already exists
    """
    form = SignUp()
    if form.is_submitted() and form.validate():
        user = User(
            email=form.email.data,
            password=generate_password_hash(form.password.data, method="sha256"),
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            role=EMPLOYEE_ROLE,
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("auth.login"))
    return render_template("auth/signup.html", form=form)


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for(".login"))

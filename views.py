from cmath import log
from flask import redirect, render_template, request, url_for
from flask import Blueprint
from flask_login import current_user, login_fresh, login_required
from werkzeug.security import generate_password_hash

from models import Task
from models import User
from models import Incident
from constants import ADMIN_ROLE
from constants import EMPLOYEE_ROLE
from forms.Profile import Profile
from db import db

bp = Blueprint("views", __name__, url_prefix="/")


@bp.errorhandler(Exception)
def page_not_found(e):
    print(e)
    return render_template("errors/404.html"), 404


@bp.route("/")
def landing():
    """Landing, if logged in, send to home, if not prompt login"""
    if current_user and login_fresh():
        return redirect(url_for(".home"))
    return redirect(url_for("auth.login"))


@bp.route("/home")
@login_required
def home():
    """Manual check if user is authenticated so the user doesn't see a nasty error on their first time visiting the application"""
    users = User.query.all()
    return render_template("home.html", users=users)


@bp.route("/incidents")
@login_required
def incidents():
    """View all Incidents"""
    incidents = Incident.query.all()
    return render_template("incidents.html", incidents=incidents)


@bp.route("/incidents/<incident_id>")
@login_required
def incident(incident_id):
    """View a specific Incident"""
    query_incident = Incident.query.get(int(incident_id))
    users = User.query.all()
    return render_template("incident.html", incident=query_incident, users=users)


@bp.route("/tasks")
@login_required
def tasks():
    """View all tasks"""
    incidents = Incident.query.all()
    return render_template("incidents.html", incidents=incidents)


@bp.route("/tasks/<task_id>")
@login_required
def task(task_id):
    """View a specific task"""
    task = Task.query.get(int(task_id))
    users = User.query.all()
    return render_template("task.html", task=task, users=users)


@bp.route("/administration")
@login_required
def administration():
    """Administration view, only available to users with the ADMIN role"""
    users = User.query.all()
    print("users", users)

    # Button not available in UI without role, extra check for berevity
    if not current_user.role == ADMIN_ROLE:
        return ("You do not have permission to view that page", 404)
    print("hm")
    return render_template("administration.html", users=users)


@bp.route("/administration/<user_id>/revoke_admin")
@login_required
def revoke_admin(user_id):
    """Revoke admin privileges for a particular user account"""
    users = User.query.all()
    user = User.query.get(user_id)

    user.role = EMPLOYEE_ROLE
    db.session.commit()
    return render_template("administration.html", users=users)


@bp.route("/administration/<user_id>/apply_admin")
@login_required
def apply_admin(user_id):
    """Apply admin privileges for a particular user account"""
    users = User.query.all()
    user = User.query.get(user_id)

    user.role = ADMIN_ROLE
    db.session.commit()
    return render_template("administration.html", users=users)


@bp.route("/administration/<user_id>/delete")
@login_required
def delete_admin(user_id):
    """Remove a user account"""
    users = User.query.all()
    user = User.query.get(user_id)

    db.session.delete(user)
    db.session.commit()
    return render_template("administration.html", users=users)


@bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """Edit user profile data"""
    form = Profile()
    form.first_name.data = current_user.first_name
    form.last_name.data = current_user.last_name

    if request.method == "POST" and form.is_submitted() and form.validate():
        user = User.query.get(current_user.id)
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.password = generate_password_hash(form.password.data, method="sha256")

        db.session.commit()
        return redirect("/profile")

    return render_template("profile.html", form=form, current_user=current_user)

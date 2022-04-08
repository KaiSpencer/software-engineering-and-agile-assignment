from flask import Blueprint, flash, redirect, url_for, request

from models import Task
from models import User
from models import Incident
from db import db

bp_v1 = Blueprint("api", __name__, url_prefix="/api/v1/")


@bp_v1.route("/incident", methods=["POST"])
def create_incident():
    """
    Creates a new incident in the database.
    Once written redirect to incidents page, if this was the page the request came from data will simply refresh.
    """
    title = request.form.get("title")
    description = request.form.get("description")

    if not title or not description:
        if not title:
            flash("missing-title")
        if not description:
            flash("missing-description")
        return redirect(url_for("views.incidents"))

    incident = Incident(title=title, description=description)

    db.session.add(incident)
    db.session.commit()

    return redirect(url_for("views.incidents"))


@bp_v1.route("/incident/<id>/delete", methods=["GET"])
def delete_incident(id):
    """
    Deletes a given incident.
    """
    incident = Incident.query.get(id)
    db.session.delete(incident)
    db.session.commit()
    return redirect(url_for("views.incidents"))


@bp_v1.route("/incident/<id>", methods=["POST"])
def update_incident(id):
    """
    Updates an incident.
    """
    title = request.form.get("title")
    description = request.form.get("description")
    assignee_id = request.form.get("assignee")

    incident = Incident.query.get(id)
    incident.title = title
    incident.description = description
    if assignee_id:
        incident.assignee = User.query.get(assignee_id)

    db.session.commit()
    return redirect((f"/incidents/{id}"))


@bp_v1.route("/task", methods=["POST"])
def create_task():
    """
    Creates a new task in the database.
    """
    title = request.form.get("title")
    description = request.form.get("description")
    assignee_id = request.form.get("assignee")
    incident_id = request.args.get("incident_id")
    incident = Incident.query.get(incident_id)

    # Handle errors
    if not title or not description:
        if not title:
            flash("missing-title")
        if not description:
            flash("missing-description")
        return redirect(f"/incidents/{incident.id}")

    if not assignee_id:
        task = Task(title=title, description=description, incident=incident)
    else:
        task = Task(
            title=title,
            description=description,
            assignee=User.query.get(assignee_id),
            incident=incident,
        )

    db.session.add(task)
    db.session.commit()

    return redirect(f"/incidents/{incident.id}")


@bp_v1.route("/task/<id>/delete", methods=["GET"])
def delete_task(id):
    """
    Deletes a given task.
    """
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return redirect((f"/incidents/{task.incident_id}"))


@bp_v1.route("/task/<id>", methods=["POST"])
def update_task(id):
    """
    Updates a task.
    """
    title = request.form.get("title")
    description = request.form.get("description")
    assignee_id = request.form.get("assignee")

    task = Task.query.get(id)
    task.title = title
    task.description = description
    if assignee_id:
        task.assignee = User.query.get(assignee_id)

    db.session.commit()
    return redirect((f"/tasks/{id}"))

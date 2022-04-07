from flask_sqlalchemy import SQLAlchemy
from models import User
from models import Incident
from models import Task

from db import db


def db_setup(app):
    # db = SQLAlchemy(app)
    # db.create_all(app=app)
    # Create DB

    admin = User(username="Kai - Admin", email="admin@example.com", role="admin", id=1)
    guest = User(username="Ruth - Guest", email="guest@example.com", role="guest", id=2)

    incident1 = Incident(id=1, assignee_id=1, title="I am an incident title 1")
    incident2 = Incident(id=2, assignee_id=2, title="I am an incident title 2")

    task1 = Task(id=1, assignee_id=1, title="I am task title 1")
    task2 = Task(id=2, assignee_id=2, title="I am task title 2")
    task3 = Task(id=3, assignee_id=1, title="I am task title 2")
    task4 = Task(id=4, assignee_id=1, title="I am task title 2")

    db.session.add(admin)
    db.session.add(guest)
    db.session.add(incident1)
    db.session.add(incident2)
    db.session.add(task1)
    db.session.add(task2)
    db.session.add(task3)
    db.session.add(task4)
    db.session.commit()

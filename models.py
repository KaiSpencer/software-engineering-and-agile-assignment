from flask_login import UserMixin

from db import db


class User(UserMixin, db.Model):  # type: ignore
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(80), nullable=False)
    incidents = db.relationship("Incident", back_populates="assignee")
    tasks = db.relationship("Task", back_populates="assignee")

    def __repr__(self):
        return "<User %r>" % self.first_name

    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)


class Incident(db.Model):  # type: ignore
    __tablename__ = "incident"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    description = db.Column(db.Text)
    assignee = db.relationship("User", back_populates="incidents")
    assignee_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    tasks = db.relationship("Task", back_populates="incident")


class Task(db.Model):  # type: ignore
    __tablename__ = "task"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    description = db.Column(db.Text)
    assignee = db.relationship("User", back_populates="tasks")
    assignee_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    incident = db.relationship("Incident", back_populates="tasks")
    incident_id = db.Column(db.Integer, db.ForeignKey("incident.id"))

from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)


@app.route("/")
def hello_world():
    users = User.query.all()
    return render_template("hello.html", users=users)


@app.route("/incidents")
def incidents():
    incidents = Incident.query.all()
    return render_template("incidents.html", incidents=incidents)


class User(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return "<User %r>" % self.username


class Incident(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    assignee = db.Column(db.Integer, unique=True, nullable=True)

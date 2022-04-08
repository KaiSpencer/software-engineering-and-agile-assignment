import os

from flask import Flask
from dotenv import load_dotenv, find_dotenv
from werkzeug.security import generate_password_hash
from flask_login import LoginManager

from views import bp
from api import bp_v1 as api_bp
from auth import bp as auth_bp
from db import db

load_dotenv(find_dotenv())


def create_app():
    """
    App entry point
    Initialize database, views, login management
    """
    app = Flask(__name__)
    app.config["DEBUG"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
    app.config["SESSION_TYPE"] = "filesystem"
    app.secret_key = os.environ.get("SECRET_KEY")

    db.init_app(app)

    app.register_blueprint(bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from models import (
        User,
    )  # Fetch user class after db is initialized as it depends on the instance of db

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    if not os.path.exists("incident_management/database.db") and not os.path.exists(
        "database.db"
    ):
        with app.app_context():
            db.create_all()
            admin = User(
                first_name="Admin",
                last_name="Admin",
                email="admin@admin.com",
                role="ADMIN",
                password=generate_password_hash("adminadmin", method="sha256"),
            )
            db.session.add(admin)
            db.session.commit()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="localhost", port=8080)

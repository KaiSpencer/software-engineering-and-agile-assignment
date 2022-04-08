from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, EqualTo, Length, ValidationError

from models import User
from constants import NHSUK_FORM_STYLES


def user_already_exists(self, email):
    """
    Custom validator to ensure the user being registered does not already exist
    Check if the email exists in the database, if it does show an error.
    """
    user = User.query.filter_by(email=email.data).first()
    if user:
        raise ValidationError(
            "A user with this email already exists, Please login instead."
        )


class SignUp(FlaskForm):
    """Sign up form to register a new user to the web app"""

    class Meta:
        csrf = False

    email = EmailField(
        "email",
        validators=[
            InputRequired(message="Email is a required field"),
            user_already_exists,
        ],
        render_kw=NHSUK_FORM_STYLES["input"],
    )
    first_name = StringField(
        "first_name",
        validators=[InputRequired(message="First Name is a required field")],
        render_kw=NHSUK_FORM_STYLES["input"],
    )
    last_name = StringField(
        "last_name",
        validators=[InputRequired(message="Last Name is a required field")],
        render_kw=NHSUK_FORM_STYLES["input"],
    )
    password = PasswordField(
        "password",
        validators=[
            InputRequired(message="Password is a required field"),
            Length(
                min=8, max=150, message="Password must be between 8 and 150 characters"
            ),
        ],
        render_kw=NHSUK_FORM_STYLES["input"],
    )
    confirm_password = PasswordField(
        "confirm_password",
        validators=[
            InputRequired(message="Please confirm your password"),
            EqualTo("password", message="Passwords must match"),
        ],
        render_kw=NHSUK_FORM_STYLES["input"],
    )
    submit = SubmitField("Sign Up", render_kw=NHSUK_FORM_STYLES["button"])

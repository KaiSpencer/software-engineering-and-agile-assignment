from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, EqualTo, Length, ValidationError

from constants import NHSUK_FORM_STYLES


class Profile(FlaskForm):
    """Form to edit the current users profile"""

    class Meta:
        csrf = False

    first_name = StringField(
        "first_name",
        render_kw=NHSUK_FORM_STYLES["input"],
    )
    last_name = StringField(
        "last_name",
        render_kw=NHSUK_FORM_STYLES["input"],
    )
    password = PasswordField(
        "password",
        validators=[
            Length(
                min=8, max=150, message="Password must be between 8 and 150 characters"
            ),
        ],
        render_kw=NHSUK_FORM_STYLES["input"],
    )
    confirm_password = PasswordField(
        "confirm_password",
        validators=[
            EqualTo("password", message="Passwords must match"),
        ],
        render_kw=NHSUK_FORM_STYLES["input"],
    )
    submit = SubmitField("Update Profile", render_kw=NHSUK_FORM_STYLES["button"])

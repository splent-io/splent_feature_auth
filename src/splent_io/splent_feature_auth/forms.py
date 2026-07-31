from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired
from flask_babel import lazy_gettext as _l


class LoginForm(FlaskForm):
    # Lazy, not eager: a form class is built once at import time, before any
    # request has said what language it wants, so gettext here would freeze
    # whatever locale happened to be active during startup into every label
    # the product ever renders.
    email = StringField(_l("Email"), validators=[DataRequired()])
    password = PasswordField(_l("Password"), validators=[DataRequired()])
    remember_me = BooleanField(_l("Remember me"))
    submit = SubmitField(_l("Log in"))

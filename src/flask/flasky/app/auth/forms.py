from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField("Hasło", validators=[DataRequired()])
    remember_me = BooleanField("Zapisz")
    submit = SubmitField("Zaloguj")


class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField("Username", validators=[DataRequired(), Length(1, 64),
                                                   Regexp("^[A-Za-z][A-Za-z0-9_.]*$", 0,
                                                          "Usernames must have only letters, numbers, "
                                                          "dots or underscores")])
    password = PasswordField("Password", validators=[
        DataRequired(), EqualTo("password2", message="Passwords must match.")])
    password2 = PasswordField("Confirm password", validators=[DataRequired()])
    submit = SubmitField("Zarejestruj")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError("Email przypisany do innego konta.")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Username już istnieje.")

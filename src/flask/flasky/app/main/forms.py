from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, EmailField, BooleanField, widgets
from wtforms.validators import DataRequired


class MojaForma(FlaskForm):
    name = StringField("Jak masz na imię?", default=None, validators=[DataRequired()])
    priorytet_minimum = 0
    priorytet_maximum = 10
    priorytet = IntegerField(f"Priorytet ({priorytet_minimum} do {priorytet_maximum})", default=0,
                             widget=widgets.NumberInput(min=priorytet_minimum, max=priorytet_maximum))
    wyslij_email = BooleanField(default=False)
    email = EmailField("Email")
    submit = SubmitField("Wyslij")

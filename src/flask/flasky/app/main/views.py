from . import main
from ..models import User
from .forms import MojaForma
from .. import db
from flask import render_template, session, redirect, url_for, flash
import datetime
from ..email import send_email_message


@main.route("/", methods=["GET", "POST"])
def index():
    moja_forma = MojaForma()
    if moja_forma.validate_on_submit():
        name_from_db = User.query.filter_by(username=moja_forma.name.data).first()
        if name_from_db:
            flash(f"Uzytkownik {name_from_db.username} już istnieje.")
        else:
            # Dodanie do bazy danych
            user = User(email=moja_forma.email.data,
                        username=moja_forma.name.data.lower(),
                        priorytet=moja_forma.priorytet.data)
            db.session.add(user)
            db.session.commit()
            # Dodanie do cookies
            session["name"] = moja_forma.name.data
            session["priorytet"] = moja_forma.priorytet.data
            session["email"] = moja_forma.email.data
            if moja_forma.wyslij_email.data:
                send_email_message("Witamy na stronie Flasky", ["anana900@wp.pl"],
                                   "mail/email",  user=moja_forma.name.data,
                                   timestamp=datetime.datetime.now())
                flash(f"SUCCESS Wyslano email")
        # tutaj robimy przekierowanie zapobiegające ponownemy wysłaniu formularza w przypadku odświeżenia
        return redirect(url_for("main.index"))
    return render_template("index.html", current_time=datetime.datetime.utcnow(),
                           moja_forma=moja_forma, name=session.get("name"), priorytet=session.get("priorytet"),
                           email=session.get("email"))


@main.route("/user/<zmienna>")
def user(zmienna):
    lista = [f"{u.username} {u.email} Priorytet {u.priorytet}" for u in User.query.all()]
    return render_template("user.html", name=zmienna, lista=lista, element=2)

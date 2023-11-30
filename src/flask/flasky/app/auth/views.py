from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from ..models import User
from .forms import LoginForm, RegistrationForm
from..email import send_email_message


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.password_verify(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid email or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data.lower(),
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email_message("Potwierdz swoje konto", user.email,
                           "auth/email/confirm", user=user, token=token)
        flash('Potwierdź swój email')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route("/confirm/<token>")
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for("main.index"))
    if current_user.confirm_token(token):
        db.session.commit()
        flash("Konto zostało potwierdzone.")
    else:
        flash("Link potwierdzający jest nieprawidłowy.")
    return redirect(url_for("main.index"))


@auth.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if (not current_user.confirmed and request.endpoint and
                request.blueprint != "auth" and request.endpoint != "static"):
            return redirect(url_for("auth.unconfirmed"))


@auth.route("/unconfirmed")
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for("main.index"))
    return render_template("auth/unconfirmed.html")


@auth.route("/confirm")
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email_message("Potwierdz swoje konto", current_user.email,
                       "auth/email/confirm", user=current_user, token=token)
    flash('Nowa wiadomosc z potwierdzeniem została wysłana.')
    return redirect(url_for("main.index"))

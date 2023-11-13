from threading import Thread
from flask import render_template, current_app
from flask_mail import Message
from . import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email_message(subject, recipients, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(subject, sender=app.config['MAIL_SENDER'], recipients=[recipients])
    msg.body = render_template(template + ".txt", **kwargs)
    email_th = Thread(target=send_async_email, args=[app, msg])
    email_th.start()
    return email_th

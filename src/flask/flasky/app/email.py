from threading import Thread
from flask import render_template
from flask_mail import Message
from . import mail, main


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email_message(subject, recipients, template, **kwargs):
    msg = Message(subject, sender="botrobitorobak@gmail.com", recipients=recipients)
    msg.body = render_template(template + ".txt", **kwargs)
    email_th = Thread(target=send_async_email, args=[main, msg])
    email_th.start()
    return email_th

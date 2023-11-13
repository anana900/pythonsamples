from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app

@login_manager.user_loader  # zarejestrowanie funkcji w Flask-Login, które ją wywoła w chwili potrzeby pobrania info o user
def load_user(user_id):
    return User.query.get(int(user_id))


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship("User", backref="role", lazy="dynamic")

    def __repr__(self):
        return str(self.name)


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    priorytet = db.Column(db.Integer())
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))

    def __repr__(self):
        return str(self.username)

    @property
    def password(self):
        raise AttributeError("Odczyt hasla zabroniony")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def password_verify(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self):
        serial = Serializer(current_app.config["SECRET_KEY"])
        return serial.dumps({"confirm": self.id}).encode("utf-8")

    def confirm_token(self, token):
        serial = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = serial.loads(token.encode("utf-8"))
        except Exception as e:
            print("Problem with getting token")
            return False
        if data.get("confirm") != self.id:
            print("Problem with token confirmation")
            return False
        self.confirmed = True
        db.session.add(self)
        return True

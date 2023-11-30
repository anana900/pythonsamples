from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from . import login_manager
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app
from datetime import datetime


@login_manager.user_loader  # zarejestrowanie funkcji w Flask-Login, które ją wywoła w chwili potrzeby pobrania info o user
def load_user(user_id):
    return User.query.get(int(user_id))


class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship("User", backref="role", lazy="dynamic")
    default = db.Column(db.Boolean, default=False, index=True)
    permission = db.Column(db.Integer)

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permission is None:
            self.permission = 0

    def has_permission(self, perm):
        return self.permission & perm == perm

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permission += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permission -= perm

    def reset_permission(self):
        self.permission = 0

    def __repr__(self):
        return str(self.name)

    @staticmethod
    def insert_roles():
        roles = {"User": [Permission.FOLLOW,
                          Permission.COMMENT,
                          Permission.WRITE],
                 "Administrator": [Permission.FOLLOW,
                                   Permission.COMMENT,
                                   Permission.WRITE,
                                   Permission.MODERATE,
                                   Permission.ADMIN],
                 "Moderator": [Permission.FOLLOW,
                               Permission.COMMENT,
                               Permission.WRITE,
                               Permission.MODERATE]}
        default_role = 'User'
        for _role, _permissions_list in roles.items():
            role = Role.query.filter_by(name=_role).first()
            if role is None:
                role = Role(name=_role)
            for permission in _permissions_list:
                role.add_permission(permission)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    priorytet = db.Column(db.Integer())
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config["MAIL_SENDER"]:
                self.role = Role.query.filter_by(name="Administrator").first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def can(self, permission):
        return self.role is not None and self.role.has_permission(permission)
    
    def is_administrator(self):
        return self.can(Permission.ADMIN)

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
            print(f"Problem with getting token {e}")
            return False
        if data.get("confirm") != self.id:
            print("Problem with token confirmation")
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return str(self.username)


class AnonymousUser(AnonymousUserMixin):
    def can(self, permission):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser
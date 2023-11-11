from . import db


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship("User", backref="role")

    def __repr__(self):
        return f"Role {self.name}"


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    priorytet = db.Column(db.Integer())
    email = db.Column(db.String(64))
    city = db.Column(db.String(64))
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))

    def __repr__(self):
        return f"User {self.username}"

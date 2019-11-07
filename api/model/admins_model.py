from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from api import db


class Admin(db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    email = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name, email, password):
        self.name = name.title()
        self.email = email
        self.password = password

    @property
    def password(self):
        raise AttributeError('Sorry mate :|. Read only field')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(password)

    def __repr__(self):
        return f'Admin(name={self.name}, email={self.email})'

    def save(self):
        db.session.add(self)
        db.session.commit()
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from api import db


class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    othername = db.Column(db.String(50))
    reg_no = db.Column(db.String(11), unique=True, index=True)
    email = db.Column(db.String(128), index=True)
    level_id = db.Column(db.Integer, db.ForeignKey('levels.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    password_hash = db.Column(db.String(128))
    fingerprint_template = db.Column(db.String(256), unique=True, index=True, default=None)
    graduated = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, firstname=None, lastname=None, othername=None, reg_no=None, level=None, email=None, password=None):
        self.firstname = firstname
        self.lastname = lastname
        self.othername = othername
        self.reg_no = reg_no
        self.email = email
        self.password = password

    @property
    def password(self):
        raise AttributeError('Sorry mate :|. Read only field')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'User <name:{self.firstname} <reg_no:{self.reg_no}>>'

    def save(self):
        db.session.add(self)
        db.session.commit()

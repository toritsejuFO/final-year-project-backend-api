from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

import  arrow
import jwt

from api import db
from api.model import Level
from config import jwt_key


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
    reg_complete = db.Column(db.Boolean, default=False)

    def __init__(self, firstname=None, lastname=None, othername=None, reg_no=None, email=None, password=None):
        self.firstname = firstname
        self.lastname = lastname
        self.othername = othername
        self.reg_no = reg_no
        self.email = email
        self.password = password

    @property
    def to_dict(self):
        json_user = {
            'firstname': self.firstname,
            'lastname': self.lastname,
            'othername': self.othername,
            'reg_no': self.reg_no,
            'email': self.email,
            'level': self.get_level,
            'department': self.get_department,
            'school': self.get_school,
            'fingerprint': self.fingerprint_template,
            'graduated': self.graduated,
            'registered_on': arrow.get(self.created_at).for_json(),
            'registered_since': arrow.get(self.created_at).humanize(),
        }
        return json_user

    def encode_auth_token(self, data=None, expiry=datetime.utcnow() + timedelta(days=1)):
        if data is None:
            return 'Invalid "sub"[subscriber] passed'
        try:
            payload = {
                'sub': data,
                'exp': expiry,
                'iat': datetime.utcnow()
            }
            return jwt.encode(payload, jwt_key, algorithm='HS256')
        except Exception as e:
            return repr(e)

    @staticmethod
    def decode_auth_token(auth_token=None):
        try:
            payload = jwt.decode(auth_token, jwt_key)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Expired token. Please log in again'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again'

    @property
    def get_level(self):
        level = None
        if self.level is not None:
            level = self.level.level
        return level

    @property
    def get_department(self):
        department = None
        if self.department is not None:
            department = self.department.code
        return department

    @property
    def get_school(self):
        school = None
        if self.department is not None:
            school = self.department.school.code
        return school

    @property
    def password(self):
        raise AttributeError('Sorry mate :|. Read only field')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'User <name:{self.firstname}> <reg_no:{self.reg_no}>'

    def save(self):
        db.session.add(self)
        db.session.commit()

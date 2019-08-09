from datetime import datetime

import arrow
from werkzeug.security import generate_password_hash, check_password_hash

from api import db
from api.model import Department


class Lecturer(db.Model):
    __tablename__ = 'lecturers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(128), index=True)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name, email, department_code, password):
        self.name = name
        self.email = email
        self.department = Department.query.filter_by(code=department_code).first()
        self.password = password

    @property
    def to_dict(self):
        json_lecturer = {
            'name': self.name,
            'email': self.email,
            'department': self.department.code,
            'school': self.department.school.code,
            'registered_on': arrow.get(self.created_at).for_json(),
            'registered_since': arrow.get(self.created_at).humanize(),
        }
        return json_lecturer

    @property
    def password(self):
        raise AttributeError('Sorry mate :|. Read only field')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'Lecturer(name={self.name}, email={self.email})'

    def save(self):
        db.session.add(self)
        db.session.commit()
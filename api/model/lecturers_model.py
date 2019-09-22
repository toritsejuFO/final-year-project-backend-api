import os
from datetime import datetime

import arrow
from werkzeug.security import generate_password_hash, check_password_hash

from api import db
from api.model import Department
from api import select_table_name

session = os.environ.get('CURRENT_ASSIGNED_COURSES_SESSION')
semester = os.environ.get('CURRENT_ASSIGNED_COURSES_SEMESTER')
table_name = select_table_name(f'ASSIGNED_COURSES_{semester}_{session}')

assigned_courses = db.Table(table_name,
                            db.Column('lecturer_id', db.Integer, db.ForeignKey(
                                'lecturers.id'), primary_key=True),
                            db.Column('course_id', db.Integer, db.ForeignKey(
                                'courses.id'), primary_key=True)
                            )


class Lecturer(db.Model):
    __tablename__ = 'lecturers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(128), index=True)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    password_hash = db.Column(db.String(128))
    assigned_courses = db.relationship('Course', secondary=assigned_courses,
                                       backref=db.backref('lecturers_assigned', lazy='dynamic'), lazy='dynamic')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name, email, department_code, password):
        self.name = name.title()
        self.email = email
        self.department = Department.query.filter_by(
            code=department_code).first()
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

    def assign_course(self, course):
        if not self.is_assigned(course):
            self.assigned_courses.append(course)

    def is_assigned(self, course):
        return self.assigned_courses.filter(assigned_courses.c.course_id == course.id).count() > 0

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

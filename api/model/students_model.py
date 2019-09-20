import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

import arrow

from api import db, select_table_name
from api.model import Level

session = os.environ.get('CURRENT_REGISTERED_COURSES_SESSION')
semester = os.environ.get('CURRENT_REGISTERED_COURSES_SEMESTER')
table_name = select_table_name(f'REGISTERED_COURSES_{semester}_{session}')

registered_courses = db.Table(table_name,
                              db.Column('student_id', db.Integer, db.ForeignKey(
                                  'students.id'), primary_key=True),
                              db.Column('course_id', db.Integer, db.ForeignKey(
                                  'courses.id'), primary_key=True)
                              )


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
    fingerprint_template = db.Column(db.String(1112), unique=True, default=None)
    graduated = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reg_complete = db.Column(db.Boolean, default=False)
    registered_courses = db.relationship('Course', secondary=registered_courses, backref=db.backref(
        'students_registered', lazy='dynamic'), lazy='dynamic')
    has_registered_course = db.Column(db.Boolean, default=False)

    def __init__(self, firstname=None, lastname=None, othername=None, reg_no=None, email=None, password=None):
        self.firstname = firstname.title()
        self.lastname = lastname.title()
        self.othername = othername.title()
        self.reg_no = reg_no
        self.email = email
        self.password = password

    @property
    def to_dict(self):
        json_student = {
            'firstname': self.firstname,
            'lastname': self.lastname,
            'othername': self.othername,
            'reg_no': self.reg_no,
            'email': self.email,
            'level': self.get_level,
            'department': self.get_department,
            'school': self.get_school,
            'fingerprint': True if self.fingerprint_template else False,
            # 'graduated': self.graduated,
            'reg_completed': self.reg_complete,
            # 'registered_on': arrow.get(self.created_at).for_json(),
            # 'registered_since': arrow.get(self.created_at).humanize(),
            'has_registered_courses': self.has_registered_course
        }
        return json_student

    def register_course(self, course):
        if not self.is_registered(course):
            self.registered_courses.append(course)

    def is_registered(self, course):
        return self.registered_courses.filter(registered_courses.c.course_id == course.id).count() > 0

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

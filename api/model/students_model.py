import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

import arrow

from api import db, select_table_name
from api.model import Level

session = os.environ.get('CURRENT_REGISTERED_COURSES_SESSION')
semester = os.environ.get('CURRENT_REGISTERED_COURSES_SEMESTER')
registered_courses_table_name = select_table_name(f'REGISTERED_COURSES_{semester}_{session}')
exam_table_name = select_table_name(f'STUDENTS_EXAM_{semester}_{session}')
student_lectures_table_name = select_table_name(f'STUDENT_LECTURES_{semester}_{session}')
lecturer_lectures_table_name = select_table_name(f'LECTURER_LECTURES_{semester}_{session}')

registered_courses = db.Table(registered_courses_table_name,
    db.Column('student_id', db.Integer, db.ForeignKey('students.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'), primary_key=True))

exam_attendance = db.Table(exam_table_name,
    db.Column('student_id', db.Integer, db.ForeignKey('students.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'), primary_key=True))

lecture_attendance = db.Table(student_lectures_table_name,
    db.Column('student_id', db.Integer, db.ForeignKey('students.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'), primary_key=True),
    db.Column('count', db.Integer, default=0))


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
    exam_attendance = db.relationship('Course', secondary=exam_attendance, backref=db.backref(
        'students_exam_attended', lazy='dynamic'), lazy='dynamic')
    lecture_attendance = db.relationship('Course', secondary=lecture_attendance,
        backref=db.backref('student_lecture_attended', lazy='dynamic'), lazy='dynamic')
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

    def take_exam_attendance(self, course):
        if not self.exam_attendance_taken(course):
            self.exam_attendance.append(course)

    def exam_attendance_taken(self, course):
        return self.exam_attendance.filter(exam_attendance.c.course_id == course.id).count() > 0

    def attend_lecture(self, course, lecturer):
        if not self.is_lecture_attended(course):
            self.lecture_attendance.append(course)
            db.session.commit()

        # Get current lecturer lecture count
        sql = f'''
            SELECT count
            FROM {lecturer_lectures_table_name}
            WHERE lecturer_id = {lecturer.id}
            AND course_id = {course.id}
            LIMIT 1
        '''
        result = db.session.execute(sql)
        lecturer_lecture_count = result.fetchone()[0]
        print(lecturer_lecture_count)

        # Check if attendance has been taken by student
        sql = f'''
            SELECT day{lecturer_lecture_count}
            FROM {student_lectures_table_name}
            WHERE student_id = {self.id}
            AND course_id = {course.id}
            LIMIT 1
        '''
        result = db.session.execute(sql)
        student_lecture_count_for_day = result.fetchone()[0]

        if student_lecture_count_for_day == 0:
            sql = f'''
                UPDATE {student_lectures_table_name}
                SET day{lecturer_lecture_count} = 1, count = count + 1
                WHERE student_id = {self.id}
                AND course_id = {course.id}
            '''
            result = db.session.execute(sql)

    def is_lecture_attended(self, course):
        return self.lecture_attendance.filter(lecture_attendance.c.course_id == course.id).count() > 0

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
        return f'Student <name:{self.firstname}> <reg_no:{self.reg_no}>'

    def save(self):
        db.session.add(self)
        db.session.commit()

import os
from datetime import datetime

import arrow
from werkzeug.security import generate_password_hash, check_password_hash

from api import db
from api.model import Department
from api import select_table_name

session = os.environ.get('CURRENT_ASSIGNED_COURSES_SESSION')
semester = os.environ.get('CURRENT_ASSIGNED_COURSES_SEMESTER')
DB_NAME = os.environ.get('DB_NAME')
assigned_courses_table_name = select_table_name(f'ASSIGNED_COURSES_{semester}_{session}')
lecturer_lectures_table_name = select_table_name(f'LECTURER_LECTURES_{semester}_{session}')
student_lectures_table_name = select_table_name(f'STUDENT_LECTURES_{semester}_{session}')

assigned_courses = db.Table(assigned_courses_table_name,
    db.Column('lecturer_id', db.Integer, db.ForeignKey('lecturers.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'), primary_key=True))

lecture_attendance = db.Table(lecturer_lectures_table_name,
    db.Column('lecturer_id', db.Integer, db.ForeignKey('lecturers.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'), primary_key=True),
    db.Column('count', db.Integer, default=1))


class Lecturer(db.Model):
    __tablename__ = 'lecturers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(128), index=True)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    password_hash = db.Column(db.String(128))
    assigned_courses = db.relationship('Course', secondary=assigned_courses,
        backref=db.backref('lecturers_assigned', lazy='dynamic'), lazy='dynamic')
    lecture_attendance = db.relationship('Course', secondary=lecture_attendance,
        backref=db.backref('lecturer_lecture_attended', lazy='dynamic'), lazy='dynamic')
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
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'department': self.department.code,
            'school': self.department.school.code,
            # 'registered_on': arrow.get(self.created_at).for_json(),
            # 'registered_since': arrow.get(self.created_at).humanize(),
        }
        return json_lecturer

    def assign_course(self, course):
        if not self.is_assigned(course):
            self.assigned_courses.append(course)

    def is_assigned(self, course):
        return self.assigned_courses.filter(assigned_courses.c.course_id == course.id).count() > 0

    def attend_lecture(self, course):
        if not self.is_lecture_attended(course):
            self.lecture_attendance.append(course)
            # Create lecture day1 column in students lecture table if column doesn't exist
            sql = f'''
                SHOW COLUMNS
                FROM {student_lectures_table_name}
                LIKE 'day1'
            '''
            result = db.session.execute(sql)
            column_exists = result.fetchone()

            if not column_exists:
                sql = f'''
                    ALTER TABLE {student_lectures_table_name}
                    ADD day1 INT NOT NULL DEFAULT 0
                '''
                db.session.execute(sql)
        else:
            # Increment lecture attendance count for lecturer
            sql = f'''
                UPDATE {lecturer_lectures_table_name}
                SET count = count + 1
                WHERE lecturer_id = {self.id}
                AND course_id = {course.id}
            '''
            db.session.execute(sql)
            db.session.commit()

            # Get current lecturer lecture count
            sql = f'''
                SELECT count
                FROM {lecturer_lectures_table_name}
                WHERE lecturer_id = {self.id}
                AND course_id = {course.id}
                LIMIT 1
            '''
            result = db.session.execute(sql)
            lecture_count = result.fetchone()[0]
            
            # Create lecture day column in students lecture table with current count if column doesn't exist
            sql = f'''
                SHOW COLUMNS
                FROM {student_lectures_table_name}
                LIKE 'day{lecture_count}'
            '''
            result = db.session.execute(sql)
            column_exists = result.fetchone()

            if not column_exists:
                sql = f'''
                    ALTER TABLE {student_lectures_table_name}
                    ADD day{lecture_count} INT NOT NULL DEFAULT 0
                '''
                db.session.execute(sql)


    def is_lecture_attended(self, course):
        return self.lecture_attendance.filter(lecture_attendance.c.course_id == course.id).count() > 0

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

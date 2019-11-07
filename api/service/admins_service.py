import os

from collections import namedtuple

from api import db, AppException, select_table_name
from api.model import Course, Department, Admin


class AdminsService():
    @staticmethod
    def create(data):
        response = {}
        try:
            admin = Admin(**data)
            admin.save()
        except Exception:
            db.session.rollback()
            raise AppException('Internal Server Error', 500)

        response['success'] = True
        response['message'] = 'New admin registered successfully'
        return response, 201

    @staticmethod
    def get_oar(session, semester, course_code, department_code):
        response = {}

        # Find course and department
        try:
            course = Course.query.filter_by(code=course_code).first()
            department = Department.query.filter_by(code=department_code).first()
        except Exception:
            raise AppException('Internal Server Error', 500)

        if not course or not department:
            response['success'] = False
            response['message'] = 'Invalid department or course'
            return response, 404

        # Perform formatting to check if table with provided session and semester exists
        formatted_session = session.lstrip('20')[0] + session.lstrip('20')[1]
        table_to_search = f'STUDENTS_EXAM_{semester.upper()}_{formatted_session}'
        table_name = select_table_name(table_to_search)

        if table_name is None:
            response['success'] = False
            response['message'] = 'Invalid session or semester selected'
            return response, 404

        # Perform query and fetch students
        try:
            sql = f'''
                SELECT firstname, lastname, othername, reg_no
                FROM students
                INNER JOIN {table_name} ON {table_name}.student_id = students.id
                WHERE students.department_id = {department.id}
                AND {table_name}.course_id = {course.id}
            '''
            result = db.session.execute(sql)
            Student = namedtuple('Student', result.keys())
        except Exception:
            raise AppException('Internal Server Error', 500)

        response['data'] = []
        for record in result.fetchall():
            student = Student(*record)
            data = {}
            data['firstname'] = student.firstname
            data['lastname'] = student.lastname
            data['othername'] = student.othername
            data['reg_no'] = student.reg_no
            response['data'].append(data)

        response['success'] = True
        return response, 200

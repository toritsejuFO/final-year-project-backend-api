import os

from collections import namedtuple

from api import db, AppException, select_table_name
from api.model import Course, Department, Admin, Level, Student


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
    def get_exam_oar(session, semester, course_code, department_code, email):
        response = {}

        try:
            admin = Admin.query.filter_by(email=email).first()
        except Exception:
            raise AppException('Internal Server Error', 500)

        if not admin:
            response['success'] = False
            response['message'] = 'Admin Not Found'
            return response, 404

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

    @staticmethod
    def get_lecture_oar(session, semester, course_code, department_code, email):
        response = {}

        try:
            admin = Admin.query.filter_by(email=email).first()
        except Exception:
            raise AppException('Internal Server Error', 500)

        if not admin:
            response['success'] = False
            response['message'] = 'Admin Not Found'
            return response, 404

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
        table_to_search = f'STUDENT_LECTURES_{semester.upper()}_{formatted_session}'
        table_name = select_table_name(table_to_search)

        if table_name is None:
            response['success'] = False
            response['message'] = 'Invalid session or semester selected'
            return response, 404

        # Perform query and fetch students
        try:
            # Get lecturer total lecture count for course
            lecturer_table_to_search = f'LECTURER_LECTURES_{semester.upper()}_{formatted_session}'
            lecturer_lectures_table_name = select_table_name(lecturer_table_to_search)
            sql = f'''
                SELECT count
                FROM {lecturer_lectures_table_name}
                WHERE course_id = {course.id}
                LIMIT 1
            '''
            result = db.session.execute(sql)
            record = result.fetchone()
            # print(result.fetchone())
            if not record:
                response['success'] = False
                response['message'] = 'No lecture has been taken for this class this session/semester'
                return response, 403

            lecturer_lecture_count = record[0]
            sql_count = ' '
            for day_count in range(lecturer_lecture_count):
                sql_count += f'day{day_count + 1}, '
            # print(lecturer_lecture_count)
            # print(sql_count)

            # Get student details
            sql = f'''
                SELECT firstname, lastname, othername, reg_no, {sql_count} count
                FROM students
                INNER JOIN {table_name} ON {table_name}.student_id = students.id
                WHERE students.department_id = {department.id}
                AND {table_name}.course_id = {course.id}
            '''
            result = db.session.execute(sql)
            Student = namedtuple('Student', result.keys())
        except Exception:
            raise AppException('Internal Server Error', 500)

        response['data'] = {'students': [], 'lecturer_count': lecturer_lecture_count}
        for record in result.fetchall():
            # print(record)
            student = Student(*record)
            # print(student)
            data = {}
            data['firstname'] = student.firstname
            data['lastname'] = student.lastname
            data['othername'] = student.othername
            data['reg_no'] = student.reg_no
            for day_count in range(lecturer_lecture_count):
                data[f'day{day_count + 1}'] = record[day_count + 4]
            data['count'] = student.count
            response['data']['students'].append(data)

        response['success'] = True
        return response, 200

    @staticmethod
    def get_mastersheet(session, semester, level, department_code, email):
        response = {}

        try:
            admin = Admin.query.filter_by(email=email).first()
        except Exception:
            raise AppException('Internal Server Error', 500)

        if not admin:
            response['success'] = False
            response['message'] = 'Admin Not Found'
            return response, 404

        # Find level and department
        try:
            department = Department.query.filter_by(code=department_code).first()
            level = Level.query.filter_by(level=level).first()
        except Exception:
            raise AppException('Internal Server Error', 500)

        if not level or not department:
            response['success'] = False
            response['message'] = 'Invalid department or level'
            return response, 404

        try:
            students = Student.query.filter_by(department=department, level=level).all()
        except Exception:
            raise AppException('Internal Server Error', 500)

        if not students:
            response['success'] = False
            response['message'] = 'Student Not Found'
            return response, 404

        # Perform formatting to check if table with provided session and semester exists
        formatted_session = session.lstrip('20')[0] + session.lstrip('20')[1]
        table_to_search = f'STUDENT_LECTURES_{semester.upper()}_{formatted_session}'
        table_name = select_table_name(table_to_search)

        if table_name is None:
            response['success'] = False
            response['message'] = 'Invalid session or semester selected'
            return response, 404

        # Get json serialized data object
        students_data = [student.to_dict for student in students]
        try:
            for index, student in enumerate(students):
                # add registered column attribute
                students_data[index]['registered_courses'] = []

                # Append json serialized registered courses and count to each student data object
                for registered_course in student.registered_courses.all():
                    sql = f'''
                        SELECT count
                        FROM {table_name}
                        WHERE {table_name}.student_id = {student.id}
                        AND {table_name}.course_id = {registered_course.id}
                        LIMIT 1
                    '''
                    result = db.session.execute(sql)
                    record = result.fetchone()
                    count = record[0] if record is not None else 0
                    students_data[index]['registered_courses'].append({f'{registered_course.code}': count})
        except Exception:
            raise AppException('Internal Server Error', 500)

        response['success'] = True
        response['data'] = students_data
        return response, 200

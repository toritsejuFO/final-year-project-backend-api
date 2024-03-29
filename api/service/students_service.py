from api import db, AppException
from api.model import Student, Department, Level, Course, Lecturer


class StudentService():
    @staticmethod
    def get_all_students():
        response = {}
        try:
            students = Student.query.all()
        except Exception:
            raise AppException('Internal Server Error', 500)

        if not students:
            response['success'] = False
            response['message'] = 'Students Not Found'
            return response, 404

        response['success'] = True
        response['data'] = [student.to_dict for student in students]
        return response, 200

    @staticmethod
    def create_student(data=None):
        response = {}
        try:
            student = Student(**data)
            student.save()
        except Exception:
            db.session.rollback()
            raise AppException('Internal Server Error', 500)

        response['success'] = True
        response['message'] = 'New student successfully registered'
        return response, 201

    @staticmethod
    def get_me(reg_no):
        response = {}
        try:
            student = Student.query.filter_by(reg_no=reg_no).first()
        except Exception:
            raise AppException('Internal Server Error', 500)

        if not student:
            response['success'] = False
            response['message'] = 'Student Not Found'
            return response, 404

        response['success'] = True
        response['data'] = student.to_dict
        return response, 200

    @staticmethod
    def edit_me(reg_no, data):
        response = {}
        level = data['level']
        department = data['department']
        try:
            student = Student.query.filter_by(reg_no=reg_no).first()
        except Exception:
            raise AppException('Internal Server Error', 500)

        if not student:
            response['success'] = False
            response['message'] = 'Student Not Found'
            return response, 404

        if student.reg_complete:
            response['success'] = False
            response['message'] = "You cannot update your details anymore. Contact Admin"
            return response, 423

        try:
            student.level = Level.query.filter_by(level=level).first()
            student.department = Department.query.filter_by(code=department).first()
            student.reg_complete = True
            student.save()
        except Exception:
            db.session.rollback()
            raise AppException('Internal Server Error', 500)

        response['success'] = True
        response['message'] = 'Details updated successfully'
        return response, 200

    @staticmethod
    def get_me_courses(reg_no, semester):
        response = {}
        try:
            student = Student.query.filter_by(reg_no=reg_no).first()
        except Exception:
            raise AppException('Internal Server Error', 500)

        if not student:
            response['success'] = False
            response['message'] = 'Student Not Found'
            return response, 404

        # Select courses based on student's level and current semester
        # If and only if student has completed registration
        if not student.reg_complete or not student.fingerprint_template:
            response['success'] = False
            response['message'] = 'Student registration is incomplete and thus can not access courses'
            return response, 423

        try:
            courses = list(filter(
                lambda c: c.semester.semester == semester and c.level.level == student.level.level,
                student.department.courses))
        except Exception:
            raise AppException('Internal Server Error', 500)


        response['success'] = True
        response['data'] = [course.to_dict for course in courses]
        return response, 200

    @staticmethod
    def register_courses(reg_no, data):
        response = {}
        try:
            student = Student.query.filter_by(reg_no=reg_no).first()
        except Exception:
            raise AppException('Internal Server Error', 500)

        if not student:
            response['success'] = False
            response['message'] = 'Student Not Found'
            return response, 404

        if not student.reg_complete or not student.fingerprint_template:
            response['success'] = False
            response['message'] = 'You must complete your registration and thumbprint before registering your courses'
            return response, 423

        if student.has_registered_course:
            response['success'] = False
            response['message'] = 'Registration can only be done once. Contact Admin'
            return response, 423

        try:
            course_codes = data['courses']
            for course_code in course_codes:
                course = Course.query.filter_by(code=course_code).first()
                student.register_course(course)
            db.session.commit()
            student.has_registered_course = True
            student.save()
        except Exception:
            db.session.rollback()
            raise AppException('Internal Server Error', 500)

        response['success'] = True
        response['message'] = 'Courses registered successfully'
        return response, 200

    @staticmethod
    def get_registered_courses(reg_no):
        response = {}
        try:
            student = Student.query.filter_by(reg_no=reg_no).first()
        except Exception:
            raise AppException('Internal Server Error', 500)

        if not student:
            response['success'] = False
            response['message'] = 'Student Not Found'
            return response, 404

        response['success'] = True
        response['data'] = [course.to_dict for course in student.registered_courses.all()]
        return response, 200

    @staticmethod
    def register_fingerprint(reg_no, data):
        response = {}
        try:
            student = Student.query.filter_by(reg_no=reg_no).first()
        except Exception:
            raise AppException('Internal Server Error', 500)

        if not student:
            response['success'] = False
            response['message'] = 'Student Not Found'
            return response, 404

        if student.fingerprint_template:
            response['success'] = False
            response['message'] = 'Fingerprint registration can only be done once. Contact Admin'
            return response, 423

        try:
            student.fingerprint_template = data['template']
            student.save()
        except Exception:
            db.session.rollback()
            raise AppException('Internal Server Error', 500)

        response['success'] = True
        response['message'] = 'Fingerprint registered successfully'
        return response, 200

    @staticmethod
    def verify_registered_courses(reg_no, course_code):
        response = {}
        try:
            student = Student.query.filter_by(reg_no=reg_no).first()
        except Exception:
            raise AppException('Internal Server Error', 500)

        if not student:
            response['success'] = False
            response['message'] = 'Student Not Found'
            return response, 404

        try:
            registered_course = student.registered_courses.filter_by(code=course_code).first()
        except Exception:
            raise AppException('Internal Server Error', 500)

        if not registered_course:
            response['success'] = False
            response['message'] = 'Student has not registered for this course'
            return response, 200

        response['success'] = True
        response['message'] = 'Student has registered for this course'
        return response, 200

    @staticmethod
    def get_registered_students(course_code, department_code):
        response = {}
        try:
            registered_students = Course.query.filter_by(code=course_code).first().students_registered
        except Exception:
            raise AppException('Internal Server Error', 500)

        if not registered_students:
            response['success'] = False
            response['message'] = f'No student is registered for {course_code}'
            return response, 404

        try:
            department = Department.query.filter_by(code=department_code).first()
            students_by_dept = registered_students.filter_by(department=department).all()
        except Exception:
            raise AppException('Internal Server Error', 500)

        if not students_by_dept:
            response['success'] = False
            response['message'] = f'No student from {department_code.upper()} is registered for {course_code}'
            return response, 404

        response['success'] = True
        response['message'] = 'Students fetched successfully'
        response['data'] = [{
            'id': id + 1,
            'reg_no': student.reg_no,
            'name': f'{student.firstname} {student.lastname}',
            'template': student.fingerprint_template
        } for id, student in enumerate(students_by_dept)]
        return response, 200

    @staticmethod
    def take_exam_attendance(reg_no, course_code):
        response = {}
        try:
            student = Student.query.filter_by(reg_no=reg_no).first()
            course = Course.query.filter_by(code=course_code).first()
        except Exception:
            raise AppException('Internal Server Error', 500)

        if not student:
            response['success'] = False
            response['message'] = 'Student not found'
            return response, 404

        if not course:
            response['success'] = False
            response['message'] = 'Course not found'
            return response, 404

        if not student.is_registered(course):
            response['success'] = False
            response['message'] = 'Student is not registered for this course'
            return response, 403

        if student.exam_attendance_taken(course):
            response['success'] = False
            response['message'] = 'Student has already taken exam attendance for this course'
            return response, 403

        try:
            student.take_exam_attendance(course)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise AppException('Internal Server Error', 500)

        response['success'] = True
        response['message'] = 'Attendance taken'
        return response, 200

    @staticmethod
    def take_lecture_attendance(reg_no, course_code, lecturer_id):
        response = {}
        try:
            student = Student.query.filter_by(reg_no=reg_no).first()
            course = Course.query.filter_by(code=course_code).first()
            lecturer = Lecturer.query.filter_by(id=lecturer_id).first()
        except Exception:
            raise AppException('Internal Server Error', 500)

        if not student:
            response['success'] = False
            response['message'] = 'Student not found'
            return response, 404

        if not course:
            response['success'] = False
            response['message'] = 'Course not found'
            return response, 404

        if not lecturer:
            response['success'] = False
            response['message'] = 'Lecturer not found'
            return response, 404

        if not student.is_registered(course):
            response['success'] = False
            response['message'] = 'Student is not registered for this course'
            return response, 403

        try:
            student.attend_lecture(course, lecturer)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise AppException('Internal Server Error', 500)

        response['success'] = True
        response['message'] = 'Attendance taken'
        return response, 200

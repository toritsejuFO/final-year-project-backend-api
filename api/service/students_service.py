from api import db
from api.model import Student, Department, Level, Course


class StudentService():
    @staticmethod
    def get_all_students():
        response = {}
        try:
            students = Student.query.all()
        except:
            response['success'] = False
            response['message'] = 'Internal Server Error'
            return response, 500

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
        except:
            response['success'] = False
            response['message'] = 'Internal Server Error'
            return response, 500

        response['success'] = True
        response['message'] = 'New student successfully registered'
        return response, 201

    @staticmethod
    def get_me(reg_no):
        response = {}
        try:
            student = Student.query.filter_by(reg_no=reg_no).first()
        except:
            response['success'] = False
            response['message'] = 'Internal Server Error'
            return response, 500

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
        except:
            response['success'] = False
            response['message'] = 'Internal Server Error'
            return response, 500

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
        except:
            response['success'] = False
            response['message'] = 'Internal Server Error'
            return response, 500

        response['success'] = True
        response['message'] = 'Details updated successfully'
        return response, 200

    @staticmethod
    def get_me_courses(reg_no, semester):
        response = {}
        try:
            student = Student.query.filter_by(reg_no=reg_no).first()
        except:
            response['success'] = False
            response['message'] = 'Internal Server Error'
            return response, 500

        if not student:
            response['success'] = False
            response['message'] = 'Student Not Found'
            return response, 404

        # Select courses based on student's level and current semester
        courses = list(filter(
            lambda c: c.semester.semester == semester and c.level.level == student.level.level,
            student.department.courses))

        response['success'] = True
        response['data'] = [course.to_dict for course in courses]
        return response, 200

    @staticmethod
    def register_courses(reg_no, data):
        response = {}
        try:
            student = Student.query.filter_by(reg_no=reg_no).first()
        except:
            response['success'] = False
            response['message'] = 'Internal Server Error'
            return response, 500

        if not student:
            response['success'] = False
            response['message'] = 'Student Not Found'
            return response, 404

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
        except Exception as e:
            print(repr(e))
            response['success'] = False
            response['message'] = 'Internal Server Error'
            return response, 500

        response['success'] = True
        response['message'] = 'Courses registered successfully'
        return response, 200

    @staticmethod
    def get_registered_courses(reg_no):
        response = {}
        try:
            student = Student.query.filter_by(reg_no=reg_no).first()
        except Exception:
            response['success'] = False
            response['message'] = 'Internal Server Error'
            return response, 500

        if not student:
            response['success'] = False
            response['message'] = 'Student Not Found'
            return response, 404

        response['success'] = True
        response['data'] = [course.to_dict for course in student.registered_courses.all()]
        return response, 200

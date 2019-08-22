from api import db
from api.model import HOD, Lecturer, Course

class HODService:
    @staticmethod
    def create_hod(data):
        response = {}
        name = data['name']
        email = data['email']
        department_code = data['department']
        password = data['password']

        try:
            hod = HOD(
                name=name,
                email=email,
                department_code=department_code,
                password=password
            )
            hod.save()
        except Exception:
            response['success'] = False
            response['message'] = "Internal Server Error"
            return response, 500

        response['success'] = True
        response['message'] = 'New HOD registered successsfully'
        return response, 201

    @staticmethod
    def get_me(email):
        response = {}
        try:
            hod = HOD.query.filter_by(email=email).first()
        except Exception:
            response['success'] = False
            response['message'] = 'Internal Server Error'
            return response, 500

        if not hod:
            response['success'] = False
            response['message'] = 'HOD Not Found'
            return response, 404

        response['success'] = True
        response['data'] = hod.to_dict
        return response, 200

    @staticmethod
    def edit_me(email, data):
        response = {}
        try:
            hod = HOD.query.filter_by(email=email).first()
        except Exception:
            response['success'] = False
            response['message'] = 'Internal Server Error'
            return response, 500

        if not hod:
            response['success'] = False
            response['message'] = 'HOD not found'
            return response, 404

        try:
            hod.name = data['name']
            if data['password'] != '':
                hod.password = data['password']
            hod.save()
        except Exception:
            response['success'] = False
            response['message'] = 'Internal Server Error'
            return response, 500

        response['success'] = True
        response['message'] = 'Details updated successfully'
        return response, 200

    @staticmethod
    def get_lecturers(email):
        response = {}
        try:
            hod = HOD.query.filter_by(email=email).first()
        except Exception:
            response['success'] = False
            response['message'] = 'Internal Server Error'
            return response, 500

        if not hod:
            response['success'] = False
            response['message'] = 'HOD not found'
            return response, 404

        response['success'] = True
        response['data'] = [lecturer.to_dict for lecturer in hod.department.lecturers]
        return response, 200

    @staticmethod
    def get_courses(email, semester):
        response = {}
        try:
            hod = HOD.query.filter_by(email=email).first()
        except Exception:
            response['success'] = False
            response['message'] = 'Internal Server Error'
            return response, 500

        if not hod:
            response['success'] = False
            response['message'] = 'HOD not found'
            return response, 404

        # Filter courses in department by semester
        courses = list(filter(lambda c: c.semester.semester == semester, hod.department.courses))

        response['success'] = True
        response['data'] = [course.to_dict for course in courses]
        return response, 200
    @staticmethod
    def assign_courses(email, data):
        response = {}
        try:
            hod = HOD.query.filter_by(email=email).first()
        except Exception:
            response['success'] = False
            response['message'] = 'Internal Server Error'
            return response, 500

        if not hod:
            response['success'] = False
            response['message'] = 'HOD not found'
            return response, 404

        try:
            for datum in data:
                lecturer_email = datum['email']
                course_codes = datum['courses']
                lecturer = Lecturer.query.filter_by(email=lecturer_email).first()
                for course_code in course_codes:
                    course = Course.query.filter_by(code=course_code).first()
                    lecturer.assign_course(course)
                db.session.commit()
        except Exception:
            response['success'] = False
            response['message'] = 'Internal Server Error'
            return response, 500

        response['success'] = True
        response['message'] = 'Courses assigned successfully'
        return response, 200

    @staticmethod
    def get_assigned(email, semester):
        response = {}
        try:
            hod = HOD.query.filter_by(email=email).first()
        except Exception:
            response['success'] = False
            response['message'] = 'Internal Server Error'
            return response, 500

        if not hod:
            response['success'] = False
            response['message'] = 'HOD not found'
            return response, 404

        # Filter courses in department by semester
        courses = list(filter(lambda c: c.semester.semester == semester, hod.department.courses))
        assigned_courses = [{
            'course': course.to_dict,
            'lecturers': [lecturer.to_dict for lecturer in course.lecturers_assigned.all()]
        } for course in courses]

        response['success'] = False
        response['data'] = assigned_courses
        return response, 200

from api import db, AppException
from api.model import HOD, Lecturer, Course, Department

class HODService:
    @staticmethod
    def create_hod(data):
        response = {}
        name = data['name']
        email = data['email']
        department_code = data['department']
        password = data['password']

        try:
            dept = Department.query.filter_by(code=department_code).first()
            if dept and HOD.query.filter_by(department=dept).count() > 0:
                response['success'] = False
                response['message'] = f'HOD for {dept.name} has already been signed up'
                return response, 423
        except Exception:
            raise AppException('Internal Server Error', 500)

        try:
            hod = HOD(
                name=name,
                email=email,
                department_code=department_code,
                password=password
            )
            hod.save()
            db.session.refresh(hod)
        except Exception:
            db.session.rollback()
            raise AppException('Internal Server Error', 500)

        response['success'] = True
        response['message'] = 'New HOD registered successsfully'
        return response, 201

    @staticmethod
    def get_me(email):
        response = {}
        try:
            hod = HOD.query.filter_by(email=email).first()
        except Exception:
            raise AppException('Internal Server Error', 500)

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
            raise AppException('Internal Server Error', 500)

        if not hod:
            response['success'] = False
            response['message'] = 'HOD not found'
            return response, 404

        try:
            hod.name = data['name']
            if data['password'] != '':
                hod.password = data['password']
            hod.save()
            db.session.refresh(hod)
        except Exception:
            db.session.rollback()
            raise AppException('Internal Server Error', 500)

        response['success'] = True
        response['message'] = 'Details updated successfully'
        return response, 200

    @staticmethod
    def get_lecturers(email):
        response = {}
        try:
            hod = HOD.query.filter_by(email=email).first()
        except Exception:
            raise AppException('Internal Server Error', 500)

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
            raise AppException('Internal Server Error', 500)

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
            raise AppException('Internal Server Error', 500)

        if not hod:
            response['success'] = False
            response['message'] = 'HOD not found'
            return response, 404

        # if hod.has_assigned_courses:
        #     response['success'] = False
        #     response['message'] = 'Unable to assign courses more than once. Contact Admin'
        #     return response, 423

        try:
            for datum in data:
                lecturer_email = datum['email']
                course_codes = datum['courses']
                lecturer = Lecturer.query.filter_by(email=lecturer_email).first()
                for course_code in course_codes:
                    course = Course.query.filter_by(code=course_code).first()
                    lecturer.assign_course(course)
                db.session.commit()
                db.session.refresh(lecturer)
                # hod.has_assigned_courses = True
                # hod.save()
        except Exception:
            db.session.rollback()
            raise AppException('Internal Server Error', 500)

        response['success'] = True
        response['message'] = 'Courses assigned successfully'
        return response, 200

    @staticmethod
    def get_assigned(email, semester):
        response = {}
        try:
            hod = HOD.query.filter_by(email=email).first()
        except Exception:
            raise AppException('Internal Server Error', 500)

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

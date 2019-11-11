from api import db, AppException
from api.model import Lecturer, Course

class LecturerService:
    @staticmethod
    def create_lecturer(data):
        response = {}
        name = data['name']
        email = data['email']
        department_code = data['department']
        password = data['password']

        try:
            lecturer = Lecturer(
                name=name,
                email=email,
                department_code=department_code,
                password=password
            )
            lecturer.save()
            db.session.refresh(lecturer)
        except Exception:
            db.session.rollback()
            raise AppException('Internal Server Error', 500)

        response['success'] = True
        response['message'] = 'New Lecturer registered successsfully'
        return response, 201

    @staticmethod
    def get_me(email):
        response = {}
        try:
            lecturer = Lecturer.query.filter_by(email=email).first()
        except Exception:
            raise AppException('Internal Server Error', 500)

        if not lecturer:
            response['success'] = False
            response['message'] = 'Lecturer Not Found'
            return response, 404

        data = {
            **lecturer.to_dict,
            'assigned_courses': [course.to_dict for course in lecturer.assigned_courses.all()]
        }
        response['success'] = True
        response['data'] = data
        return response, 200

    @staticmethod
    def mark_lecture_attendance(email, course_code):
        response = {}
        try:
            lecturer = Lecturer.query.filter_by(email=email).first()
            course = Course.query.filter_by(code=course_code).first()
        except Exception:
            raise AppException('Internal Server Error', 500)

        if not lecturer:
            response['success'] = False
            response['message'] = 'Lecturer Not Found'
            return response, 404

        if not course:
            response['success'] = False
            response['message'] = 'Course Not Found'
            return response, 404

        if not lecturer.is_assigned(course):
            response['success'] = False
            response['message'] = 'Lecturer is not assigned to this course'
            return response, 403

        try:
            lecturer.attend_lecture(course)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise AppException('Internal Server Error', 500)

        response['success'] = True
        response['message'] = 'Attendance taken for lecturer'
        return response, 200

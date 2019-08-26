import os

from flask_restplus import Resource, Namespace

from api.service import CourseService

course_api = Namespace(
    'courses', description='API endpoints for managing courses resourse')

current_api = Namespace(
    'current', description='API endpoints for getting current session and semester')


@course_api.route('')
class CourseList(Resource):
    @course_api.doc('Get All Courses')
    def get(self):
        response, code = CourseService.get_all_courses()
        return response, code


@course_api.route('/<string:department>/<string:level>')
class Course(Resource):
    @course_api.doc('Get Courses via Department & Level')
    def get(self, department, level):
        response, code = CourseService.get_courses_by_dept_level(
            department=department, level=level)
        return response, code


@current_api.route('/semester')
class CurrentSemester(Resource):
    @current_api.doc('Get current semester')
    def get(self):
        response = {
            'success': True,
            'data': os.environ.get('CURRENT_SEMESTER')
        }
        return response, 200


@current_api.route('/session')
class CurrentSession(Resource):
    @current_api.doc('Get current session')
    def get(self):
        response = {
            'success': True,
            'data': os.environ.get('CURRENT_SESSION')
        }
        return response, 200

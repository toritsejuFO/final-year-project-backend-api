import os

from flask_restplus import Resource, Namespace

from api.service import CourseService

course_api = Namespace(
    'courses', description='API endpoints for managing courses resourse')

current_api = Namespace(
    'current', description='API endpoints for getting current session and semester')


@course_api.route('/all')
class CourseList(Resource):
    @course_api.doc('Get All Courses')
    def get(self):
        ''' Get all courses '''
        response, code = CourseService.get_all_courses()
        return response, code


@course_api.route('/<string:department>/<string:level>')
@course_api.route('/<string:department>/<string:level>/<int:minimal>')
class Course(Resource):
    @course_api.doc('Get Courses via Department & Level')
    def get(self, department, level, minimal=0):
        ''' Get a course by department and level '''
        print(minimal)
        response, code = CourseService.get_courses_by_dept_level(
            department=department, level=level, minimal=minimal)
        return response, code


@current_api.route('/semester')
class CurrentSemester(Resource):
    @current_api.doc('Get current semester')
    def get(self):
        ''' Get the current semester '''
        response = {
            'success': True,
            'data': os.environ.get('CURRENT_SEMESTER') or 'unavailable'
        }
        return response, 200


@current_api.route('/session')
class CurrentSession(Resource):
    @current_api.doc('Get current session')
    def get(self):
        ''' Get the current session '''
        response = {
            'success': True,
            'data': os.environ.get('CURRENT_SESSION') or 'unavailable'
        }
        return response, 200

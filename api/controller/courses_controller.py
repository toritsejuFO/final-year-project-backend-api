from flask_restplus import Resource, Namespace

from api.service import CourseService

course_api = Namespace('courses', description='API endpoints for managing courses resourse')

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
        response, code = CourseService.get_courses_by_dept_level(department=department, level=level)
        return response, code

from flask_restplus import Resource, Namespace

from api.service import CourseService

course_api = Namespace('courses', description='API endpoints for manaigin courses resourse')

@course_api.route('')
class CourseList(Resource):
    @course_api.doc('Get All Courses')
    def get(self):
        response, code = CourseService.get_all_courses()
        return response, code

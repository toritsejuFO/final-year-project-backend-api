from flask_restplus import Resource, Namespace

from api.service import SchoolService

school_api = Namespace('schools', description='API endpoints for managing schools resource')


@school_api.route('/all')
class SchoolList(Resource):
    @school_api.doc('Get All Schools')
    def get(self):
        response, code = SchoolService.get_all()
        return response, code

@school_api.route('/<string:school>/departments')
class DepartmentList(Resource):
    @school_api.doc('Get All departments in a school')
    def get(self, school):
        response, code = SchoolService.get_departments(school_code=school)
        return response, code

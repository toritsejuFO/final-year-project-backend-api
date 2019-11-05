from flask_restplus import Resource, Namespace

from api.service import DepartmentService

dept_api = Namespace('departments', description='API endpoints for managing departments resource')


@dept_api.route('/all')
class DepartmentList(Resource):
    @dept_api.doc('Get All Departments')
    def get(self):
        ''' Get all departments '''
        response, code = DepartmentService.get_all()
        return response, code

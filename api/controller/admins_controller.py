from flask_restplus import Resource, Namespace

from api.service import AdminsService

admin_api = Namespace('admins', description='Endpoints to feed admin data')


@admin_api.route('/exam/oar/<string:session>/<string:semester>/<string:course>/<string:department>')
class ExamOAR(Resource):
    def get(self, session, semester, course, department):
        ''' Get all students froma a department who attended exam for a course '''
        response, code = AdminsService.get_oar(
            session=session, semester=semester, course_code=course, department_code=department)
        return response, code

from flask import request
from flask_restplus import Resource, Namespace, fields
from marshmallow import ValidationError

from api.service import AdminsService, admin_login_required
from api.schema import NewAdminSchema

admin_api = Namespace('admins', description='Endpoints to manage admin operations')

admin_reg = admin_api.model('Admin Registration', {
    'name': fields.String(required=True, description='Admin\'s name'),
    'email': fields.String(required=True, description='Admin\'s email'),
    'password': fields.String(required=True, description='Admin\'s password')
})


@admin_api.route('/signup')
class Signup(Resource):
    @admin_api.doc('Register a new Admin')
    @admin_api.response(201, 'New Admin successfully registered')
    @admin_api.expect(admin_reg)
    def post(self):
        ''' Signup a new admin '''
        data = request.json
        payload = admin_api.payload or data
        schema = NewAdminSchema()

        try:
            new_payload = schema.load(payload)._asdict()
        except ValidationError as e:
            response = {
                'success': False,
                'error': e.messages
            }
            return response, 400
        response, code = AdminsService.create(data=new_payload)
        return response, code

@admin_api.route('/exam/oar/<string:session>/<string:semester>/<string:course>/<string:department>')
class ExamOAR(Resource):
    @admin_login_required
    @admin_api.doc('Get data for exam OAR sheet', security='apiKey')
    def get(self, session, semester, course, department, decoded_payload):
        ''' Get all students froma a department who attended exam for a course '''
        email = decoded_payload.get('email')
        response, code = AdminsService.get_oar(
            session=session, semester=semester, course_code=course, department_code=department, email=email)
        return response, code

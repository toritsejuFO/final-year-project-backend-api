from flask import request
from flask_restplus import Resource, Namespace, fields
from marshmallow import ValidationError

from api.service import LecturerService, lecturer_login_required
from api.schema import NewLecturerSchema

lecturer_api = Namespace(
    'lecturers', description='API endpoints for managing Lecturer Resource')

lecturer_reg = lecturer_api.model('Lecturer Registration', {
    'name': fields.String(required=True, description='Lecturer\'s name'),
    'email': fields.String(required=True, description='Lecturer\'s email'),
    'department': fields.String(required=True, description='Lecturer\'s department'),
    'password': fields.String(required=True, description='Lecturer\'s password'),
})


@lecturer_api.route('/signup')
class LecturerSignup(Resource):
    @lecturer_api.doc('Register a new lecturer')
    @lecturer_api.response(201, 'New lecturer successfully registered')
    @lecturer_api.expect(lecturer_reg)
    def post(self):
        data = request.json
        payload = lecturer_api.payload or data
        schema = NewLecturerSchema()

        try:
            new_payload = schema.load(payload)._asdict()
        except ValidationError as e:
            response = {
                'success': False,
                'error': e.messages
            }
            return response, 400
        response, code = LecturerService.create_lecturer(data=new_payload)
        return response, code

@lecturer_api.route('/me')
class Me(Resource):
    @lecturer_login_required
    @lecturer_api.doc('View Lecturer details', security='apiKey')
    def get(self, decoded_payload):
        email = decoded_payload.get('email')
        response, code = LecturerService.get_me(email=email)
        return response, code

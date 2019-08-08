from flask import request
from flask_restplus import Resource, Namespace, fields
from marshmallow import ValidationError

from api.service import AuthService
from api.schema import StudentLoginSchema

student_auth_api = Namespace(
    'students', description='API endpoints for authenticating Students')

student_login = student_auth_api.model('Student login', {
    'reg_no': fields.String(required=True, description='Student\'s reg number'),
    'password': fields.String(required=True, description='Student\'s password'),
})


@student_auth_api.route('/signin')
class StudentLogin(Resource):
    @student_auth_api.doc('Login a student')
    @student_auth_api.response(200, 'Logged in successfully')
    @student_auth_api.expect(student_login)
    def post(self):
        data = request.json
        payload = student_auth_api.payload or data
        schema = StudentLoginSchema(strict=True)

        try:
            new_payload = schema.load(payload).data._asdict()
        except ValidationError as e:
            response = {
                'status': False,
                'message': e.messages
            }
            return response, 400

        response, code = AuthService.login_student(data=new_payload)
        return response, code

@student_auth_api.route('/signout')
class StudentLogout(Resource):
    @student_auth_api.doc('Log out a student', security='apiKey')
    @student_auth_api.response(200, 'Logged in successfully')
    def get(self):
        auth_token = request.headers.get('x-auth-token')
        if not auth_token or auth_token is None:
            response = {
                'status': False,
                'message': 'Please provide a token'
            }
            return response, 401
        response, code = AuthService.logout_student(auth_token=auth_token)
        return response, code

from flask import request
from flask_restplus import Resource, Namespace, fields
from marshmallow import ValidationError

from api.service import AuthService
from api.schema import StudentLoginSchema, LecturerLoginSchema, HODLoginSchema, AdminLoginSchema

student_auth_api = Namespace(
    'students', description='API endpoints for authenticating Students')

student_login = student_auth_api.model('Student login', {
    'reg_no': fields.String(required=True, description='Student\'s reg number'),
    'password': fields.String(required=True, description='Student\'s password'),
})

lecturer_auth_api = Namespace(
    'lecturers', description='API endpoints for authenticating Lecturers')

lecturer_login = lecturer_auth_api.model('Lecturer login', {
    'email': fields.String(required=True, description='Lecturer\'s email'),
    'password': fields.String(required=True, description='Lecturer\'s password'),
})

hod_auth_api = Namespace(
    'hods', description='API endpoints for authenticating HODs')

hod_login = hod_auth_api.model('HOD login', {
    'email': fields.String(required=True, description='HOD\'s email'),
    'password': fields.String(required=True, description='HOD\'s password'),
})

admin_auth_api = Namespace(
    'admins', description='API endpoints for authenticating Admins')

admin_login = admin_auth_api.model('Admin login', {
    'email': fields.String(required=True, description='Admin\'s email'),
    'password': fields.String(required=True, description='Admin\'s password'),
})

auth_verification_api = Namespace('auth', description='API endpoint for verifying auth token')


@student_auth_api.route('/signin')
class StudentLogin(Resource):
    @student_auth_api.doc('Login a student')
    @student_auth_api.response(200, 'Logged in successfully')
    @student_auth_api.expect(student_login)
    def post(self):
        ''' Authenticate a student '''
        data = request.json
        payload = student_auth_api.payload or data
        schema = StudentLoginSchema()

        try:
            new_payload = schema.load(payload)._asdict()
        except ValidationError as e:
            response = {
                'success': False,
                'error': e.messages
            }
            return response, 400

        response, code = AuthService.login_student(data=new_payload)
        return response, code


@student_auth_api.route('/signout')
class StudentLogout(Resource):
    @student_auth_api.doc('Log out a student', security='apiKey')
    @student_auth_api.response(200, 'Logged out successfully')
    def get(self):
        ''' Logout a student '''
        auth_token = request.headers.get('x-auth-token')
        if not auth_token or auth_token is None:
            response = {
                'success': False,
                'message': 'Please provide a token'
            }
            return response, 401
        response, code = AuthService.logout_student(auth_token=auth_token)
        return response, code


@lecturer_auth_api.route('/signin')
class LecturerLogin(Resource):
    @lecturer_auth_api.doc('Login a lecturer')
    @lecturer_auth_api.response(200, 'Logged in successfully')
    @lecturer_auth_api.expect(lecturer_login)
    def post(self):
        ''' Authenticate a lecturer '''
        data = request.json
        payload = lecturer_auth_api.payload or data
        schema = LecturerLoginSchema()

        try:
            new_payload = schema.load(payload)._asdict()
        except ValidationError as e:
            response = {
                'success': False,
                'error': e.messages
            }
            return response, 400

        response, code = AuthService.login_lecturer(data=new_payload)
        return response, code


@lecturer_auth_api.route('/signout')
class LecturerLogout(Resource):
    @lecturer_auth_api.doc('Log out a lecturer', security='apiKey')
    @lecturer_auth_api.response(200, 'Logged out successfully')
    def get(self):
        ''' Logout a lecturer '''
        auth_token = request.headers.get('x-auth-token')
        if not auth_token or auth_token is None:
            response = {
                'success': False,
                'message': 'Please provide a token'
            }
            return response, 401
        response, code = AuthService.logout_lecturer(auth_token=auth_token)
        return response, code


@hod_auth_api.route('/signin')
class HODLogin(Resource):
    @hod_auth_api.doc('Login a HOD')
    @hod_auth_api.response(200, 'Logged in successfully')
    @hod_auth_api.expect(hod_login)
    def post(self):
        ''' Authenticate an HOD '''
        data = request.json
        payload = hod_auth_api.payload or data
        schema = HODLoginSchema()

        try:
            new_payload = schema.load(payload)._asdict()
        except ValidationError as e:
            response = {
                'success': False,
                'error': e.messages
            }
            return response, 400

        response, code = AuthService.login_hod(data=new_payload)
        return response, code


@hod_auth_api.route('/signout')
class HODLogout(Resource):
    @hod_auth_api.doc('Log out an HOD', security='apiKey')
    @hod_auth_api.response(200, 'Logged out successfully')
    def get(self):
        ''' Logout an HOD '''
        auth_token = request.headers.get('x-auth-token')
        if not auth_token or auth_token is None:
            response = {
                'success': False,
                'message': 'Please provide a token'
            }
            return response, 401
        response, code = AuthService.logout_hod(auth_token=auth_token)
        return response, code

@admin_auth_api.route('/signin')
class AdminLogin(Resource):
    @admin_auth_api.doc('Login a admin')
    @admin_auth_api.response(200, 'Logged in successfully')
    @admin_auth_api.expect(admin_login)
    def post(self):
        ''' Authenticate an admin '''
        data = request.json
        payload = admin_auth_api.payload or data
        schema = AdminLoginSchema()

        try:
            new_payload = schema.load(payload)._asdict()
        except ValidationError as e:
            response = {
                'success': False,
                'error': e.messages
            }
            return response, 400

        response, code = AuthService.login_admin(data=new_payload)
        return response, code


@admin_auth_api.route('/signout')
class AdminLogout(Resource):
    @admin_auth_api.doc('Log out an admin', security='apiKey')
    @admin_auth_api.response(200, 'Logged out successfully')
    def get(self):
        ''' Logout an admin '''
        auth_token = request.headers.get('x-auth-token')
        if not auth_token or auth_token is None:
            response = {
                'success': False,
                'message': 'Please provide a token'
            }
            return response, 401
        response, code = AuthService.logout_admin(auth_token=auth_token)
        return response, code

@auth_verification_api.route('/verify')
class AuthTokenVerification(Resource):
    @auth_verification_api.doc('Verify Auth Token', security='apiKey')
    @auth_verification_api.response(200, 'Valid Token')
    @auth_verification_api.response(401, 'Token Not Provided')
    @auth_verification_api.response(401, 'Invalid Token')
    @auth_verification_api.response(401, 'Expired Token')
    @auth_verification_api.response(403, 'Revoked Token')
    def get(self):
        ''' Verify a token's validity '''
        auth_token = request.headers.get('x-auth-token')
        if not auth_token or auth_token is None:
            response = {
                'success': False,
                'message': 'Please provide a token'
            }
            return response, 401

        response, code = AuthService.verify(auth_token=auth_token)
        return response, code

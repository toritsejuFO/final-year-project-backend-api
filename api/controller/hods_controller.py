from flask import request
from flask_restplus import Resource, Namespace, fields
from marshmallow import ValidationError

from api.service import HODService, hod_login_required
from api.schema import NewHODSchema, EditHODSchema

hod_api = Namespace(
    'hods', description='API endpoints for managing HOD Resource')

hod_reg = hod_api.model('HOD Registration', {
    'name': fields.String(required=True, description='HOD\'s name'),
    'email': fields.String(required=True, description='HOD\'s email'),
    'department': fields.String(required=True, description='HOD\'s department'),
    'password': fields.String(required=True, description='HOD\'s password'),
})

edit_me = hod_api.model('HOD Update', {
    'name': fields.String(required=True, description='HOD\'s name'),
    'password': fields.String(required=True, description='HOD\'s password'),
})

assign_course_object = hod_api.model('Assign Course Object', {
    'email': fields.String(required=True, description='Lecturer\'s email'),
    'courses': fields.List(fields.String, required=True, description='List of courses to be assigned to lecturer')
})

assign_course_list = hod_api.model('Assign Courses List', {
    'payload': fields.Nested(assign_course_object, required=True, description='List of course objects to be assigned to a lecturer', as_list=True)
})


@hod_api.route('/signup')
class HODSignup(Resource):
    @hod_api.doc('Register a new hod')
    @hod_api.response(201, 'New hod successfully registered')
    @hod_api.expect(hod_reg)
    def post(self):
        ''' Signup a new HOD '''
        data = request.json
        payload = hod_api.payload or data
        schema = NewHODSchema()

        try:
            new_payload = schema.load(payload)._asdict()
        except ValidationError as e:
            response = {
                'success': False,
                'error': e.messages
            }
            return response, 400
        response, code = HODService.create_hod(data=new_payload)
        return response, code

@hod_api.route('/me')
class Me(Resource):
    @hod_login_required
    @hod_api.doc('View HOD details', security='apiKey')
    def get(self, decoded_payload):
        ''' Get details of logged in HOD '''
        email = decoded_payload.get('email')
        response, code = HODService.get_me(email=email)
        return response, code

@hod_api.route('/me/edit')
class EditMe(Resource):
    @hod_login_required
    @hod_api.doc('Update HOD details', security='apiKey')
    @hod_api.expect(edit_me)
    def post(self, decoded_payload):
        ''' Edit details of logged in HOD '''
        email = decoded_payload.get('email')
        data = request.json
        schema = EditHODSchema()
        payload = hod_api.payload or data

        try:
            new_payload = schema.load(payload)._asdict()
        except ValidationError as e:
            response = {
                'success': False,
                'error': e.messages
            }
            return response, 400

        response, code = HODService.edit_me(email=email, data=new_payload)
        return response, code

@hod_api.route('/lecturers')
class LecturerList(Resource):
    @hod_login_required
    @hod_api.doc('Get All Lecturers in HOD department', security='apiKey')
    def get(self, decoded_payload):
        ''' Get all lecturers in HOD's department '''
        email = decoded_payload.get('email')
        response, code = HODService.get_lecturers(email=email)
        return response, code

@hod_api.route('/courses/<string:semester>')
class CourseList(Resource):
    @hod_login_required
    @hod_api.doc('Get All Courses in HOD department per semester', security='apiKey')
    def get(self, semester, decoded_payload):
        ''' Get all courses in HOD's department filtered by provided semester '''
        email = decoded_payload.get('email')
        response, code = HODService.get_courses(email=email, semester=semester)
        return response, code

@hod_api.route('/assign/lecturers')
class AssignCourses(Resource):
    @hod_login_required
    @hod_api.doc('Assign Courses to Lecturers', security='apiKey')
    @hod_api.expect(assign_course_list)
    def post(self, decoded_payload):
        ''' Assign courses to lecturers '''
        email = decoded_payload.get('email')
        data = request.json.get('payload')
        payload = hod_api.payload.get('payload') or data
        response, code = HODService.assign_courses(email=email, data=payload)
        return response, code

@hod_api.route('/assigned/<string:semester>')
class Assigned(Resource):
    @hod_login_required
    @hod_api.doc('Get All Courses Assigned per semester', security='apiKey')
    def get(self, semester, decoded_payload):
        ''' View courses and assigned lecturers '''
        email = decoded_payload.get('email')
        response, code = HODService.get_assigned(email=email, semester=semester)
        return response, code

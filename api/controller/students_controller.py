from flask import request
from flask_restplus import Resource, Namespace, fields
from marshmallow import ValidationError

from api.service import StudentService, login_required
from api.schema import NewStudentSchema

student_api = Namespace(
    'students', description='API endpoints for managin Student Resource')
student_reg = student_api.model('Student Registration', {
    'firstname': fields.String(required=True, description='Student\'s firstname'),
    'lastname': fields.String(required=True, description='Student\'s lastname'),
    'othername': fields.String(required=True, description='Student\'s othername'),
    'reg_no': fields.String(required=True, description='Student\'s reg number'),
    'email': fields.String(required=True, description='Student\'s email'),
    'password': fields.String(required=True, description='Student\'s password'),
})

student_edit = student_api.model('Student Update', {
    'level': fields.String(required=True, description='Student\'s level'),
    'school': fields.String(required=True, description='Student\'s school'),
    'department': fields.String(required=True, description='Student\'s department'),
})


@student_api.route('')
class StudentList(Resource):
    @student_api.doc('Get all students')
    def get(self):
        response, code = StudentService.get_all_students()
        return response, code


@student_api.route('/signup')
class students(Resource):
    @student_api.doc('Register a new student')
    @student_api.response(201, 'New student successfully registered')
    @student_api.expect(student_reg)
    def post(self):
        data = request.json
        payload = student_api.payload or data
        schema = NewStudentSchema(strict=True)

        try:
            new_payload = schema.load(payload).data._asdict()
        except ValidationError as e:
            response = {
                'status': False,
                'message': e.messages
            }
            return response, 400
        response, code = StudentService.create_student(data=new_payload)
        return response, code


@student_api.route('/me')
class Student(Resource):
    @login_required
    @student_api.doc('View student details')
    def get(self, payload):
        reg_no = payload['reg_no']
        response, code = StudentService.get_me(reg_no=reg_no)
        return response, code

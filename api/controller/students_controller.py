from flask import request
from flask_restplus import Resource, Namespace, fields

from api.service import StudentService

student_api = Namespace('students', description='API endpoints for managin Student Resource')
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



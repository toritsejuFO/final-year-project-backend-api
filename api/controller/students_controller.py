from flask import request
from flask_restplus import Resource, Namespace, fields
from marshmallow import ValidationError

from api.service import StudentService, student_login_required
from api.schema import NewStudentSchema, EditMeSchema

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

edit_me = student_api.model('Student Update', {
    'level': fields.String(required=True, description='Student\'s level'),
    'department': fields.String(required=True, description='Student\'s department'),
})

courses_registration = student_api.model('Courses Registration', {
    'courses': fields.List(fields.String, required=True, description='A Course')
})


@student_api.route('')
class StudentList(Resource):
    @student_api.doc('Get all students')
    def get(self):
        ''' Get all students '''
        response, code = StudentService.get_all_students()
        return response, code


@student_api.route('/signup')
class Signup(Resource):
    @student_api.doc('Register a new student')
    @student_api.response(201, 'New student successfully registered')
    @student_api.expect(student_reg)
    def post(self):
        ''' Signup a new student '''
        data = request.json
        payload = student_api.payload or data
        schema = NewStudentSchema()

        try:
            new_payload = schema.load(payload)._asdict()
        except ValidationError as e:
            response = {
                'success': False,
                'error': e.messages
            }
            return response, 400
        response, code = StudentService.create_student(data=new_payload)
        return response, code


@student_api.route('/me')
class Me(Resource):
    @student_login_required
    @student_api.doc('View student details', security='apiKey')
    def get(self, decoded_payload):
        ''' Get details of logged in student '''
        reg_no = decoded_payload.get('reg_no')
        response, code = StudentService.get_me(reg_no=reg_no)
        return response, code


@student_api.route('/me/edit')
class EditMe(Resource):
    @student_login_required
    @student_api.expect(edit_me)
    @student_api.doc('Edit/Update student details', security='apiKey')
    def post(self, decoded_payload):
        ''' Update details of logged in student '''
        reg_no = decoded_payload.get('reg_no')
        data = request.json
        payload = student_api.payload or data
        schema = EditMeSchema()

        try:
            new_payload = schema.load(payload)._asdict()
        except ValidationError as e:
            response = {
                'success': False,
                'error': e.messages
            }
            return response, 400
        response, code = StudentService.edit_me(
            reg_no=reg_no, data=new_payload)
        return response, code


@student_api.route('/me/courses/<string:semester>')
class StudentCourseList(Resource):
    @student_login_required
    @student_api.doc('View student courses per semester', security='apiKey')
    def get(self, semester, decoded_payload):
        ''' View student courses of specified semester '''
        reg_no = decoded_payload.get('reg_no')
        response, code = StudentService.get_me_courses(
            reg_no=reg_no, semester=semester)
        return response, code


@student_api.route('/me/register/courses')
class RegisterCourses(Resource):
    @student_login_required
    @student_api.expect(courses_registration)
    @student_api.doc('Register Student Courses', security='apiKey')
    def post(self, decoded_payload):
        ''' Register courses for logged in student '''
        reg_no = decoded_payload.get('reg_no')
        data = request.json
        payload = student_api.payload or data
        response, code = StudentService.register_courses(
            reg_no=reg_no, data=payload)
        return response, code


@student_api.route('/me/registered/courses')
class RegisteredCourseList(Resource):
    @student_login_required
    @student_api.doc('View Student\'s Registered Courses', security='apiKey')
    def get(self, decoded_payload):
        ''' View registered courses of logged in student '''
        reg_no = decoded_payload.get('reg_no')
        response, code = StudentService.get_registered_courses(reg_no=reg_no)
        return response, code


@student_api.route('/me/register/fingerprint')
class RegisterFingerprintTemplate(Resource):
    @student_login_required
    @student_api.doc('Register Student\'s fingerprint', security='apiKey')
    def post(self, decoded_payload):
        ''' HW: Register fingerprint for registered student '''
        reg_no = decoded_payload.get('reg_no')
        data = request.json
        payload = student_api.payload or data
        response, code = StudentService.register_fingerprint(
            reg_no=reg_no, data=payload)
        return response, code


@student_api.route('/<string:reg_no>/<string:course>')
class VerifyRegisteredCourse(Resource):
    def get(self, reg_no, course):
        ''' Verify if student has registered a course '''
        response, code = StudentService.verify_registered_courses(
            reg_no=reg_no, course_code=course)
        return response, code

@student_api.route('/registered/<string:course>/<string:department>')
class RegisteredCourseStudentList(Resource):
    def get(self, course, department):
        ''' HW: Get all the students from a department that have registered for a course '''
        response, code = StudentService.get_registered_students(
            course_code=course, department_code=department)
        return response, code

@student_api.route('/<string:reg_no>/exam/attendance/<string:course>')
class ExamAttendance(Resource):
    def get(self, reg_no, course):
        ''' Take course exam attendance for student with provided reg number '''
        response, code = StudentService.take_exam_attendance(reg_no=reg_no, course_code=course)
        return response, code

@student_api.route('/<string:reg_no>/lecture/attendance/<string:course>/<string:lecturer>')
class LectureAttendance(Resource):
    def get(self, reg_no, course, lecturer):
        ''' Take course lecture attendance for student with provided reg number '''
        response, code = StudentService.take_lecture_attendance(
            reg_no=reg_no, course_code=course, lecturer_id=lecturer)
        return response, code

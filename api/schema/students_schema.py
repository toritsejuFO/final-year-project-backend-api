from collections import namedtuple

from marshmallow import Schema, fields, post_load, validates, ValidationError

from api.model import Student, Department

NewStudent = namedtuple('NewStudent', [
    'firstname',
    'lastname',
    'othername',
    'reg_no',
    'email',
    'password'
])

EditMe = namedtuple('EditMe', [
    'level',
    'department',
])

class EditMeSchema(Schema):
    level = fields.String(required=True, error_messages={'required': 'level is required'})
    department = fields.String(required=True, error_messages={'required': 'department is required'})

    @post_load
    def edit_me(self, data):
        return EditMe(**data)

    @validates('level')
    def validate_level(self, value):
        levels = ['100', '200', '300', '400', '500']
        if not value:
            raise ValidationError('Level cannot be empty')
        if value not in levels:
            raise ValidationError(f'Invalid level. Must be in {levels}')

    @validates('department')
    def validate_department(self, value):
        if not value:
            raise ValidationError('Department cannot be empty')
        try:
            dept = Department.query.filter_by(code=value.upper()).first()
        except:
            raise ValidationError('Internal Server Error')
        if not dept:
            raise ValidationError('This department does not exist currently')


class NewStudentSchema(Schema):
    firstname = fields.String(required=True, error_messages={'required': 'firstname is required'})
    lastname = fields.String(required=True, error_messages={'required': 'lastname is required'})
    othername = fields.String(required=True, error_messages={'required': 'othername is required'})
    reg_no = fields.String(required=True, error_messages={'required': 'reg_no is required'})
    email = fields.Email(required=True, error_messages={'required': 'email is required'})
    password = fields.String(required=True, error_messages={'required': 'password is required'})

    @post_load
    def new_student(self, data):
        return NewStudent(**data)

    @validates('firstname')
    def validate_firstname(self, value):
        max_len = 50
        if not value:
            raise ValidationError('First name cannot be empty')
        if len(value) > max_len:
            raise ValidationError(f'First Name cannot exceed {max_len} characters')

    @validates('lastname')
    def validate_lastname(self, value):
        max_len = 50
        if not value:
            raise ValidationError('Last name cannot be empty')
        if len(value) > max_len:
            raise ValidationError(f'Last name cannot exceed {max_len} characters')

    @validates('othername')
    def validate_othername(self, value):
        max_len = 50
        if not value:
            raise ValidationError('Other name cannot be empty')
        if len(value) > max_len:
            raise ValidationError(f'Other name cannot exceed {max_len} characters')

    @validates('reg_no')
    def validate_reg_no(self, value):
        max_len = 11
        student = Student.query.filter_by(reg_no=value).first()
        if not value:
            raise ValidationError('Reg number cannot be empty')
        if len(value) > max_len or len(value) < max_len:
            raise ValidationError(f'Reg number must be exactly {max_len} characters')
        if student:
            raise ValidationError('Student with this reg number already exists')

    @validates('email')
    def validate_email(self, value):
        max_len = 128
        student = Student.query.filter_by(email=value).first()
        if not value:
            raise ValidationError('Email cannot be empty')
        if len(value) > max_len:
            raise ValidationError(f'Email cannot exceed {max_len} characters')
        if student:
            raise ValidationError('Student with this email already exists')

    @validates('password')
    def validate_password(self, value):
        if not value:
            raise ValidationError('Password cannot be empty')

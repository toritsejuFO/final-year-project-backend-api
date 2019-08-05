from collections import namedtuple

from marshmallow import Schema, fields, post_load, validates, ValidationError

from api.model import Student

NewStudent = namedtuple('NewStudent', [
    'firstname',
    'lastname',
    'othername',
    'reg_no',
    'email',
    'password'
])

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
            raise ValidationError('firstname cannnot be empty')
        if len(value) > max_len:
            raise ValidationError(f'firstname cannot exceed {max_len} characters')

    @validates('lastname')
    def validate_lastname(self, value):
        max_len = 50
        if not value:
            raise ValidationError('lastname cannnot be empty')
        if len(value) > max_len:
            raise ValidationError(f'lastname cannot exceed {max_len} characters')

    @validates('othername')
    def validate_othername(self, value):
        max_len = 50
        if not value:
            raise ValidationError('othername cannnot be empty')
        if len(value) > max_len:
            raise ValidationError(f'othername cannot exceed {max_len} characters')
    
    @validates('reg_no')
    def validate_reg_no(self, value):
        max_len = 11
        student = Student.query.filter_by(reg_no=value).first()
        if not value:
            raise ValidationError('reg_no cannnot be empty')
        if len(value) > max_len or len(value) < max_len:
            raise ValidationError(f'reg number must be exactly {max_len} characters')
        if student:
            raise ValidationError('Student with this reg number already exists')

    @validates('email')
    def validate_email(self, value):
        max_len = 128
        student = Student.query.filter_by(email=value).first()
        if not value:
            raise ValidationError('email cannnot be empty')
        if len(value) > max_len:
            raise ValidationError(f'email cannot exceed {max_len} characters')
        if student:
            raise ValidationError('Student with this email already exists')

    @validates('password')
    def validate_password(self, value):
        if not value:
            raise ValidationError('password cannnot be empty')

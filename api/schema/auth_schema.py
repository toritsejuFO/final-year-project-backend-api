from collections import namedtuple

from marshmallow import Schema, fields, post_load, validates, ValidationError

StudentLogin = namedtuple('StudentLogin', [
    'reg_no',
    'password'
])

LecturerLogin = namedtuple('LecturerLogin', [
    'email',
    'password'
])

HODLogin = namedtuple('HODLogin', [
    'email',
    'password'
])


class StudentLoginSchema(Schema):
    reg_no = fields.String(required=True, error_messages={'required': 'reg number is required'})
    password = fields.String(required=True, error_messages={'required': 'password is required'})

    @post_load
    def new_student(self, data):
        return StudentLogin(**data)

    @validates('reg_no')
    def validate_reg_no(self, value):
        if not value:
            raise ValidationError('reg number cannot be empty')

    @validates('password')
    def validate_password(self, value):
        if not value:
            raise ValidationError('password cannot be empty')


class LecturerLoginSchema(Schema):
    email = fields.String(required=True, error_messages={'required': 'email is required'})
    password = fields.String(required=True, error_messages={'required': 'password is required'})

    @post_load
    def new_lecturer(self, data):
        return LecturerLogin(**data)

    @validates('email')
    def validate_email(self, value):
        if not value:
            raise ValidationError('email cannot be empty')

    @validates('password')
    def validate_password(self, value):
        if not value:
            raise ValidationError('password cannot be empty')


class HODLoginSchema(Schema):
    email = fields.String(required=True, error_messages={'required': 'email is required'})
    password = fields.String(required=True, error_messages={'required': 'password is required'})

    @post_load
    def new_hod(self, data):
        return HODLogin(**data)

    @validates('email')
    def validate_email(self, value):
        if not value:
            raise ValidationError('email cannot be empty')

    @validates('password')
    def validate_password(self, value):
        if not value:
            raise ValidationError('password cannot be empty')

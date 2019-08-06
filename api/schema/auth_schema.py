from collections import namedtuple

from marshmallow import Schema, fields, post_load, validates, ValidationError

StudentLogin = namedtuple('StudentLogin', [
    'reg_no',
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
            raise ValidationError('reg number cannnot be empty')

    @validates('password')
    def validate_password(self, value):
        if not value:
            raise ValidationError('password cannnot be empty')

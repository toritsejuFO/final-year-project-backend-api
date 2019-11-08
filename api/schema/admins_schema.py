from collections import namedtuple
import re

from marshmallow import Schema, fields, ValidationError, validates, post_load

from api.model import Admin

def is_school_email(email):
    return True if re.match(r'[^@]+@futo.edu.ng', email) else False

NewAdmin = namedtuple('NewAdmin', [
    'name',
    'email',
    'password'
])


class NewAdminSchema(Schema):
    name = fields.String(required=True, error_messages={'required': 'Name is required'})
    email = fields.String(required=True, error_messages={'required': 'Email is required'})
    password = fields.String(required=True, error_messages={'required': 'Password is required'})

    @post_load
    def new_admin(self, data, **kwargs):
        return NewAdmin(**data)

    @validates('name')
    def validate_name(self, value):
        max_len = 128
        if not value:
            raise ValidationError('Name cannot be empty')
        if len(value) > 128:
            raise ValidationError(f'Name cannot exceed {max_len} characters')

    @validates('email')
    def validate_email(self, value):
        max_len = 128
        admin = Admin.query.filter_by(email=value).first()
        if not value:
            raise ValidationError('Email cannot be empty')
        if len(value) > 128:
            raise ValidationError(f'Email cannot exceed {max_len} characters')
        if not is_school_email(value):
            raise ValidationError('Invalid email')
        if admin:
            raise ValidationError('Admin with this email already exists')

    @validates('password')
    def validate_password(self, value):
        max_len = 128
        if not value:
            raise ValidationError('Password cannot be empty')
        if len(value) > 128:
            raise ValidationError(f'Password cannot exceed {max_len} characters')
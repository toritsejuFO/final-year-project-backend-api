from collections import namedtuple

from marshmallow import Schema, ValidationError, fields, post_load, validates

from api.model import HOD, Department

NewHOD = namedtuple('NewHOD', [
    'name',
    'email',
    'department',
    'password'
])

EditHOD = namedtuple('EditHOD', [
    'name',
    'password',
])

class EditHODSchema(Schema):
    name = fields.String(required=True, error_messages={'required': 'Name is required'})
    password = fields.String(required=True, error_messages={'required': 'Password is required'})

    @post_load
    def edit_me(self, data, **kwargs):
        return EditHOD(**data)

    @validates('name')
    def validate_name(self, value):
        max_len = 100
        if not value:
            raise ValidationError('Name cannot be empty')
        if len(value) > max_len:
            raise ValidationError(f'Name cannot exceed {max_len} characters')


class NewHODSchema(Schema):
    name = fields.String(required=True, error_messages={'required': 'Name is required'})
    email = fields.Email(required=True, error_messages={'required': 'Email is required'})
    department = fields.String(required=True, error_messages={'required': 'Department is required'})
    password = fields.String(required=True, error_messages={'required': 'Password is required'})

    @post_load
    def new_lecturer(self, data, *kwargs):
        return NewHOD(**data)

    @validates('name')
    def validate_name(self, value):
        max_len = 100
        if not value:
            raise ValidationError('Name cannot be empty')
        if len(value) > max_len:
            raise ValidationError(f'Name cannot exceed {max_len} characters')

    @validates('email')
    def Validate_email(self, value):
        max_len = 128
        hod = HOD.query.filter_by(email=value).first()
        if not value:
            raise ValidationError('Email cannot be empty')
        if len(value) > max_len:
            raise ValidationError(f'Email cannot exceed {max_len} characters')
        if hod:
            raise ValidationError('HODs with this email already exists')

    @validates('department')
    def validate_department(self, value):
        dept = Department.query.filter_by(code=value).first()
        if not value:
            raise ValidationError('department cannot be empty')
        if not dept:
            raise ValidationError('Sorry, HODs from this department cannot use the system currently')

    @validates('password')
    def validate_password(self, value):
        if not value:
            raise ValidationError('Password cannot be empty')

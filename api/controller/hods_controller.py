from flask import request
from flask_restplus import Resource, Namespace, fields
from marshmallow import ValidationError

from api.service import HODService #, hod_login_required
from api.schema import NewHODSchema

hod_api = Namespace(
    'hods', description='API endpoints for managing HOD Resource')

hod_reg = hod_api.model('HOD Registration', {
    'name': fields.String(required=True, description='HOD\'s name'),
    'email': fields.String(required=True, description='HOD\'s email'),
    'department': fields.String(required=True, description='HOD\'s department'),
    'password': fields.String(required=True, description='HOD\'s password'),
})


@hod_api.route('/signup')
class HODSignup(Resource):
    @hod_api.doc('Register a new hod')
    @hod_api.response(201, 'New hod successfully registered')
    @hod_api.expect(hod_reg)
    def post(self):
        data = request.json
        payload = hod_api.payload or data
        schema = NewHODSchema(strict=True)

        try:
            new_payload = schema.load(payload).data._asdict()
        except ValidationError as e:
            response = {
                'status': False,
                'message': e.messages
            }
            return response, 400
        response, code = HODService.create_hod(data=new_payload)
        return response, code

@hod_api.route('/me')
class Me(Resource):
    # @hod_login_required
    @hod_api.doc('View HOD details', security='apiKey')
    def get(self, decoded_payload):
        email = decoded_payload.get('email')
        response, code = HODService.get_me(email=email)
        return response, code
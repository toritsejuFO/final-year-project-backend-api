from datetime import datetime, timedelta

from api.model import RevokedToken
from api.model import Student, RevokedToken

class AuthService():
    @staticmethod
    def login_student(data):
        response = {}
        reg_no = data['reg_no']
        password = data['password']

        try:
            student = Student.query.filter_by(reg_no=reg_no).first()
        except:
            response['status'] = False
            response['message'] = 'Internal Server Error'
            return response, 500

        if not student:
            response['status'] = False
            response['message'] = 'Invalid reg number or password'
            return response, 401

        if not student.verify_password(password):
            response['status'] = False
            response['message'] = 'Invalid reg number or password'
            return response, 401

        encode_data = {
            'reg_no': student.reg_no
        }
        token = student.encode_auth_token(data=encode_data, expiry=datetime.utcnow() + timedelta(days=1))

        if not isinstance(token, bytes):
            response['status'] = False
            response['message'] = token
            return response, 500

        response['status'] = True
        response['message'] = 'Logged in successfully'
        response['x-auth-token'] = token.decode()
        return response, 200

    @staticmethod
    def logout_student(auth_token):
        response = {}
        decoded_msg = Student.decode_auth_token(auth_token=auth_token)

        # Error decoding error
        if isinstance(decoded_msg, str):
            response['status'] = False
            response['message'] = decoded_msg
            return response, 403

        # Check revoked token
        if RevokedToken.check(token=auth_token):
            response['status'] = False
            response['message'] = 'Revoked token. Please log in again'
            return response, 403

        # Mark token as revoked and logout student
        try:
            revoked_token = RevokedToken(token=auth_token)
            revoked_token.save()
        except:
            response['status'] = False
            response['message'] = 'Internal Server Error'
            return response, 500

        response['status'] = True
        response['message'] = 'Logged out successfully'
        return response, 200


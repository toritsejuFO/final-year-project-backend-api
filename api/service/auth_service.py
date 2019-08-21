from functools import wraps
from datetime import datetime, timedelta

import jwt
from flask import request

from api.model import Student, RevokedToken, Lecturer, HOD
from config import jwt_key

class AuthService():
    @staticmethod
    def login_student(data):
        response = {}
        reg_no = data['reg_no']
        password = data['password']

        try:
            student = Student.query.filter_by(reg_no=reg_no).first()
        except Exception:
            response['success'] = False
            response['message'] = 'Internal Server Error'
            return response, 500

        if not student:
            response['success'] = False
            response['message'] = 'Invalid reg number or password'
            return response, 401

        if not student.verify_password(password):
            response['success'] = False
            response['message'] = 'Invalid reg number or password'
            return response, 401

        encode_data = {
            'reg_no': student.reg_no,
            'student': True,
            'entity': 'student'
        }
        token = encode_auth_token(data=encode_data, expiry=datetime.utcnow() + timedelta(days=1))

        if not isinstance(token, bytes):
            response['success'] = False
            response['message'] = token
            return response, 500

        response['success'] = True
        response['message'] = 'Logged in successfully'
        response['x-auth-token'] = token.decode()
        return response, 200

    @staticmethod
    def logout_student(auth_token):
        response = {}
        decoded_payload = decode_auth_token(auth_token=auth_token)

        # Error decoding error
        if isinstance(decoded_payload, str):
            response['success'] = False
            response['message'] = decoded_payload
            return response, 401

        # Ensure this method logs out only students
        if decoded_payload.get('reg_no') is None:
            response['success'] = True
            response['message'] = 'Unathorized to perform action'
            return response, 403

        # Check revoked token
        if RevokedToken.check(token=auth_token):
            response['success'] = False
            response['message'] = 'Revoked token. Please log in again'
            return response, 403

        # Mark token as revoked and logout student
        try:
            revoked_token = RevokedToken(token=auth_token)
            revoked_token.save()
        except Exception:
            response['success'] = False
            response['message'] = 'Internal Server Error'
            return response, 500

        response['success'] = True
        response['message'] = 'Logged out successfully'
        return response, 200

    @staticmethod
    def login_lecturer(data):
        response = {}
        email = data['email']
        password = data['password']

        try:
            lecturer = Lecturer.query.filter_by(email=email).first()
        except Exception:
            response['success'] = False
            response['message'] = 'Internal Server Error'
            return response, 500

        if not lecturer:
            response['success'] = False
            response['message'] = 'Invalid email or password'
            return response, 401

        if not lecturer.verify_password(password):
            response['success'] = False
            response['message'] = 'Invalid email or password'
            return response, 401

        encode_data = {
            'email': lecturer.email,
            'lecturer': True,
            'entity': 'lecturer'
        }
        token = encode_auth_token(data=encode_data, expiry=datetime.utcnow() + timedelta(days=1))

        if not isinstance(token, bytes):
            response['success'] = False
            response['message'] = token
            return response, 500

        response['success'] = True
        response['message'] = 'Logged in successfully'
        response['x-auth-token'] = token.decode()
        return response, 200

    @staticmethod
    def logout_lecturer(auth_token):
        response = {}
        decoded_payload = decode_auth_token(auth_token=auth_token)

        # Error decoding error
        if isinstance(decoded_payload, str):
            response['success'] = False
            response['message'] = decoded_payload
            return response, 401

        # Ensure this method logs out only lecturers
        if decoded_payload.get('lecturer') is None:
            response['success'] = True
            response['message'] = 'Unathorized to perform action'
            return response, 403

        # Check revoked token
        if RevokedToken.check(token=auth_token):
            response['success'] = False
            response['message'] = 'Revoked token. Please log in again'
            return response, 403

        # Mark token as revoked and logout student
        try:
            revoked_token = RevokedToken(token=auth_token)
            revoked_token.save()
        except Exception:
            response['success'] = False
            response['message'] = 'Internal Server Error'
            return response, 500

        response['success'] = True
        response['message'] = 'Logged out successfully'
        return response, 200

    @staticmethod
    def login_hod(data):
        response = {}
        email = data['email']
        password = data['password']

        try:
            hod = HOD.query.filter_by(email=email).first()
        except Exception:
            response['success'] = False
            response['message'] = 'Internal Server Error'
            return response, 500

        if not hod:
            response['success'] = False
            response['message'] = 'Invalid email or password'
            return response, 401

        if not hod.verify_password(password):
            response['success'] = False
            response['message'] = 'Invalid email or password'
            return response, 401

        encode_data = {
            'email': hod.email,
            'hod': True,
            'entity': 'hod'
        }
        token = encode_auth_token(data=encode_data, expiry=datetime.utcnow() + timedelta(days=1))

        if not isinstance(token, bytes):
            response['success'] = False
            response['message'] = token
            return response, 500

        response['success'] = True
        response['message'] = 'Logged in successfully'
        response['x-auth-token'] = token.decode()
        return response, 200

    @staticmethod
    def logout_hod(auth_token):
        response = {}
        decoded_payload = decode_auth_token(auth_token=auth_token)

        # Error decoding error
        if isinstance(decoded_payload, str):
            response['success'] = False
            response['message'] = decoded_payload
            return response, 401

        # Ensure this method logs out only hods
        if decoded_payload.get('hod') is None:
            response['success'] = True
            response['message'] = 'Unathorized to perform action'
            return response, 403

        # Check revoked token
        if RevokedToken.check(token=auth_token):
            response['success'] = False
            response['message'] = 'Revoked token. Please log in again'
            return response, 403

        # Mark token as revoked and logout student
        try:
            revoked_token = RevokedToken(token=auth_token)
            revoked_token.save()
        except Exception:
            response['success'] = False
            response['message'] = 'Internal Server Error'
            return response, 500

        response['success'] = True
        response['message'] = 'Logged out successfully'
        return response, 200

    @staticmethod
    def verify(auth_token):
        response = {}
        decoded_payload = decode_auth_token(auth_token=auth_token)

        if isinstance(decoded_payload, str):
            response['success'] = False
            response['message'] = decoded_payload
            return response, 401

        if RevokedToken.check(token=auth_token):
            response['success'] = False
            response['message'] = 'Token revoked'
            return response, 403

        response['success'] = True
        response['entity'] = decoded_payload['entity']
        return response, 200


#####################################################################################
############### Helper methods for encoding and decoding auth tokens ################
#####################################################################################

def encode_auth_token(data=None, expiry=datetime.utcnow() + timedelta(days=1)):
    if data is None:
        return 'Invalid "sub"[subscriber] passed'
    try:
        payload = {
            'sub': data,
            'exp': expiry,
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, jwt_key, algorithm='HS256')
    except Exception as e:
        return repr(e)

def decode_auth_token(auth_token=None):
    try:
        payload = jwt.decode(auth_token, jwt_key)
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Expired token. Please log in again'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again'

#####################################################################################
#####################################################################################


########################################################
############ Decorators for Authentication #############
########################################################

def student_login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = {}
        auth_token = request.headers.get('x-auth-token')
        if not auth_token or auth_token is None:
            response = {
                'success': False,
                'message': 'Please provide a token'
            }
            return response, 401

        decoded_payload = decode_auth_token(auth_token=auth_token)

        # Error decoding token
        if isinstance(decoded_payload, str):
            response['success'] = False
            response['message'] = decoded_payload
            return response, 401

        # Check revoked token
        if RevokedToken.check(token=auth_token):
            response['success'] = False
            response['message'] = 'Revoked token. Please log in again'
            return response, 403

        return func(*args, **kwargs, decoded_payload=decoded_payload)
    return wrapper

def lecturer_login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = {}
        auth_token = request.headers.get('x-auth-token')
        if not auth_token or auth_token is None:
            response = {
                'success': False,
                'message': 'Please provide a token'
            }
            return response, 401

        decoded_payload = decode_auth_token(auth_token=auth_token)

        # Error decoding token
        if isinstance(decoded_payload, str):
            response['success'] = False
            response['message'] = decoded_payload
            return response, 401

        # Check revoked token
        if RevokedToken.check(token=auth_token):
            response['success'] = False
            response['message'] = 'Revoked token. Please log in again'
            return response, 403

        return func(*args, **kwargs, decoded_payload=decoded_payload)
    return wrapper

def hod_login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = {}
        auth_token = request.headers.get('x-auth-token')
        if not auth_token or auth_token is None:
            response = {
                'success': False,
                'message': 'Please provide a token'
            }
            return response, 401

        decoded_payload = decode_auth_token(auth_token=auth_token)

        # Error decoding token
        if isinstance(decoded_payload, str):
            response['success'] = False
            response['message'] = decoded_payload
            return response, 401

        # Check revoked token
        if RevokedToken.check(token=auth_token):
            response['success'] = False
            response['message'] = 'Revoked token. Please log in again'
            return response, 403

        return func(*args, **kwargs, decoded_payload=decoded_payload)
    return wrapper

########################################################
########################################################

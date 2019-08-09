from api.model import Lecturer

class LecturerService:
    @staticmethod
    def create_lecturer(data):
        response = {}
        name = data['name']
        email = data['email']
        department_code = data['department']
        password = data['password']

        try:
            lecturer = Lecturer(
                name=name,
                email=email,
                department_code=department_code,
                password=password
            )
            lecturer.save()
        except Exception:
            response['status'] = False
            response['message'] = "Internal Server Error"
            return response, 500

        response['status'] = True
        response['message'] = 'New Lecturer registered successsfully'
        return response, 201

    @staticmethod
    def get_me(email):
        response = {}
        try:
            lecturer = Lecturer.query.filter_by(email=email).first()
        except:
            response['status'] = False
            response['message'] = 'Internal Server Error'
            return response, 500

        if not lecturer:
            response['status'] = False
            response['message'] = 'Lecturer Not Found'
            return response, 404

        response['status'] = True
        response['data'] = lecturer.to_dict
        return response, 200

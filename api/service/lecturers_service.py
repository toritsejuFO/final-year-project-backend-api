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

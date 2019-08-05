from api.model import Student

class StudentService():
    @staticmethod
    def get_all_students():
        response = {}
        try:
            students = Student.query.all()
        except Exception as e:
            response['status'] = False
            response['message'] = 'Internal Server Error'
            response['error'] = e
            return response, 500

        if not students:
            response['status'] = True
            response['message'] = 'Students not found'
            return response, 200

        response['status'] = True
        response['data'] = [student.to_dict() for student in students]
        return response, 200

    @staticmethod
    def create_student(data=None):
        response = {}
        try:
            student = Student(**data)
            student.save()
        except Exception as e:
            response['status'] = False
            response['message'] = 'Internal Server Error'
            response['error'] = e
            return response, 500

        response['status'] = True
        response['message'] = 'New student successfully registered'
        response['data'] = student.to_dict()
        return response, 201

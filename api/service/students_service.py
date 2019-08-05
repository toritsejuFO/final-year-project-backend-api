from api.model import Student

class StudentService():
    @staticmethod
    def get_all_students():
        response = {}
        try:
            students = Student.query.all()
        except Exception as e:
            response['status'] = False
            response['message'] = 'Unable to perform request. Please try again'
            response['error'] = e
            return response, 500

        if not students:
            response['status'] = True
            response['message'] = 'Students not found'
            return response, 200

        response['status'] = True
        response['data'] = [student.to_dict() for student in students]
        return response, 200


from api.model import Student, Department, Level

class StudentService():
    @staticmethod
    def get_all_students():
        response = {}
        try:
            students = Student.query.all()
        except:
            response['status'] = False
            response['message'] = 'Internal Server Error'
            return response, 500

        if not students:
            response['status'] = False
            response['message'] = 'Students Not Found'
            return response, 404

        response['status'] = True
        response['data'] = [student.to_dict for student in students]
        return response, 200

    @staticmethod
    def create_student(data=None):
        response = {}
        try:
            student = Student(**data)
            student.save()
        except:
            response['status'] = False
            response['message'] = 'Internal Server Error'
            return response, 500

        response['status'] = True
        response['message'] = 'New student successfully registered'
        return response, 201

    @staticmethod
    def get_me(reg_no):
        response = {}
        try:
            student = Student.query.filter_by(reg_no=reg_no).first()
        except:
            response['status'] = False
            response['message'] = 'Internal Server Error'
            return response, 500

        if not student:
            response['status'] = False
            response['message'] = 'Student Not Found'
            return response, 404

        response['status'] = True
        response['data'] = student.to_dict
        return response, 200

    @staticmethod
    def edit_me(reg_no, data):
        response = {}
        level = data['level']
        department = data['department']
        try:
            student = Student.query.filter_by(reg_no=reg_no).first()
        except:
            response['status'] = False
            response['message'] = 'Internal Server Error'
            return response, 500

        if not student:
            response['status'] = False
            response['message'] = 'Student Not Found'
            return response, 404

        if student.reg_complete:
            response['status'] = False
            response['message'] = "You cannot update your details anymore"
            return response, 403

        try:
            student.level = Level.query.filter_by(level=level).first()
            student.department = Department.query.filter_by(code=department).first()
            student.reg_complete = True
            student.save()
        except:
            response['status'] = False
            response['message'] = 'Internal Server Error'
            return response, 500

        response['status'] = True
        response['message'] = 'Details updated successfully'
        return response, 200

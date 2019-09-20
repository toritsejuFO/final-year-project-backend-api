from api.model import School

class SchoolService:
    @staticmethod
    def get_all():
        response = {}
        try:
            schools = School.query.order_by(School.code).all()
        except Exception:
            response['success'] = False
            response['message'] = 'Internal Server Error'
            return response, 500

        if not schools:
            response['success'] = False
            response['message'] = 'Schools Not Found'
            return response, 404

        response['success'] = True
        response['data'] = [school.code for school in schools]
        return response, 200

    @staticmethod
    def get_departments(school_code):
        response = {}
        try:
            school = School.query.filter_by(code=school_code).first()
        except Exception:
            response['success'] = False
            response['message'] = 'Internal Server Error'
            return response, 500

        if not school:
            response['success'] = False
            response['message'] = 'School Not Found'
            return response, 404

        departments = school.departments
        if not departments:
            response['success'] = False
            response['message'] = f'No Departments Not Found for this {school_code}'
            return response, 404

        response['success'] = True
        response['data'] = [dept.code for dept in departments]
        return response, 200

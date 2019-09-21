from api import AppException
from api.model import Department

class DepartmentService:
    @staticmethod
    def get_all():
        response = {}
        try:
            departments = Department.query.order_by(Department.code).all()
        except Exception:
            raise AppException('Internal Server Error', 500)

        if not departments:
            response['success'] = False
            response['message'] = 'Departments Not Found'
            return response, 404

        response['success'] = True
        response['data'] = [department.to_dict for department in departments]
        return response, 200

from api.model import HOD

class HODService:
    @staticmethod
    def create_hod(data):
        response = {}
        name = data['name']
        email = data['email']
        department_code = data['department']
        password = data['password']

        try:
            hod = HOD(
                name=name,
                email=email,
                department_code=department_code,
                password=password
            )
            hod.save()
        except Exception:
            response['success'] = False
            response['message'] = "Internal Server Error"
            return response, 500

        response['success'] = True
        response['message'] = 'New HOD registered successsfully'
        return response, 201

    @staticmethod
    def get_me(email):
        response = {}
        try:
            hod = HOD.query.filter_by(email=email).first()
        except Exception:
            response['success'] = False
            response['message'] = 'Internal Server Error'
            return response, 500

        if not hod:
            response['success'] = False
            response['message'] = 'HOD Not Found'
            return response, 404

        response['success'] = True
        response['data'] = hod.to_dict
        return response, 200

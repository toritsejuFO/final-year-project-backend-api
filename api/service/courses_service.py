from api.model import Course

class CourseService:
    @staticmethod
    def get_all_courses():
        response = {}
        try:
            courses = Course.query.all()
        except:
            response['status'] = False
            response['message'] = 'Internal Server Error'
            return response, 500

        response['status'] = True
        response['data'] = [course.to_dict for course in courses]
        return response, 200

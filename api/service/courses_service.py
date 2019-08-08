from api.model import Course, Department, Level

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

        if not courses:
            response['status'] = False
            response['message'] = 'No courses found'
            return response, 404
        
        response['status'] = True
        response['data'] = [course.to_dict for course in courses]
        return response, 200

    @staticmethod
    def get_courses_by_dept_level(department, level):
        response = {}
        try:
            department_ = Department.query.filter_by(code=department).first()
            level_ = Level.query.filter_by(level=level).first()
            courses = Course.query.filter_by(department=department_, level=level_).all()
        except:
            response['status'] = False
            response['message'] = 'Internal Server Error'
            return response, 500

        if not courses:
            response['status'] = False
            response['message'] = f'No courses found for "{department}" department in "{level}" level'
            return response, 404

        response['status'] = True
        response['data'] = [course.to_dict for course in courses]
        return response, 200

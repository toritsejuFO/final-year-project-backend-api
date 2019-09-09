from api import db
from api.model import Level, Department, Semester


class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    code = db.Column(db.String(6))
    level_id = db.Column(db.Integer, db.ForeignKey('levels.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    semester_id = db.Column(db.Integer, db.ForeignKey('semesters.id'))
    units = db.Column(db.Integer)

    def __init__(self, title, code, level, department_code, semester, units):
        self.title = title
        self.code = code
        self.level = Level.query.filter_by(level=level).first()
        self.department = Department.query.filter_by(code=department_code).first()
        self.semester = Semester.query.filter_by(semester=semester).first()
        self.units = units

    @staticmethod
    def exists(course_code):
        return Course.query.filter_by(code=course_code).count() > 0

    @property
    def to_dict(self):
        json_course = {
            'course_code': self.code,
            'course_title': self.title,
            'course_unit': self.units,
            'level_oferred':  self.level.level,
            'department': self.department.code,
            'school': self.department.school.code,
            'semester_offered': self.semester.semester
        }
        return json_course

    def save(self):
        db.session.add(self)
        db.session.commit()
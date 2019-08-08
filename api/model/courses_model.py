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

    def __init__(self, title, code, level, department_code, semester):
        self.title = title
        self.code = code
        self.level = Level.query.filter_by(level=level).first()
        self.department = Department.query.filter_by(code=department_code).first()
        self.semester = Semester.query.filter_by(semester=semester).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
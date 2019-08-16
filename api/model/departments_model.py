from api import db
from api.model import School

class Department(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    code = db.Column(db.String(3))
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'))
    students = db.relationship('Student', backref='department')
    courses = db.relationship('Course', backref='department')
    lecturers = db.relationship('Lecturer', backref='department')
    hods = db.relationship('HOD', backref='department')

    def __init__(self, name=None, code=None, school_code=None):
        self.name = name
        self.code = code
        self.school = School.query.filter_by(code=school_code).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

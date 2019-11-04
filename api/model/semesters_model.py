from api import db


class Semester(db.Model):
    __tablename__ = 'semesters'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    semester = db.Column(db.String(7))
    courses = db.relationship('Course', backref='semester')

    def __init__(self, semester):
        self.semester = semester

    @staticmethod
    def exists(department_code):
        return Semester.query.filter_by(semester=semester).count() > 0

    def save(self):
        db.session.add(self)
        db.session.commit()

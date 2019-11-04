from api import db

class Level(db.Model):
    __tablename__ = 'levels'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    level = db.Column(db.String(3))
    students = db.relationship('Student', backref='level')
    courses = db.relationship('Course', backref='level')

    def __init__(self, level=None):
        self.level = level

    @staticmethod
    def exists(department_code):
        return Level.query.filter_by(level=level).count() > 0

    def save(self):
        db.session.add(self)
        db.session.commit()

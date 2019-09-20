from api import db

class School(db.Model):
    __tablename__ = 'schools'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    code = db.Column(db.String(4))
    departments = db.relationship('Department', backref='school')

    def __init__(self, name=None, code=None):
        self.name = name
        self.code = code

    @staticmethod
    def exists(school_code):
        return School.query.filter_by(code=school_code).count() > 0

    @property
    def to_dict(self):
        json_school = {
            'code': self.code,
            'fullname': self.name
        }
        return json_school

    def save(self):
        db.session.add(self)
        db.session.commit()

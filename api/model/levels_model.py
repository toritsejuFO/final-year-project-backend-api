from api import db

class Level(db.Model):
    __tablename__ = 'levels'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    level = db.Column(db.String(3))
    students = db.relationship('Student', backref='level')

    def __init__(self, level=None):
        self.level = level

    def save(self):
        db.session.add(self)
        db.session.commit()

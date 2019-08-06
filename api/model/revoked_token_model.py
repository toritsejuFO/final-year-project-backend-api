from datetime import datetime

from api import db

class RevokedToken(db.Model):
    __tablename__ = 'revoked_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(300), unique=True, nullable=False)
    revoked_on = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, token):
        self.token = token

    @staticmethod
    def check(token):
        token = RevokedToken.query.filter_by(token=token).first()
        if token:
            return True
        else:
            return False

    def save(self):
        db.session.add(self)
        db.session.commit()

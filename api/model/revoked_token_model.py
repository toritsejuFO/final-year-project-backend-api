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
        return RevokedToken.query.filter_by(token=token).count() > 0

    def save(self):
        db.session.add(self)
        db.session.commit()

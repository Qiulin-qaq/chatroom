from datetime import datetime
from ..extensions import db


class PrivateSession(db.Model):
    __tablename__ = 'private_session'

    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_time = db.Column(db.DateTime, default=datetime.utcnow)

    user1 = db.relationship('User', foreign_keys=[user1_id], backref='private_sessions1')
    user2 = db.relationship('User', foreign_keys=[user2_id], backref='private_sessions2')

    def to_dict(self):
        return {
            'id': self.id,
            'user1_id': self.user1_id,
            'user2_id': self.user2_id,
            'created_time': self.created_time.strftime('%Y-%m-%d %H:%M:%S')
        }

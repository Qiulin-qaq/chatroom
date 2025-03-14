
from ..extensions import db


class ChatRoom(db.Model):
    __tablename__ = 'chatroom'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_time = db.Column(db.DateTime, nullable=False)
    creator = db.relationship('User', backref='created_chatrooms')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'creator_id': self.creator_id,
            'created_time': self.created_time.strftime('%Y-%m-%d %H:%M:%S'),

        }



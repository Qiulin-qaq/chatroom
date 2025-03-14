from datetime import datetime
from ..extensions import db


class Message(db.Model):
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    session_type = db.Column(db.Enum('group', 'private'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('chatroom.id'))
    private_session_id = db.Column(db.Integer, db.ForeignKey('private_session.id'))
    content = db.Column(db.Text, nullable=False)

    sent_time = db.Column(db.DateTime, default=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref='messages')
    room = db.relationship('ChatRoom', backref='messages')
    private_session = db.relationship('PrivateSession', backref='messages')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'session_type': self.session_type,
            'room_id': self.room_id,
            'private_session_id': self.private_session_id,
            'content': self.content,

            'sent_time': self.sent_time.strftime('%Y-%m-%d %H:%M:%S'),
            'is_deleted': self.is_deleted
        }

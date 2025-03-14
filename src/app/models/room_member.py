from datetime import datetime
from ..extensions import db


class RoomMember(db.Model):
    __tablename__ = 'room_members'

    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('chatroom.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role = db.Column(db.Enum('member', 'admin'), default='member')
    joined_time = db.Column(db.DateTime, default=datetime.utcnow)

    room = db.relationship('ChatRoom', backref='members')
    user = db.relationship('User', backref='room_memberships')

    def to_dict(self):
        return {
            'id': self.id,
            'room_id': self.room_id,
            'room_name': self.room.name,
            'user_id': self.user_id,
            'role': self.role,
            'joined_time': self.joined_time.strftime('%Y-%m-%d %H:%M:%S')
        }
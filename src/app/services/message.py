from datetime import datetime

from ..extensions import db
from ..models.chatroom import ChatRoom
from ..models.message import Message
from ..models.room_member import RoomMember
from ..utils.R import R
from flask_login import current_user


def send_message(data):
    try:
        room_id = data['room_id']
        content = data['content']
        print(data['room_id'])
        room = db.session.query(RoomMember).filter_by(room_id=room_id).first()
        if not room:
            return R.fail(message='聊天室不存在')
        user_in_room = db.session.query(RoomMember).filter_by(room_id=room_id, user_id=current_user.id).first()
        if not user_in_room:
            return R.fail(message='您不在该聊天室中，无法发送消息')

        message = Message(
            user_id=current_user.id,
            room_id=room_id,
            content=content,
            sent_time=datetime.utcnow(),
            session_type='group'
        )
        db.session.add(message)
        db.session.commit()

        return R.ok(message='发送成功', data=message.to_dict())

    except Exception as e:
        db.session.rollback()
        return R.fail(message=str(e))

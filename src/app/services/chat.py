from datetime import datetime

from ..extensions import db
from ..models.chatroom import ChatRoom
from ..models.room_member import RoomMember
from ..utils.R import R
from flask_login import current_user


def create_chatroom(room_name):
    try:
        chatroom = ChatRoom(name=room_name, creator_id=current_user.id, created_time=datetime.now())

        db.session.add(chatroom)

        db.session.commit()
        room_member = RoomMember(room_id=chatroom.id, user_id=current_user.id, role='admin', joined_time=datetime.now())
        db.session.add(room_member)
        db.session.commit()

        return R.ok(message='聊天室创建成功', data=chatroom.to_dict())
    except Exception as e:
        db.session.rollback()
        print(e)
        return R.fail(message="创建聊天室失败")


def list_chatroom():
    try:
        list_chatroom = RoomMember.query.filter_by(user_id=current_user.id).all()

        return R.ok(message='获取聊天室列表成功', data=[chatroom.to_dict() for chatroom in list_chatroom])
    except Exception as e:
        return R.fail(message="获取聊天室列表失败")

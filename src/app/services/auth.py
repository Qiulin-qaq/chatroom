from flask import jsonify

from ..models.user import User
from ..models.chatroom import ChatRoom
from ..models.friend import Friend
from ..models.private_session import PrivateSession
from ..models.message import Message
from ..models.room_member import RoomMember
from ..extensions import db
from ..utils.R import R


def register(telephone, password):
    user = User.query.filter_by(telephone=telephone).first()
    if user:
        return R.fail(message='手机号已被注册')

    try:
        new_user = User(telephone=telephone, password=password)
        db.session.add(new_user)
        db.session.commit()

        return R.ok(message='注册成功', code=200)
    except Exception as e:
        db.session.rollback()
        return R.fail(message="注册失败")


def login(telephone, password):
    user = User.query.filter_by(telephone=telephone).first()
    if not user or not user.verify_password(password):
        return R.fail(message='手机号或密码错误')

    return R.ok(message='登录成功', data=user.to_dict())

from datetime import datetime

from flask import current_app

from ..extensions import db
from ..models.chatroom import ChatRoom
from ..models.room_member import RoomMember
from ..utils.R import R
from flask_login import current_user
from datetime import timezone


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


def join_chatroom(data):
    """
    加入聊天室核心服务
    Args:
        data (dict): 原始请求数据
    Returns:
        R: 标准化响应对象
    """
    try:
        # 参数验证
        if not isinstance(data, dict):
            return R.fail(message="无效的请求格式", code=400)
        
        # 必要参数检查
        if 'room_id' not in data:
            return R.fail(message="缺少room_id参数", code=400)
        
        # 类型转换
        try:
            room_id = int(data['room_id'])
        except (ValueError, TypeError):
            return R.fail(message="聊天室ID必须为整数", code=400)
        
        # 参数范围验证
        if room_id <= 0:
            return R.fail(message="无效的聊天室ID", code=400)
        
        # 业务逻辑验证
        chatroom = ChatRoom.query.get(room_id)
        if not chatroom:
            current_app.logger.warning(f"聊天室不存在: {room_id}")
            return R.fail(message="聊天室不存在", code=404)
        
        # 检查成员关系
        if RoomMember.query.filter_by(room_id=room_id, user_id=current_user.id).first():
            current_app.logger.debug(f"用户已加入聊天室: {current_user.id} -> {room_id}")
            return R.fail(message="您已在该聊天室中", code=409)
        
        # 创建成员记录
        new_member = RoomMember(
            room_id=room_id,
            user_id=current_user.id,
            role='member',
            joined_time=datetime.now()
        )
        
        db.session.add(new_member)
        db.session.commit()
        current_app.logger.info(f"用户加入成功: {current_user.id} -> {room_id}")
        return R.ok(message="成功加入聊天室", code=200)
        

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"加入聊天室失败: {str(e)}")
        return R.fail(message="加入聊天室失败", code=500)


from datetime import datetime

from ..extensions import db
from ..models.chatroom import ChatRoom
from ..models.message import Message
from ..models.room_member import RoomMember
from ..utils.R import R
from flask import current_app
from flask_login import current_user


def send_message(data):
    """
    发送消息到指定聊天室

    Args:
        data (dict): 包含消息内容的字典，必须包含 room_id 和 content 字段
            - room_id: 聊天室ID
            - content: 消息内容

    Returns:
        dict: 包含发送结果的响应对象
            - 成功时返回消息详情
            - 失败时返回错误信息

    Raises:
        Exception: 数据库操作异常时抛出
    """
    try:
        room_id = data['room_id']
        content = data['content']
        print(data)

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
            sent_time=datetime.now(),
            session_type='group'
        )
        db.session.add(message)
        db.session.commit()

        return R.ok(message='发送成功', data=message.to_dict(), code=200)

    except Exception as e:
        db.session.rollback()
        return R.fail(message=str(e)), 500


def get_message(data):
    """
    获取指定聊天室的消息记录。

    Args:
        room_id (int): 聊天室ID
        sent_time (str): 消息时间过滤点,格式为'YYYY-MM-DD HH:MM:SS',可选

    Returns:
        dict: 包含状态码和消息列表的响应对象
            成功时返回消息列表,每条消息包含:
                - id: 消息ID
                - content: 消息内容
                - sender: 发送者用户名
                - sent_time: 发送时间
            失败时返回错误信息和状态码

    Raises:
        Exception: 当数据库查询等操作发生异常时
    """
    """消息获取服务"""
    try:
        # 参数验证
        room_id = data['room_id']
        sent_time = data.get('send_time')
        sender_id = data.get('sender_id')  # 使用get方法避免KeyError
        
        if not room_id or not isinstance(room_id, int):
            current_app.logger.warning(f"无效的聊天室ID: {room_id}")
            return R.fail(message="无效的聊天室ID", code=400)
        # 新增sender_id类型验证
        if sender_id and not isinstance(sender_id, int):
            return R.fail(message="发送者ID格式错误", code=400)
        
        # 权限验证
        membership = RoomMember.query.filter_by(
            room_id=room_id,
            user_id=current_user.id
        ).first()
        if not membership:
            current_app.logger.warning(f"未授权访问尝试: 用户{current_user.id}访问聊天室{room_id}")
            return R.fail(message="无权限查看该聊天室消息", code=403)
        print (room_id)
        # 时间处理
        base_time = datetime.min
        try:
            filter_time = datetime.strptime(sent_time, '%Y-%m-%d %H:%M:%S') if sent_time else base_time
        except ValueError:
            return R.fail(message="时间格式应为YYYY-MM-DD HH:MM:SS", code=400)

        # 构建查询
        query = Message.query.filter_by(room_id=room_id)
        # 添加发送者过滤条件
        if sender_id:
            query = query.filter(Message.user_id == sender_id)
        if filter_time > base_time:
            query = query.filter(Message.sent_time > filter_time)

        messages = query.order_by(Message.sent_time.asc()).all()
        
        return R.ok(data=[{
            "id": msg.id,
            "content": msg.content,
            "sender": {  # 优化返回结构
                "user_id": msg.user_id,
                "nickname": msg.user.nickname  # 需要User模型关联
            },
            "sent_time": msg.sent_time.isoformat()
        } for msg in messages])

    except Exception as e:
        current_app.logger.error(f"消息查询失败: {str(e)}", exc_info=True)
        return R.fail(message="消息查询服务异常", code=500)

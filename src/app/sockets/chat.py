import uuid

from flask_socketio import emit, join_room, leave_room
from flask_login import current_user, login_required
from datetime import datetime, time
from ..extensions import socketio, db
from ..models.message import Message
import logging

# 配置日志
logger = logging.getLogger('socketio')
logger.setLevel(logging.DEBUG)


@socketio.on('connect')
def handle_connect():
    """处理新连接"""
    try:
        if not current_user.is_authenticated:
            logger.warning("未认证用户尝试连接")
            return False  # 拒绝连接
        logger.info(f"用户 {current_user.nickname} 已连接")
    except Exception as e:
        logger.error(f"连接处理异常: {str(e)}")
        return False


@socketio.on('disconnect')
def handle_disconnect():
    """处理断开连接"""
    logger.info(f"用户 {current_user.nickname} 断开连接")


@socketio.on('join')
def on_join(data):
    """加入聊天室优化版"""
    try:
        room = data.get('room')
        if not room:
            emit('error', {'msg': '缺少房间参数'})
            return

        join_room(room)
        logger.debug(f"用户 {current_user.nickname} 加入房间 {room}")

        # 发送系统通知（限频）
        emit('system', {
            'type': 'join',
            'nickname': current_user.nickname,
            'timestamp': datetime.now().isoformat()
        }, room=room)

    except Exception as e:
        logger.error(f"加入房间失败: {str(e)}")
        emit('error', {'msg': '加入房间失败'})


@socketio.on('leave')
def on_leave(data):
    """离开聊天室优化版"""
    try:
        room = data.get('room')
        if not room:
            emit('error', {'msg': '缺少房间参数'})
            return

        leave_room(room)
        logger.debug(f"用户 {current_user.nickname} 离开房间 {room}")

        # 发送系统通知
        emit('system', {
            'type': 'leave',
            'nickname': current_user.nickname,
            'timestamp': datetime.now().isoformat()
        }, room=room)

    except Exception as e:
        logger.error(f"离开房间失败: {str(e)}")
        emit('error', {'msg': '离开房间失败'})


@socketio.on('message')
@login_required
def handle_message(data):
    """增强版消息处理"""
    try:
        # 参数校验
        required_fields = ['room', 'content']
        if not all(field in data for field in required_fields):
            emit('error', {'msg': '缺少必要参数'})
            return

        room_id = data['room']
        content = data['content'].strip()

        if not content:
            emit('error', {'msg': '消息内容不能为空'})
            return

        # 消息限频（示例：1秒内最多5条）
        if not check_message_rate(current_user.id):
            emit('error', {'msg': '发送频率过高'})
            return

        # 保存消息到数据库（异步）
        save_message_async(current_user.id, room_id, content)

        # 广播结构化消息
        emit('message', {
            'user': {
                'id': current_user.id,
                'nickname': current_user.nickname,
                'avatar': current_user.avatar_url
            },
            'content': content,
            'timestamp': datetime.now().isoformat(),
            'message_id': generate_message_id()  # 生成唯一ID用于客户端确认
        }, room=room_id)

    except Exception as e:
        logger.error(f"消息处理失败: {str(e)}")
        emit('error', {'msg': '消息发送失败'})


# ---------- 工具函数 ----------
message_rate = {}  # 简易限频缓存


def check_message_rate(user_id):
    """消息频率检查（生产环境应使用Redis）"""
    now = time.time()
    if user_id not in message_rate:
        message_rate[user_id] = []

    # 清理10秒前的记录
    message_rate[user_id] = [t for t in message_rate[user_id] if t > now - 10]

    if len(message_rate[user_id]) >= 5:  # 10秒内最多5条
        return False

    message_rate[user_id].append(now)
    return True


def save_message_async(user_id, room_id, content):
    """异步保存消息（使用eventlet线程池）"""
    from eventlet import tpool
    tpool.execute(_save_message, user_id, room_id, content)


def _save_message(user_id, room_id, content):
    """实际保存消息到数据库"""
    try:
        message = Message(
            user_id=user_id,
            room_id=room_id,
            content=content,
            session_type='group'
        )
        db.session.add(message)
        db.session.commit()
        logger.debug(f"消息保存成功: {message.id}")
    except Exception as e:
        db.session.rollback()
        logger.error(f"数据库保存失败: {str(e)}")


def generate_message_id():
    """生成唯一消息ID（示例实现）"""
    return f"{int(time.time() * 1000)}-{uuid.uuid4().hex[:6]}"
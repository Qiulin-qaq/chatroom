from flask import Blueprint, request, jsonify
from flask_login import login_required


ms_bp = Blueprint('message', __name__, url_prefix='/message')

from src.app.services.message import send_message,get_message

ms_bp.route('/send', methods=["POST"])


@ms_bp.route('/send', methods=['POST'])
def send_message_view():
    data = request.get_json()
    result = send_message(data)
    return jsonify(result), result['code']


@ms_bp.route('/get', methods=['GET'])
@login_required
def get_messages_view():
    """获取消息历史视图"""
    # 仅做基础参数类型转换
    data = request.get_json()
    # 调用服务层处理所有业务逻辑
    result = get_message(data)
    return jsonify(result), result['code']


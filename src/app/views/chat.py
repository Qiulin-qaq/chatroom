from flask import Blueprint
from flask_login import login_required


from ..services.chat import create_chatroom, list_chatroom

from flask import request, jsonify


chat_bp = Blueprint('chat', __name__, url_prefix='/chat')


@chat_bp.route('/chatroom/create', methods=["POST"])
@login_required
def create_chatroom_view():
    data = request.get_json()

    room_name = data['name']

    result = create_chatroom(room_name)
    return jsonify(result), result['code']


@chat_bp.route('/chatroom/list', methods=["GET"])
@login_required
def list_chatroom_view():
    result = list_chatroom()
    return jsonify(result), result['code']
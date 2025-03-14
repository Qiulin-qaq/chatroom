from flask import Blueprint, request, jsonify
from flask_login import login_required

from src.app.services.message import send_message

ms_bp = Blueprint('message', __name__, url_prefix='/message')

ms_bp.route('/send', methods=["POST"])


@ms_bp.route('/send', methods=['POST'])
def send_message_view():
    data = request.get_json()
    result = send_message(data)
    return jsonify(result), result['code']

from flask import Blueprint, jsonify, request
from flask_login import login_required
from ..utils.R import R
from ..services.friend import query_friends_service, add_friend_service

fr_bp = Blueprint('friend', __name__, url_prefix='/friends')

@fr_bp.route('/add', methods=['POST'])
@login_required
def add_friend():
    """添加好友接口"""
    data = request.get_json()
    if not data:
        return R.fail(message="无效的请求格式")
    result = add_friend_service(data)
    return jsonify(result), result['code']


@fr_bp.route('/search', methods=['GET'])
@login_required
def search_friends():
    """搜索已建立的好友接口"""
    data = request.get_json()
    if not data:
        return R.fail(message="无效的请求格式")
    result = query_friends_service(data)
    return jsonify(result), result['code']

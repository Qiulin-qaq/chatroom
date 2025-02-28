from flask import Blueprint, request, jsonify
from ..services.auth_service import register_user

auth_bp = Blueprint('auth', __name__)


# 注册
@auth_bp.route('/register', methods=['POST'])
def register():
    telephone = request.form.get('telephone')
    pwd = request.form.get('password')
    if not all([telephone, pwd]):
        return jsonify({'success': False, 'message': '手机号和密码不能为空'}), 400

    result = register_user(telephone, pwd)
    if result['success']:
        return jsonify({'message': '注册成功'}), 200
    else:
        return jsonify({'message': result['message']}), 400

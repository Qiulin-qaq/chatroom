from functools import wraps

from flask import request, jsonify

import re
from flask import Blueprint
from ..utils.R import R

from ..services.auth import register, login

# 手机号正则验证
PHONE_REGEX = r'^1[3-9]\d{9}$'

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


def validate_phone_and_pwd(func):
    """
    验证手机号和密码
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        telephone = request.form.get('telephone', '').strip()
        pwd = request.form.get('password', '').strip()
        nickname = request.form.get('nickname', '').strip()

        if not telephone or not pwd:
            return jsonify(R.fail(message='手机号和密码不能为空')), 400

        if not re.match(PHONE_REGEX, telephone):
            return jsonify(R.fail(message='手机号格式不正确')), 400

        if len(pwd) < 6:
            return jsonify(R.fail(message='密码长度至少6位')), 400

        if request.endpoint == 'auth.register_view':
            return func(telephone, pwd, nickname, *args, **kwargs)
        else:
            return func(telephone, pwd, *args, **kwargs)

    return wrapper


# 注册
@auth_bp.route('/register', methods=['POST'])
@validate_phone_and_pwd
def register_view(telephone, pwd, nickname):

    result = register(telephone, pwd, nickname)

    return jsonify(result), result['code']


@auth_bp.route('/login', methods=['POST'])
@validate_phone_and_pwd
def login_view(telephone, pwd):
    result = login(telephone, pwd)

    return jsonify(result), result['code']

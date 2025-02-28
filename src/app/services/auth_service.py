from ..models.user import User
from ..extensions import db


def register_user(telephone, password):
    user = User.query.filter_by(telephone=telephone).first()
    if user:
        return {'success': False, 'message': '账户已存在'}

    new_user = User(telephone=telephone, password=password)
    db.session.add(new_user)
    db.session.commit()

    return {'success': True, "message": "注册成功"}
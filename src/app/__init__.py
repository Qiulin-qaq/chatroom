from flask import Flask

from config import Config
from .extensions import db, bcrypt, migrate, login_manager



from .models.user import User


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 初始化扩展
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # 配置登录视图
    login_manager.login_view = 'auth.login_view'  # 指定登录页面的路由
    login_manager.login_message = '请先登录以访问此页面'  # 登录提示信息

    from .views.auth import auth_bp
    from .views.chat import chat_bp
    from .views.message import  ms_bp
    from .views.friend import  fr_bp

    # 注册蓝图
    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(ms_bp)
    app.register_blueprint(fr_bp)

    # 加载用户模型并配置用户加载器
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app

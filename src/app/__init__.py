from flask import Flask

from config import Config
from .extensions import db, bcrypt, migrate
from .routes.auth import auth_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 初始化扩展
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    # 注册蓝图
    app.register_blueprint(auth_bp, url_prefix='/auth')
    return app

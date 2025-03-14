from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager



# init数据库
db = SQLAlchemy()

# init密码哈希工具
bcrypt = Bcrypt()

# database迁移工具
migrate = Migrate()

# 初始化 Flask-Login
login_manager = LoginManager()





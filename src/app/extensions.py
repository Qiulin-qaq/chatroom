from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# init数据库
db = SQLAlchemy()

# init密码哈希工具
bcrypt = Bcrypt()

# database迁移工具
migrate = Migrate()

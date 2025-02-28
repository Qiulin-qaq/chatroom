from datetime import datetime
from ..extensions import db, bcrypt


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    telephone = db.Column(db.String(11), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_time = db.Column(db.DateTime, default=datetime.utcnow)
    last_login_time = db.Column(db.DateTime)

    @property
    def password(self):
        raise AttributeError('密码不可读')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'telephone': self.telephone,
            'created_time': self.created_time.strftime('%Y-%m-%d %H:%M:%S'),

        }

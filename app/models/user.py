from app import db  # 从app包导入db
from app.utils.security import generate_password_hash, check_password_hash
from app import bcrypt

class User(db.Model):
    __tablename__ = 'user_data'

    uid = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(1000), unique=True, nullable=False)
    passWord = db.Column(db.String(1000), nullable=False)
    role = db.Column(db.String(1000), nullable=False,default=1)
    isVip = db.Column(db.String(1000), nullable=False, default=1)

    def check_password(self, password):
        """验证哈希密码"""
        return check_password_hash(self.passWord, password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def to_dict(self):
        return {
            'uid': self.uid,
            'userName': self.userName,
            'role': self.role,
            'isVip':self.isVip
        }
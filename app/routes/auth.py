from flask_restx import Namespace, Resource, fields
from app.models.user import User
from app import db

auth_ns = Namespace('auth', description='用户认证相关操作')

# 数据模型
login_model = auth_ns.model('Login', {
    'userName': fields.String(required=True, example="admin"),
    'passWord': fields.String(required=True, example="123456")
})


@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        """明文密码登录"""
        data = auth_ns.payload

        # 简单参数检查
        if 'userName' not in data or 'passWord' not in data:
            return {"message": "需要用户名和密码"}, 400

        user = User.query.filter_by(userName=data['userName']).first()

        if not user or not user.check_password(data['passWord']):
            return {"message": "用户名或密码错误"}, 401

        return user.to_dict(), 200

# @auth_ns.route('/register')
# class Rgister()
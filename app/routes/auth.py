from flask_restx import Namespace, Resource, fields
from app.models.user import User
from app import db

auth_ns = Namespace('auth', description='用户认证相关操作')

# 数据模型定义
user_model = auth_ns.model('User', {
    'id': fields.Integer(readOnly=True),
    'username': fields.String(required=True)
})

register_model = auth_ns.model('Register', {
    'username': fields.String(required=True),
    'password': fields.String(required=True)
})

login_model = auth_ns.model('Login', {
    'username': fields.String(required=True),
    'password': fields.String(required=True)
})


@auth_ns.route('/register')
class Register(Resource):
    @auth_ns.expect(register_model)
    @auth_ns.response(201, '注册成功', user_model)
    @auth_ns.response(400, '参数缺失')
    @auth_ns.response(409, '用户名已存在')
    def post(self):
        """用户注册"""
        data = auth_ns.payload

        if User.query.filter_by(username=data['username']).first():
            auth_ns.abort(409, '用户名已存在')

        user = User(username=data['username'])
        user.set_password(data['password'])

        db.session.add(user)
        db.session.commit()

        return user.to_dict(), 201


@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    @auth_ns.response(200, '登录成功', user_model)
    @auth_ns.response(400, '参数缺失')
    @auth_ns.response(401, '用户名或密码错误')
    def post(self):
        """用户登录"""
        data = auth_ns.payload

        user = User.query.filter_by(username=data['username']).first()
        if not user or not user.check_password(data['password']):
            auth_ns.abort(401, '用户名或密码错误')

        return user.to_dict(), 200
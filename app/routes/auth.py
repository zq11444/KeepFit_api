from flask_restx import Namespace, Resource, fields
from app.models.user import User
from app import db
from app.utils.security import generate_password_hash

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


# 注册请求数据模型（带确认密码字段）
register_model = auth_ns.model('Register', {
    'userName': fields.String(required=True, min_length=1, max_length=50, example="newuser"),
    'passWord': fields.String(required=True, min_length=1, max_length=100, example="securepassword123"),
    'confirmPassword': fields.String(required=True, example="securepassword123")  # 确认密码
})

# 注册请求数据模型（带确认密码字段）
register_model = auth_ns.model('Register', {
    'userName': fields.String(required=True, min_length=1, max_length=50, example="newuser"),
    'passWord': fields.String(required=True, min_length=1, max_length=100, example="securepassword123"),
    'confirmPassword': fields.String(required=True, example="securepassword123")  # 确认密码
})

@auth_ns.route('/register')
class Register(Resource):
    @auth_ns.expect(register_model)
    @auth_ns.response(201, '用户注册成功')
    @auth_ns.response(400, '参数无效')
    @auth_ns.response(409, '用户名已存在')
    def post(self):
        """
        用户注册接口
        - 用户名必须唯一
        - 密码需与确认密码一致
        - 密码会自动加密存储
        """
        data = auth_ns.payload

        # 验证密码一致性
        if data['passWord'] != data['confirmPassword']:
            return {"message": "两次输入的密码不一致"}, 400

        # 检查用户名是否已存在
        if User.query.filter_by(userName=data['userName']).first():
            return {"message": "用户名已被占用"}, 409

        try:
            # 创建新用户（密码自动加密）
            password_hash = generate_password_hash(data['passWord'])  # 加密密码
            new_user = User(
                userName=data['userName'],
                passWord=password_hash,  # 确保密码字段不为 None
                role=1  # 假设 role 是一个默认值
            )

            db.session.add(new_user)
            db.session.commit()

            # 返回创建的用户信息
            return {
                "message": "注册成功",
                "user": {
                    "uid": new_user.uid,
                    "userName": new_user.userName
                }
            }, 201

        except Exception as e:
            db.session.rollback()
            return {"message": f"注册失败: {str(e)}"}, 500
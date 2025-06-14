from flask_restx import Namespace, Resource, fields
from app.models.user import User
from app import db
from app.utils.security import generate_password_hash
from app.utils.security import check_password_hash

auth_ns = Namespace('auth', description='用户认证相关操作')

# 数据模型
login_model = auth_ns.model('Login', {
    'userName': fields.String(required=True, example="admin"),
    'passWord': fields.String(required=True, example="123456")
})

@auth_ns.route('/adminlogin')
class AdminLogin(Resource):
    @auth_ns.expect(login_model)
    @auth_ns.response(200, '管理员登录成功')
    @auth_ns.response(400, '用户名或密码为空')
    @auth_ns.response(401, '用户名或密码错误')
    @auth_ns.response(403, '无管理员权限')
    def post(self):
        """管理员登录"""
        data = auth_ns.payload
        # 输入验证
        if 'userName' not in data or not data['userName']:
            return {"message": "用户名为空"}, 400
        if 'passWord' not in data or not data['passWord']:
            return {"message": "密码为空"}, 400

        # 查询用户
        user = User.query.filter_by(userName=data['userName']).first()

        # 验证用户是否存在和密码是否正确
        if not user or not check_password_hash(user.passWord, data['passWord']):
            return {"message": "用户名或密码错误"}, 401

        # 验证是否为管理员(role=0)
        if user.role != "0":
            return {"message": "无管理员权限"}, 403

        return {
            "message": "管理员登录成功",
            "user": user.to_dict()
        }, 200

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        """哈希密码登录"""
        data = auth_ns.payload

        # 更详细的空值检查
        if 'userName' not in data or not data['userName']:
            return {"message": "用户名为空"}, 400
        if 'passWord' not in data or not data['passWord']:
            return {"message": "密码为空"}, 400

        user = User.query.filter_by(userName=data['userName']).first()

        if not user or not check_password_hash(user.passWord, data['passWord']):
            return {"message": "用户名或密码错误"}, 401

        return user.to_dict(), 200

# 注册请求数据模型（带确认密码字段）
register_model = auth_ns.model('Register', {
    'userName': fields.String(required=True, min_length=1, max_length=50, example="newuser"),
    'passWord': fields.String(required=True, min_length=1, max_length=100, example="securepassword123"),
    'confirmPassword': fields.String(required=True, example="securepassword123")  # 确认密码
})

@auth_ns.route('/register')
class Register(Resource):
    @auth_ns.expect(register_model)
    @auth_ns.response(200, '用户注册成功')
    @auth_ns.response(400, '参数无效')
    @auth_ns.response(409, '用户名已存在')
    def post(self):
        """
        用户注册接口
        - 用户名必须唯一
        - 密码需与确认密码一致
        - 用户名、密码、确认密码不能为空
        - 密码会自动加密存储
        """
        data = auth_ns.payload

        # 验证用户名是否为空
        if not data['userName']:
            return {"message": "用户名不能为空"}, 400

        # 验证密码和确认密码是否为空
        if not data['passWord'] or not data['confirmPassword']:
            return {"message": "密码和确认密码不能为空"}, 400

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
                    "uid": new_user.uid,  # 使用 uid 替代 id
                    "userName": new_user.userName
                }
            }, 200

        except Exception as e:
            db.session.rollback()
            return {"message": f"注册失败: {str(e)}"}, 500
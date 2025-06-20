from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_restx import Api
from flask_cors import CORS


db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
api = Api(
    title='KeepFit API',  # 文档标题
    version='1.0',                    # API版本
    description='KeepFit 后端接口文档',  # 详细描述
)

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object('config.Config')

    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    api.init_app(app)  # 将 Api 绑定到 Flask 应用

    # 注册 Namespace
    from app.routes.auth import auth_ns
    from app.routes.admindata import stats_ns
    from app.routes.admindata import manager_ns
    from app.routes.CoachVideoClass import Videos_ns
    from app.routes.CoachData import coaches_ns
    from app.routes.ReserveData import reserve_ns
    api.add_namespace(auth_ns, path='/api/auth')
    api.add_namespace(stats_ns, path='/api/status')
    api.add_namespace(manager_ns,path='/api/manager')
    api.add_namespace(Videos_ns,path='/api/videos')
    api.add_namespace(coaches_ns, path='/api/coaches')
    api.add_namespace(reserve_ns, path='/api/reserve')
    
    return app
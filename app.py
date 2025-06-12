from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from config import Config
import pymysql

# 初始化扩展
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    CORS(app)

    # 测试数据库连接
    with app.app_context():
        try:
            db.engine.connect()
            print("数据库连接成功!")
        except Exception as e:
            print("数据库连接失败:", str(e))
            raise e

    # 注册蓝图
    from routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    @app.route('/')
    def hello():
        return jsonify({'message': 'Welcome to the Flask API', 'status': 'running'})

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
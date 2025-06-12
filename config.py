import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # MySQL 配置 - 使用环境变量或默认值
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',
                                        'mysql+pymysql://root:password@localhost/flask_auth?charset=utf8mb4')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 280,
        'pool_pre_ping': True
    }

    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
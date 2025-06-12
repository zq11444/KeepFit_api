from app import bcrypt  # 从app包导入bcrypt

def generate_password_hash(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')

def check_password_hash(password_hash, password):
    return bcrypt.check_password_hash(password_hash, password)
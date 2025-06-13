# app/routes/CoachData.py
from flask_restx import Namespace, Resource, fields
from flask import jsonify
from app import db
from app.models.Coach import Coach

# 创建一个 Namespace
coaches_ns = Namespace('coaches', description='教练信息相关操作')

# 定义一个 Resource 类
@coaches_ns.route('/')
class CoachList(Resource):
    def get(self):
        """获取所有教练信息"""
        # 从数据库获取所有的教练数据
        coaches = Coach.query.all()
        # 将数据转换为字典列表
        coaches_list = [coach.to_dict() for coach in coaches]
        # 返回 JSON 响应
        return coaches_list

@coaches_ns.route('/<int:cid>/increase_publicity')
@coaches_ns.param('cid', '教练ID')
class IncreasePublicity(Resource):
    def patch(self, cid):
        """增加指定教练的publicity值"""
        coach = Coach.query.get_or_404(cid)
        coach.publicity += 1
        db.session.commit()
        return {'message': 'Publicity increased successfully', 'new_publicity': coach.publicity}

@coaches_ns.route('/<int:cid>/decrease_publicity')
@coaches_ns.param('cid', '教练ID')
class DecreasePublicity(Resource):
    def patch(self, cid):
        """减少指定教练的publicity值"""
        coach = Coach.query.get_or_404(cid)
        coach.publicity -= 1
        db.session.commit()
        return {'message': 'Publicity decreased successfully', 'new_publicity': coach.publicity}
# app/routes/CoachData.py
from flask_restx import Namespace, Resource, fields
from flask import jsonify,request
from app import db
from app.models.ReserveCoach import ReserveData

# 创建一个 Namespace
reserve_ns = Namespace('reserve', description='教练信息相关操作')

# 定义请求数据模型
reserve_model = reserve_ns.model('ReserveQuery', {
    'id': fields.Integer(required=True, description='要查询的ID')
})

@reserve_ns.route('/coach')
class ReserveList(Resource):
    @reserve_ns.expect(reserve_model)
    @reserve_ns.doc(responses={
        200: '成功',
        400: '请求参数错误',
        404: '未找到相关数据'
    })
    def post(self):
        """
        根据ID查询教练预约数据
        通过POST请求传入ID，返回reservetime_data中对应coach_id的所有数据
        """
        # 获取请求数据
        data = request.get_json()

        # 验证数据
        if not data or 'id' not in data:
            return {'message': '缺少ID参数'}, 400

        query_id = data['id']

        try:
            # 查询reservetime_data中coach_id等于传入ID的所有数据
            results = ReserveData.query.filter_by(coach_id=query_id).all()

            if not results:
                return {'message': f'未找到coach_id为{query_id}的数据'}, 404

            # 将结果转换为字典列表
            result_list = []
            for item in results:
                item_dict = {
                    'id': item.rid,
                    'coach_id': item.coach_id,
                    'address': item.address,
                    'deadline': item.deadline.strftime('%Y-%m-%d %H:%M:%S') if item.deadline else None,
                    # 添加其他需要的字段
                    'price':item.price
                }
                result_list.append(item_dict)

            return {'data': result_list}, 200

        except Exception as e:
            return {'message': f'查询失败: {str(e)}'}, 500
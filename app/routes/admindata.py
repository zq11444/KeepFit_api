from flask_restx import Namespace, Resource, fields
from app.models.user import User
from app import db
from flask import jsonify


# 创建命名空间
stats_ns = Namespace('stats', description='统计相关操作')



@stats_ns.route('/user_counts')
class UserCounts(Resource):
    def get(self):
        """获取用户、教练和课程数量统计"""
        try:
            # 计算普通用户总数（role为'1'的）
            total_users = User.query.filter_by(role='1').count()

            # 计算教练总数（从Coach表统计）
            # total_coaches = Coach.query.count()
            #
            # # 计算教练课程总数
            # total_coach_courses = CoachCourse.query.count()

            return {
                'code': 200,
                'message': 'Success',
                'data': {
                    'total_users': total_users,
                    # 'total_coaches': total_coaches,
                    # 'total_coach_courses': total_coach_courses
                }
            }
        except Exception as e:
            stats_ns.abort(500, f'服务器错误: {str(e)}')


manager_ns=Namespace('manager', description='管理用户相关操作')

user_model = manager_ns.model('User', {
    'uid': fields.Integer(description='用户ID'),
    'userName': fields.String(description='用户名'),
})

@manager_ns.route('/user_data')
class UserList(Resource):
    @manager_ns.marshal_list_with(user_model)
    def get(self):
        """获取所有用户列表"""
        return User.query.all()


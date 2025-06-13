from flask_restx import Namespace, Resource, fields, reqparse
from app.models.user import User
from app.models.CoachVideo import CoachVideo
from app.models.Coach import Coach
from app import db
from flask import jsonify


# 创建命名空间
stats_ns = Namespace('stats', description='统计相关操作')



@stats_ns.route('/total_counts')
class UserCounts(Resource):
    def get(self):
        """获取用户、教练和课程数量统计"""
        try:
            # 计算用户总数
            total_users = User.query.count()

            # 计算教练总数（从Coach表统计）
            total_coaches = Coach.query.count()
            #
            # 计算教练课程总数
            total_coach_video = CoachVideo.query.count()

            return {
                'code': 200,
                'message': 'Success',
                'data': {
                    'total_users': total_users,
                    'total_coaches': total_coaches,
                    'total_coach_courses': total_coach_video
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


@manager_ns.route('/user_data/<int:uid>')
class UserDelete(Resource):
    @manager_ns.marshal_with(user_model)
    def get(self, uid):  # 参数名改为uid
        """获取单个用户信息"""
        return User.query.get_or_404(uid)

    def delete(self, uid):  # 参数名改为uid
        """删除指定用户"""
        user = User.query.get_or_404(uid)

        try:
            db.session.delete(user)
            db.session.commit()
            return {'message': '用户删除成功'}, 200
        except Exception as e:
            db.session.rollback()
            manager_ns.abort(500, f'删除用户失败: {str(e)}')

    user_update_model = manager_ns.model('UserUpdate', {
        'userName': fields.String(required=True, description='用户名')
    })

    @manager_ns.expect(user_update_model)
    @manager_ns.marshal_with(user_model)  # 确保这个装饰器存在
    def put(self, uid):
        """更新用户名"""
        user = User.query.get_or_404(uid)
        data = manager_ns.payload

        try:
            user.userName = data['userName']
            db.session.commit()
            return user, 200  # 这里会自动被 user_model 序列化
        except Exception as e:
            db.session.rollback()
            manager_ns.abort(500, f'更新用户名失败: {str(e)}')

coach_model=manager_ns.model('Coach',{
    'cid':fields.Integer(description='教练ID'),
    'coachName':fields.String(description='教练名'),
    'coachBrief':fields.String(description='教练简介'),
    'coachTag':fields.String(description='教练标签'),
    'coachStar':fields.String(description='教练星级'),
    'publicity':fields.Integer(description='关注数'),
    'comment':fields.Integer(description='评论数')
})
coach_update_model = manager_ns.model('CoachUpdate', {
    'coachName': fields.String(required=True),
    'coachBrief': fields.String(required=True),
    'coachTag': fields.String(required=True),
    'coachStar': fields.String(required=True),
    'publicity': fields.Integer(required=True),
    'comment': fields.Integer(required=True)
})
coach_create_model = manager_ns.model('CoachCreate', {
    'coachName': fields.String(required=True, example="王教练"),
    'coachBrief': fields.String(required=True, example="国家级健身教练"),
    'coachTag': fields.String(required=True, example="增肌|减脂"),
    'coachStar': fields.String(
        required=True,
        description='星级必须是：一星教练/二星教练/三星教练',
        example="三星教练",
        enum=["一星教练", "二星教练", "三星教练"]
    ),
    'publicity': fields.Integer(default=0),
    'comment': fields.Integer(default=0)
})


@manager_ns.route('/coach')
class CoachCreateResource(Resource):
    @manager_ns.expect(coach_create_model)
    @manager_ns.marshal_with(coach_model)
    @manager_ns.response(201, '教练创建成功')
    @manager_ns.response(400, '参数校验失败')
    def post(self):
        """新增教练（星级为字符串格式）"""
        data = manager_ns.payload

        # 验证星级是否合法
        valid_stars = ["一星教练", "二星教练", "三星教练", "四星教练", "五星教练"]
        if data['coachStar'] not in valid_stars:
            manager_ns.abort(400, f"非法星级，必须是：{', '.join(valid_stars)}")

        try:
            new_coach = Coach(
                coachName=data['coachName'],
                coachBrief=data['coachBrief'],
                coachTag=data['coachTag'],
                coachStar=data['coachStar'],  # 直接存储字符串
                publicity=data.get('publicity', 0),
                comment=data.get('comment', 0)
            )

            db.session.add(new_coach)
            db.session.commit()
            return new_coach, 200
        except Exception as e:
            db.session.rollback()
            manager_ns.abort(500, f"创建教练失败: {str(e)}")


@manager_ns.route('/coach/<int:cid>')
class CoachResource(Resource):
    def delete(self, cid):
        """删除教练"""
        coach = Coach.query.get_or_404(cid)
        try:
            db.session.delete(coach)
            db.session.commit()
            return {"code": 200, "message": "教练删除成功"}, 200
        except Exception as e:
            db.session.rollback()
            manager_ns.abort(500, f"删除教练失败: {str(e)}")

    @manager_ns.expect(coach_update_model)
    @manager_ns.marshal_with(coach_model)
    def put(self, cid):
        """更新教练信息"""
        coach = Coach.query.get_or_404(cid)
        data = manager_ns.payload

        try:
            for field in data:
                if hasattr(coach, field):  # 防止更新不存在的字段
                    setattr(coach, field, data[field])
            db.session.commit()
            return coach, 200
        except Exception as e:
            db.session.rollback()
            manager_ns.abort(500, f"更新教练失败: {str(e)}")


coachvideo_create_model=manager_ns.model('coachvideo',{
    'videoid':fields.Integer(description=' 教练课程视频ID'),
    'coach_id':fields.Integer(description='教练ID'),
    'title':fields.String(description='视频标题'),
    'type':fields.String(description='视频标签'),
    'hard':fields.String(description='视频难度')
})


@manager_ns.route('/coachvideo')
class CoachVideoList(Resource):
    @manager_ns.expect(coachvideo_create_model)
    @manager_ns.marshal_with(coachvideo_create_model, code=200)
    def post(self):
        """创建新的教练视频"""
        args = video_parser.parse_args()

        new_video = CoachVideo(
            coach_id=args['coach_id'],
            title=args['title'],
            type=args.get('type', 'general'),
            hard=args.get('hard', 'medium'),
            seeCount='0'
        )

        db.session.add(new_video)
        db.session.commit()

        return new_video, 200

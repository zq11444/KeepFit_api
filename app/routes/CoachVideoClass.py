from flask_restx import Namespace, Resource, fields
from flask import jsonify
from app import db
from app.models.CoachVideo import CoachVideo

# 创建一个 Namespace
Videos_ns = Namespace('videos', description='教练视频相关操作')

# 定义一个 Resource 类
@Videos_ns.route('/')
class CoachVideosList(Resource):
    def get(self):
        """获取教练课程视频"""
        # 从数据库获取所有的教练视频数据
        videos = CoachVideo.query.all()
        # 将数据转换为字典列表
        video_list = [video.to_dict() for video in videos]
        # 返回 JSON 响应
        return jsonify(video_list)
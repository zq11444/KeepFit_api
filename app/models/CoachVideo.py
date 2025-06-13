from app import db

class CoachVideo(db.Model):
    __tablename__ = 'coachclassvideo_data'

    videoid = db.Column(db.Integer, primary_key=True)
    coach_id = db.Column(db.Integer)
    title = db.Column(db.String(1000))
    seeCount = db.Column(db.String(1000))
    pictureUrl = db.Column(db.String(1000))
    type = db.Column(db.String(1000))
    hard = db.Column(db.String(1000))

    def to_dict(self):
        return {
            'videoid': self.videoid,
            'coach_id': self.coach_id,
            'title': self.title,
            'seeCount': self.seeCount,
            'pictureUrl': self.pictureUrl,
            'type': self.type,
            'hard': self.hard
        }
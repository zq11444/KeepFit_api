# app/models/Coach.py
from app import db

class Coach(db.Model):
    __tablename__ = 'coach_data'

    cid = db.Column(db.Integer, primary_key=True)
    coachName = db.Column(db.String(1000))
    coachBrief = db.Column(db.String(1000))
    coachPictureUrl = db.Column(db.String(1000))
    coachTag = db.Column(db.Text)
    coachStar = db.Column(db.Integer)
    publicity = db.Column(db.Integer)
    comment = db.Column(db.Integer)

    def to_dict(self):
        return {
            'cid': self.cid,
            'coachName': self.coachName,
            'coachBrief': self.coachBrief,
            'coachPictureUrl': self.coachPictureUrl,
            'coachTag': self.coachTag,
            'coachStar': self.coachStar,
            'publicity': self.publicity,
            'comment': self.comment
        }
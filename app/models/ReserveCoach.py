# app/models/ReserveData.py
from app import db

class ReserveData(db.Model):
    __tablename__ = 'reservetime_data'

    rid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    coach_id = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(1000), nullable=False)
    deadline = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    price = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'rid': self.rid,
            'coach_id': self.coach_id,
            'address': self.address,
            'deadline': self.deadline,
            'price':self.price
        }
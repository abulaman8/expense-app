from . import db

class Entry(db.Model):
    __tablename__ ='entry'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    places = db.Column(db.String(500), nullable=False)
    distance = db.Column(db.Integer, nullable=False)
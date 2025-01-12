from app import db

class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    text = db.Column(db.String(100), nullable=False)

from sql import db
from datetime import datetime


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    flag = db.Column(db.Boolean, default=0)
    time = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return self.username


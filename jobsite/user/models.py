from sqlalchemy import Column, desc
from utils import get_current_time,STRING_LEN
from extensions import db

class User(db.Model):
    __tablename__ = 'user'


    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50),nullable=False)
    email = db.Column(db.String(50),unique=True,nullable=False)
    password = db.Column(db.String(50),nullable=False)
    employer = db.Column(db.Boolean,default=False)

    def __repr__(self):
        return '<User %r>' % self.username



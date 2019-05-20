from sqlalchemy import Column, desc,ForeignKey
from utils import get_current_time,STRING_LEN
from extensions import db
from constants import JOB_TYPE

class Employee(db.Model):

    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(STRING_LEN), nullable=False)
    academy = db.Column(db.String(STRING_LEN), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=get_current_time)
    user = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    

    def __repr__(self):
        return '<Employee %r>' % self.full_name

    
    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
           'id' : self.id,
           'full_name': self.full_name,
           'created_at': self.created_at,
           'academy': self.academy,
           'employee_user' : {
               "username" : self.employee_user.username,
               "email" : self.employee_user.email,
               "employer" : self.employee_user.employer,
           }
       }
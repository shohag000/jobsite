from sqlalchemy import Column, desc
from utils import get_current_time,STRING_LEN
from extensions import db
from constants import JOB_TYPE
#from user.models import User

class Company(db.Model):

    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(STRING_LEN), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=get_current_time)
    user = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    job = db.relationship("Job", backref="company_job")

    applied_job = db.relationship("Job_Company_Employee", backref="applied_job_company")
    

    def __repr__(self):
        return '<Company %r>' % self.company_name

    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
           'id' : self.id,
           'company_name': self.company_name,
           'created_at': self.created_at,
           'company_user' : {
               "username" : self.company_user.username,
               "email" : self.company_user.email,
               "employer" : self.company_user.employer,
           }
       }
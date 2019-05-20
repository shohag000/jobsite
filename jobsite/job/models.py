from sqlalchemy import Column, desc
from utils import get_current_time,STRING_LEN
from extensions import db
from constants import JOB_TYPE
from sqlalchemy import Enum
import enum
from employee import Employee
from company import Company

class MyEnum(enum.Enum):
    one = "full time"
    two = "part time"


association_table = db.Table('association',
    Column('job_company_employee_id', db.Integer, db.ForeignKey('job_company_employee.id')),
    Column('employee_id', db.Integer, db.ForeignKey('employee.id'))
)


class Job(db.Model):

    __tablename__ = 'job'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(STRING_LEN), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=get_current_time)
    updated_at = db.Column(db.DateTime)
    deadline = db.Column(db.DateTime)
    job_type = db.Column(Enum(MyEnum))
    is_hot_job = db.Column(db.Boolean, default=False, nullable=False)
    company = db.Column(db.Integer,db.ForeignKey("company.id"),nullable=False)


    applied_on = db.Column(db.Integer,db.ForeignKey("job_company_employee.id"),nullable=True)

    def __repr__(self):
        return '<Job %r>' % self.id

    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
           'id' : self.id,
           'title': self.title,
           'description': self.description,
           'created_at': self.created_at,
           'deadline': self.deadline,
           'job_type'  : self.job_type.value,
           'is_hot_job' : self.is_hot_job
       }

class Job_Company_Employee(db.Model):
    __tablename__ = 'job_company_employee'

    id = db.Column(db.Integer, primary_key=True)
    employees = db.relationship("Employee",secondary=association_table,backref="applied_job")


    company = db.Column(db.Integer,db.ForeignKey("company.id"),nullable=False)
    job = db.relationship("Job", backref="applied_details")



    

    
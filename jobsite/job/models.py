from sqlalchemy import Column, desc
from utils import get_current_time,STRING_LEN
from extensions import db
from constants import JOB_TYPE
from sqlalchemy import Enum
import enum

class MyEnum(enum.Enum):
    one = "full time"
    two = "part time"

class Job(db.Model):

    __tablename__ = 'job'

    id = Column(db.Integer, primary_key=True)
    description = Column(db.String(STRING_LEN), nullable=False, unique=True)
    created_at = Column(db.DateTime, nullable=False, default=get_current_time)
    updated_at = Column(db.DateTime)
    job_type = Column(Enum(MyEnum))
    is_hot_job = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return '<job %r>' % self.id

    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
           'id' : self.id,
           'description': self.description,
           'created_at': self.created_at,
           'job_type'  : self.job_type.value,
           'is_hot_job' : self.is_hot_job
       }
    

    
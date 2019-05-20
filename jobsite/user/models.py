from sqlalchemy import Column, desc,Integer,ForeignKey
from sqlalchemy.orm import relationship
from utils import get_current_time,STRING_LEN
from extensions import db
import datetime
import jwt
from settings import SECRET_KEY
from flask import jsonify
from employee.models import Employee
from company.models import Company


class User(db.Model):
    __tablename__ = 'user'


    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50),nullable=False)
    email = db.Column(db.String(50),unique=True,nullable=False)
    password = db.Column(db.String(50),nullable=False)
    employer = db.Column(db.Boolean,default=False)
    employee = db.relationship("Employee", uselist=False, backref="employee_user")
    company = db.relationship("Company", uselist=False, backref="company_user")

    def __repr__(self):
        return '<User %r>' % self.username

    '''
    Generates the Auth Token 
    :return: string
    '''
    def encode_auth_token(self, user_id):
        try:
            payload = {
               'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=30),
               'iat': datetime.datetime.utcnow(),
               'sub': user_id
            }
         
            return jwt.encode(
                payload,
                SECRET_KEY,
                #app.config['SECRET_KEY'],
                algorithm='HS256'
            )
        except Exception as e:
            return e  
    
    @staticmethod
    def decode_auth_token(request):

        token = None

        if "token" in request.headers:
            token = request.headers["token"]

        try:
            data = jwt.decode(token,SECRET_KEY,algorithms=['HS256'])
            user_id = data['sub']
            user = User.query.filter_by(id=user_id).first()
            return user
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Signature expired. Please log in again"})
        except :
            return jsonify({"message": "Token is invalid"})

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True  
        else:
            return False


class BlacklistToken(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)
   

       

       
      
      


from flask import Blueprint
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from extensions import db
from flask_restful import Resource, Api
import jwt
import datetime


# Create new user 
class CreateUser(Resource):
    def post(self):
        data = request.get_json()

        username = data["username"]
        email = data["email"]
        hashed_password = generate_password_hash(data["password"],method="sha256")
        
        new_user = User(username=username,email=email,password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        print(new_user)
        

        return jsonify({"message": "new user created"})


# Login

class Get_login(Resource):
   def post(self):
      auth = request.authorization 

      if not auth or auth.username or not auth.password:
         print("in first")
         return make_response("Could not verify",401,{"WWW-Authenticate" : 'Basic realm="Login required!"'})
      
      user = User.query.filter_by(username=auth.username).first()

      if not user:
         print("in second")
         return make_response("Could not verify",401,{"WWW-Authenticate" : 'Basic realm="Login required!"'})

      if check_password_hash(user.password,auth.password):
         print("in third")
         token = jwt.encode({"username" : user.username, "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15)},app.config['SECRET_KEY'])

         return jsonify({"token" : token.decode("UTF-8")})
      print("in last")
      return make_response("Could not verify",401,{"WWW-Authenticate" : 'Basic realm="Login required!"'})
      
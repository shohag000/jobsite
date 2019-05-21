from flask import Blueprint
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User,BlacklistToken
from extensions import db
from flask_restful import Resource, Api
import jwt
import datetime
import json
from json import JSONDecoder
from settings import SECRET_KEY
from decorator import token_required


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
   """
   User Login Resource
   """
   def post(self):
        # get the post data 
        post_data = request.get_json()
        try:
            # fetch the user data
            user = User.query.filter_by(
                email=post_data.get('email')
              ).first()

            if user and check_password_hash(user.password, post_data.get('password')):
                auth_token = user.encode_auth_token(user.id)
            if auth_token:
               responseObject = {
                    'status': 'success',
                    'message': 'Successfully logged in.',
                    'auth_token': auth_token.decode('UTF-8')
               }
               print(auth_token)
               return jsonify(responseObject)
               #return make_response(jsonify(responseObject)), 200
               #return ("hey in try")
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Try again'
            }
            return jsonify(responseObject)


# Check user type
class CheckUserType(Resource):
    @token_required
    def get(self):
        user = User.decode_auth_token(request)
        if user.employer:
            return jsonify({"is_employer": True})
        else:
            return jsonify({"is_employer": False})


# Logout
class Get_logout(Resource):
   # Logout user
   @token_required 
   def post(self):
      # get the post data
      user= User.decode_auth_token(request)
      token = request.headers["token"]
      print (user)
      if isinstance(user.id,int):
         blacklist_token = BlacklistToken(token=token)
         try:
            # insert the token
            db.session.add(blacklist_token)
            db.session.commit()
            responseObject = {
               'status': 'success',
               'message': 'Successfully logged out.'
            }
            return jsonify(responseObject)
         except Exception as e:
            responseObject = {
               'status': 'fail',
               'message': e
            }
            return jsonify(responseObject)
      else:
         responseObject = {
               'status': 'fail',
               'message': 'Something is wrong.'
         }
         return jsonify(responseObject)

      

# hello world
class Hello(Resource):
   @token_required
   def post(self):
      user= User.decode_auth_token(request)
      print(user)
      print("hello")
      return ("hello from Hello class after token check")
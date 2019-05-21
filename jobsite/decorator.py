from functools import wraps
from flask import Flask, request, jsonify, make_response
from settings import SECRET_KEY
from user.models import User
import jwt

def token_required(f):
   @wraps(f)
   def decorated(*args,**kwargs):

      token = None

      try:
         token = request.headers['token']
      except:
         return jsonify({"message" : 'token is missing'})

      is_black_listed = User.check_blacklist(token)
      if is_black_listed:
         return jsonify({"message" : 'Login again'})
      try:
         data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
         #data = jwt.decode(token,SECRET_KEY)
      except Exception as inst:
         print(inst)
         return jsonify({"message" : 'token is invalid'})

      return f(*args,**kwargs)
   return decorated
from flask import Blueprint,render_template, url_for, flash, redirect, request
from .models import Company
from extensions import db
from flask import jsonify,request
from flask_restful import Resource, Api
from user.models import User
from decorator import token_required

# Get all job
class Allcompany(Resource):
    def get(self):
        #usr= User.query.filter_by(id=1).first()
        #emp= Employee(full_name="Mr. y",academy="y",user=usr)
        #db.session.add(emp)
        #db.session.commit()
        #employees= Employee.query.all()
        #return jsonify([employee.serialize for employee in employees])
        company = Company.query.filter_by(id=1).first()
        print (company.company_user)
        return jsonify({"employee" : "hey"})
        #return ("hello")

#Create Company profile
class CreateCompany(Resource):
    @token_required
    def post(self):
        data = request.get_json()

        company_name = data["company_name"]
        user = User.decode_auth_token(request)
        if company_name:
            company = Company(company_name=company_name,user=user.id)
            db.session.add(company)
            db.session.commit()
            print(company)
        

        return jsonify({"message": "new company created"})
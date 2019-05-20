from flask import Blueprint,render_template, url_for, flash, redirect, request
from .models import Employee
from extensions import db
from flask import jsonify,request
from flask_restful import Resource, Api
from user.models import User

# Get all job
class Allemployee(Resource):
    def get(self):
        #usr= User.query.filter_by(id=1).first()
        emp= Employee(full_name="Mr. x",academy="x",user=1)
        db.session.add(emp)
        db.session.commit()
        employees= Employee.query.all()
        return jsonify([employee.serialize for employee in employees])
        #employee = Employee.query.filter_by(id=1).first()
        #print (employee.employee_user)
        #return jsonify({"employee" : "hey"})
        #return ("hello")
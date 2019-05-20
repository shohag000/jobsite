from flask import Blueprint,render_template, url_for, flash, redirect, request
from .models import Job,Job_Company_Employee
from extensions import db
from flask import jsonify,request
from flask_restful import Resource, Api
from user.models import User
from decorator import token_required
from company import Company
from employee.models import Employee


#Get job by Job id
class GetSingleJob(Resource):
    def get(self,id):
        print(id)
        job = Job.query.filter_by(id=id).first()
        print(job)
        if job:
            return jsonify(job.serialize)

        else:
            print("somethis is wrong")
            return (" Something is wrong ")


#Search job by Job title
class SearchJob(Resource):
    def post(self):
        data = request.get_json()
        title = data['title']
        jobs = Job.query.filter_by(title=title)
        if jobs:
            return jsonify([job.serialize for job in jobs])

        else:
            print("somethis is wrong")
            return (" Something is wrong ")



# Get all job
class Alljob(Resource):
    def get(self):
        jobs= Job.query.all()
        return jsonify([job.serialize for job in jobs])

# Create new job 
class CreateJob(Resource):
    @token_required
    def post(self):
        user = User.decode_auth_token(request)
        print(user)
        try:
            company= Company.query.filter_by(user=user.id).first()
            print(company)
            if company:
                data = request.get_json()
                title = data["title"]
                description = data["description"]
                is_hot_job = data["is_hot_job"]
                job_type = data["job_type"]
                print("got all json data")

            if title and description and is_hot_job and job_type:
                job=Job(title=title,description=description,job_type=job_type,is_hot_job=is_hot_job,company=company.id)
                print("all is okay")
            
                db.session.add(job)
                db.session.commit()
                print(job)
                thisJob= Job.query.filter_by(id=job.id).first()
                print(thisJob)
                return jsonify([thisJob.serialize])

        except :
            return jsonify({"message": "something is missing"})


# delete or edit job 
class Edit_or_Delete(Resource):
    def delete(self):
        data = request.get_json()
        id=data["id"]
        try:
            job=Job.query.filter_by(id=id).one()   
            db.session.delete(job)
            db.session.commit()
            return {"message": "successfully deleted"}
        except:
            return {"message":"Data not found"}    

    def put(self):
        data = request.get_json()
        id=data["id"]
        description= data["description"]
        try:
            job=Job.query.filter_by(id=id).one()   
            job.description=description
            db.session.commit()

            thisJob= Job.query.filter_by(id=id).one()
            return jsonify([thisJob.serialize])
        except:
            return {"message":"Data not found"}  


# Apply job
class ApplyJob(Resource):
    def get(self):
        employee = Employee.query.filter_by(id=1).first()
        job = Job.query.filter_by(id=1).first()
        company_id = job.company
        applied_job = Job_Company_Employee(company=company_id)
        applied_job.employees.append(employee)

        db.session.add(applied_job)
        db.session.commit()



        return ("Successfully applied job")

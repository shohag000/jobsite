from flask import Blueprint,render_template, url_for, flash, redirect, request
from .forms import JobUploadForm
from .models import Job
from extensions import db
from flask import jsonify,request
from flask_restful import Resource, Api




# Get all job
class Alljob(Resource):
    def get(self):
        jobs= Job.query.all()
        return jsonify([job.serialize for job in jobs])

# Create new job 
class CreateJob(Resource):
    def post(self):
        data = request.get_json()
        description = data["description"]
        is_hot_job = data["is_hot_job"]
        job_type = data["job_type"]
        print(description)
        
        job=Job(description=description,job_type=job_type,is_hot_job=is_hot_job)
        db.session.add(job)
        db.session.commit()
        thisJob= Job.query.filter_by(id=job.id).one()



        return jsonify([thisJob.serialize])


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

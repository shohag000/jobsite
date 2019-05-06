from flask import Flask,Blueprint
#from job.views import job_app
#from user.views import user_app
from extensions import db
from flask_restful import Resource, Api
from settings import SECRET_KEY

#new import
from job.views import Alljob,CreateJob,Edit_or_Delete
from user.views import CreateUser,Get_login,Hello,Get_logout


#new code
api_job_bp  = Blueprint('job',__name__)
api_user_bp = Blueprint('user',__name__)
#routes
api= Api(api_job_bp)
api_user = Api(api_user_bp)


api.add_resource(Alljob,'/jobs')
api.add_resource(CreateJob,"/create")
api.add_resource(Edit_or_Delete,"/editOrDelete")

api_user.add_resource(CreateUser,"/create")
api_user.add_resource(Get_login,"/login")
api_user.add_resource(Get_logout,"/logout")
api_user.add_resource(Hello,"/hello")

app = Flask(__name__)


app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"

with app.app_context():
    db.init_app(app)
    db.create_all()
    db.session.commit()


#new code
app.register_blueprint(api_job_bp,url_prefix='/job')
app.register_blueprint(api_user_bp,url_prefix='/user')

if __name__ == '__main__':
   app.run(debug = True)
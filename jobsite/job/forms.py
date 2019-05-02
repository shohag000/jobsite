from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from job.models import Job

class JobUploadForm(FlaskForm):
    description = StringField('Descriptions')
    job_type = StringField('job_type')
    is_hot_job = BooleanField("Is this hot job?")
    submit = SubmitField('Submit')
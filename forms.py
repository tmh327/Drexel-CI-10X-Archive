from genericpath import exists
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, ValidationError, Length
import sqlite3
class LoginForm(FlaskForm):
  email = StringField('Email',validators=[DataRequired(),Email()])
  password = PasswordField('Password',validators=[DataRequired(), Length(min=8, max=20)])
  remember = BooleanField('Remember Me')
  submit = SubmitField('Login')
  def validate_email(self, email):
    conn = sqlite3.connect('ci_archive.db')
    curs = conn.cursor()
    curs.execute("SELECT email FROM users where email = (?)",[email.data])
    valemail = curs.fetchone()
    if valemail is None:
      raise ValidationError('This Email ID is not registered. Please register before login')

class RegisterForm(FlaskForm):
  conn = sqlite3.connect('ci_archive.db')
  curs = conn.cursor()
  curs.execute("SELECT role_id, role_description FROM roles")
  role_lists = curs.fetchall()

  email = StringField('Email',validators=[DataRequired(),Email()])
  password = PasswordField('Password',validators=[DataRequired(), Length(min=8, max=20)])
  name = StringField('Name',validators=[DataRequired()])
  role_id = SelectField('Role', choices=role_lists)
  remember = BooleanField('Remember Me')
  submit = SubmitField('Register')
  def validate_email(self, email):
    conn = sqlite3.connect('ci_archive.db')
    curs = conn.cursor()
    curs.execute("SELECT email FROM users where email = (?)",[email.data])
    valemail = curs.fetchone()
    if valemail is not None:
      raise ValidationError('An account with this email already exists!')

class ProjectForm(FlaskForm):
  def validate_project_name(academic_year, lab_number):
    def _validate_project_name(form, field):
      conn = sqlite3.connect('ci_archive.db')
      curs = conn.cursor()
      curs.execute("SELECT project_id FROM projects where (academic_year, lab_number, project_name) = (?, ?, ?)", [form.academic_year.data, form.lab_number.data, field.data])
      project = curs.fetchone()
      if project is not None:
        raise ValidationError('A project with in this academic year and this lab with this project name already exists!')
    return _validate_project_name

  academic_year = IntegerField('Academic Year',validators=[DataRequired(message='*Required')])
  lab_number = IntegerField('Lab Number',validators=[DataRequired(message='*Required')])
  project_name = StringField('Project Name',validators=[DataRequired(message='*Projects in the same lab from the same academic year must have unique name'), validate_project_name(academic_year, lab_number)])
  project_description = StringField('Project Description',validators=[DataRequired(message='*Required')])
  submit = SubmitField('Create')

class ProfileForm(FlaskForm):
  name = StringField('Name', validators= [DataRequired()])
  email = StringField('Email',validators=[DataRequired(),Email()])
  password = PasswordField('Password',validators=[DataRequired(), Length(min=8, max=20)])
  submit = SubmitField('Save')

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import sqlite3
class LoginForm(FlaskForm):
  email = StringField('Email',validators=[DataRequired(),Email()])
  password = PasswordField('Password',validators=[DataRequired()])
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
  password = PasswordField('Password',validators=[DataRequired()])
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
from flask import Flask, render_template, url_for, flash, request, redirect, Response, session
import sqlite3
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from forms import LoginForm, ProjectForm, RegisterForm, ProfileForm

app = Flask(__name__, static_folder='public', static_url_path='')
app.config['SECRET_KEY'] = 'TrangHoang'
app.debug=False

messages = [{'title': 'Message One',
             'content': 'Message One Content'},
            {'title': 'Message Two',
             'content': 'Message Two Content'}
            ]

login_manager = LoginManager(app)
login_manager.login_view = "login"
class User(UserMixin):
    def __init__(self, id, email, password, name):
         self.id = str(id)
         self.email = email
         self.name = name
         self.password = password
         self.authenticated = False
    def is_active(self):
         return self.is_active()
    def is_anonymous(self):
         return False
    def is_authenticated(self):
         return True
    def is_active(self):
         return True
    def get_id(self):
         return self.id

@login_manager.user_loader
def load_user(user_id):
   conn = sqlite3.connect('ci_archive.db')
   curs = conn.cursor()
   curs.execute("SELECT * from users where user_id = (?)",[user_id])
   lu = curs.fetchone()
   if lu is None:
      return None
   else:
      return User(int(lu[0]), lu[1], lu[2], lu[3])

@app.route("/login", methods=['GET','POST'])
def login():
     if current_user.is_authenticated:
          return redirect(url_for('main'))
     form = LoginForm()
     if form.validate_on_submit():
          conn = sqlite3.connect('ci_archive.db')
          curs = conn.cursor()
          curs.execute("SELECT * FROM users where email = (?)",    [form.email.data])
          user = list(curs.fetchone())
          Us = load_user(user[0])
          if form.email.data == Us.email and form.password.data == Us.password:
               login_user(Us, remember=form.remember.data)
               Umail = list({form.email.data})[0].split('@')[0]
               #flash('Logged in successfully '+Umail)
               return redirect(url_for('main'))
          else:
               flash('Login Unsuccessfull.')
     return render_template('login.html',title='Login', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    if session.get('was_once_logged_in'):
        # prevent flashing automatically logged out message
        del session['was_once_logged_in']
    flash('You have successfully logged yourself out.')
    return redirect('/login')

@app.route('/register', methods=['GET','POST'])
def register():
     form = RegisterForm()
     if form.validate_on_submit():
          conn = sqlite3.connect('ci_archive.db')
          curs = conn.cursor()
          Umail = list({form.email.data})[0].split('@')[0]
          curs.execute("INSERT INTO users (email, password, name, role_id) VALUES (?, ?, ?, ?)",    [form.email.data, form.password.data, form.name.data, form.role_id.data])
          curs.connection.commit()
          flash('You have successfully registered '+ Umail + '!')
     return render_template('register.html', title='Register', form=form)

@app.route('/profile')
@login_required
def profile():
     return render_template('profile.html', user=current_user, title='Profile')

@app.route('/edit_profile')
@login_required
def edit_profile():
     form = ProfileForm()
     if form.validate_on_submit():
          pass
     elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.password.data = current_user.password
     return render_template('edit_profile.html', user=current_user, title='Edit Profile', form=form)

@app.route('/home')
@login_required
def home():
    return 'You are logged in as {0}.'.format(app.current_user.id)

@app.route('/student_home')
@login_required
def student_home():
    return render_template('student_home.html')

@app.route("/")
def main():
     if current_user.is_authenticated:
          conn = sqlite3.connect('ci_archive.db')
          curs = conn.cursor()
          curs.execute("SELECT * FROM projects where user_id = ?", [current_user.id])
          #curs.execute("SELECT academic_year, lab_number, project_name, project_description FROM projects")
          projects = list(curs.fetchall())
          return render_template('index.html', title='DREXEL CI10X ARCHIVE', projects=projects)
     else:
          return render_template('index.html', title='DREXEL CI10X ARCHIVE')
@app.route('/project/<int:id>', methods=('GET', 'POST'))
def project(id):
     conn = sqlite3.connect('ci_archive.db')
     curs = conn.cursor()
     curs.execute("SELECT project_id, academic_year, lab_number, project_name, project_description FROM projects where project_id = (?)",[id])
     project = curs.fetchone()
     return render_template('project.html', project=project)

@app.route('/projects')
def projects():
     conn = sqlite3.connect('ci_archive.db')
     curs = conn.cursor()
     curs.execute("SELECT * FROM projects")
     #curs.execute("SELECT academic_year, lab_number, project_name, project_description FROM projects")
     projects = list(curs.fetchall())
     return render_template('projects.html', projects=projects)

@app.route('/create/', methods=('GET', 'POST'))
@login_required
def create():
     form = ProjectForm()
     if form.validate_on_submit():
          conn = sqlite3.connect('ci_archive.db')
          curs = conn.cursor()
          curs.execute("INSERT INTO projects (academic_year, lab_number, project_name, project_description, user_id) VALUES (?, ?, ?, ?, ?)",    [form.academic_year.data, form.lab_number.data, form.project_name.data, form.project_description.data, current_user.id])
          curs.connection.commit()
          flash('You have successfully added a new project '+ form.project_name.data + '!')
     return render_template('create.html', title='Create New Project', form=form)

if __name__ == "__main__":
    app.run(host='127.0.0.1',port=8080,threaded=True) 
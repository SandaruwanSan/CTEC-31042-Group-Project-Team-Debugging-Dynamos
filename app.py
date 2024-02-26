from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError
from werkzeug.security import generate_password_hash
import os
from flask import redirect, url_for
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask import send_from_directory
from flask import current_app

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SANRIDER-Debudding_Dynamose'  # Change this to a random value
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///internship.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
db = SQLAlchemy(app)
login_manager = LoginManager(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    # Check if the user ID is for a User
    user = User.query.get(int(user_id))
    if user:
        return user

    # If not found, check if the user ID is for an Admin
    admin = Admin.query.get(int(user_id))
    if admin:
        return admin

    # If neither User nor Admin is found, return None
    return None


class Internship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    poster_path = db.Column(db.String(255), nullable=False)

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        existing_user = User.query.filter_by(username=username.data).first()
        if existing_user:
            raise ValidationError('That username is already taken. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class AdminRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        existing_admin = Admin.query.filter_by(username=username.data).first()
        if existing_admin:
            raise ValidationError('That username is already taken. Please choose a different one.')

class AdminLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@app.route('/admin/register', methods=['GET', 'POST'])
def admin_register():
    form = AdminRegistrationForm()
    if form.validate_on_submit():        
        new_admin = Admin(username=form.username.data, password=form.password.data)
        db.session.add(new_admin)
        db.session.commit()
        return redirect(url_for('admin_login'))
    return render_template('admin_register.html', form=form)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin and admin.password == form.password.data:
            login_user(admin)
            return redirect(url_for('available_internships'))
    return render_template('admin_login.html', form=form)



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():        
        new_user = User(username=form.username.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('internships'))
        else:
            return "Wrong User Name or Password"
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('register'))

@app.route('/internships')
@login_required
def internships():
    internships = Internship.query.all()
    return render_template('internships.html', internships=internships)

@app.route('/post_internship', methods=['GET', 'POST'])
def post_internship():
    if request.method == 'POST':
        company_name = request.form['company_name']
        description = request.form['description']
        poster = request.files['poster']
        
        # Save poster to uploads folder
        poster_path = os.path.join('uploads/'+ poster.filename)
        absolute_path = os.path.join('static/uploads/'+ poster.filename)
        poster.save(absolute_path)

        # Save data to database
        new_internship = Internship(company_name=company_name, description=description, poster_path=poster_path)
        db.session.add(new_internship)
        db.session.commit()

        return render_template('adddone.html')

    return render_template('post_internship.html')

@app.route('/internship/delete/<int:internship_id>', methods=['GET'])
@login_required
def confirm_delete_internship(internship_id):
    return render_template('delete_internship.html', internship_id=internship_id)

@app.route('/internship/delete/<int:internship_id>', methods=['POST'])
@login_required
def delete_internship(internship_id):
    internship = Internship.query.get(internship_id)
    if internship:
        db.session.delete(internship)
        db.session.commit()
    return redirect(url_for('available_internships'))

@app.route('/available_internships')
@login_required
def available_internships():
    internships = Internship.query.all()
    return render_template('available_internships.html', internships=internships)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')


@app.route('/')
def index():
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User

from werkzeug.security import generate_password_hash, check_password_hash
from . import db
#import mysql.connector
from flask_login import login_user, login_required, logout_user, current_user
#from flask_wtf import FlaskForm
#from wtforms import StringField, SubmitField, PasswordField, FormField
#from wtforms.validators import DataRequired

auth = Blueprint('authentication', __name__)

# new_db = mysql.connector.connect(host="localhost", user="root", passwd="$C0de1sco0L!", database="testdatabase")
# mycursor = new_db.cursor()


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        # mycursor.execute("SELECT permissions FROM Users WHERE email = 'email'")
        if user:
            if check_password_hash(user.password, password):
                if user.permissions == 0:
                    flash('Admin Login Successful!', category='success')
                    login_user(user, remember=True)
                    print("Permissions = ", user.permissions, ". UserID = ", user.id)
                    return redirect(url_for('views.admin_dash'))
                elif user.permissions == 1:
                    flash('Student Login Successful!', category='success')
                    login_user(user, remember=True)
                    print("Permissions = ", user.permissions, ". UserID = ", id)
                    return redirect(url_for('views.student_dash'))
                elif user.permissions == 2:
                    flash('Faculty Login Successful!', category='success')
                    login_user(user, remember=True)
                    print("Permissions = ", user.permissions, ". UserID = ", id)
                    return redirect(url_for('views.faculty_dash'))
                elif user.permissions == 3:
                    flash('Parent/Guardian Login Successful!', category='success')
                    login_user(user, remember=True)
                    print("Permissions = ", user.permissions, ". UserID = ", id)
                    return redirect(url_for('views.parent_guardian_dash'))
                else:
                    flash('Invalid permissions, please call an administrator.', category='error')
                    print("Permissions = ", user.permissions, ". UserID = ", user.id, "email = ", user.email)
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('authentication.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        address = request.form.get('address')
        city = request.form.get('city')
        zip_code = request.form.get('zip_code')
        state = request.form.get('state')
        email = request.form.get('email')
        phone_number = request.form.get('phone')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        permissions = None #request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(last_name) < 2:
            flash('Last name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        
        """
        If all of the above checks pass, then we want to create the new user.
        We are adding this new user to our database, so we need to define all of the 
        fields that we made in the models.py database.
        """

        if request.form.get('student_box') is not None:
            permissions=request.form.get('student_box')
            new_user = User(first_name=first_name, last_name=last_name,address=address, city=city, zip_code=zip_code, state=state, email=email, phone_number=phone_number, password=generate_password_hash(password1, method='sha256'), permissions=permissions)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created! Welcome New Student!', category='success')
            return redirect(url_for('views.student_dash'))
        elif request.form.get('faculty_box') is not None:
            permissions=request.form.get('faculty_box')
            new_user = User(first_name=first_name, last_name=last_name,address=address, city=city, zip_code=zip_code, state=state, email=email, phone_number=phone_number, password=generate_password_hash(password1, method='sha256'), permissions=permissions)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created! Welcome New Faculty Member!', category='success')
            return redirect(url_for('views.faculty_dash'))
        elif request.form.get('parent_box') is not None:
            permissions=request.form.get('parent_box')
            new_user = User(first_name=first_name, last_name=last_name,address=address, city=city, zip_code=zip_code, state=state, email=email, phone_number=phone_number, password=generate_password_hash(password1, method='sha256'), permissions=permissions)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created! Welcome Parents and Family!', category='success')
            return redirect(url_for('views.parent_guardian_dash'))
        elif request.form.get('admin_box') is not None:
            permissions=request.form.get('admin_box')
            new_user = User(first_name=first_name, last_name=last_name,address=address, city=city, zip_code=zip_code, state=state, email=email, phone_number=phone_number, password=generate_password_hash(password1, method='sha256'), permissions=permissions)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created! Welcome New Admin!', category='success')
            return redirect(url_for('views.admin_dash'))

    return render_template("sign_up.html", user=current_user)

@auth.route('/admin')
def admin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("admin.html", user=current_user)

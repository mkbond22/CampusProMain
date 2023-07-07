"""
FILE TO STORE THE ROUTES/DIFFERENT PAGES THE USER CAN NAVIGATE TO.
"""

from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from .models import User, Course
from sqlalchemy.inspection import inspect
from sqlalchemy import MetaData
from . import db
import json

views = Blueprint('views', __name__)

# ROUTE FOR THE HOMEPAGE
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():

    if request.method == 'POST': 
        course = request.form.get('course')#Gets the course from the HTML form         #########################################################
        course_id = request.form.get('course_id')
        teacher = request.form.get('teacher')
        year = request.form.get('year')

        new_course = Course(id=course_id, teacher=teacher, description=course, year=year, user_id=current_user.id)  #providing the schema for the course
        db.session.add(new_course) #adding the note to the database 
        db.session.commit()
        flash('Course Added Successfully!', category='success')
    
    return render_template("home.html", user=current_user)


@views.route('/delete-course', methods=['POST'])
def delete_course():  
    course = json.loads(request.description) # this function expects a JSON from the INDEX.js file 
    courseId = course['courseId']
    course = Course.query.get(courseId)
    if course:
        if course.user_id == current_user.id:
            db.session.delete(course)
            db.session.commit()

    return jsonify({})


################################     Student Pages     ################################
@views.route('/student')
def student():
    return render_template("_template_student.html")


@views.route('/student/dash')
@login_required
def student_dash():
    return render_template("stu_dashboard.html")


@views.route('/student/grades')
@login_required
def student_grades():
    return render_template("stu_grades.html")


################################     Admin Pages     ################################
@views.route('_template_admin.html')
@login_required
def admin():
    return render_template("admin.html")


@views.route('/admin/dash')
@login_required
def admin_dash():
    return render_template("admin_dashboard.html")


@views.route('/admin/manage_users')
@login_required
def admin_manage_users():
    users = User.query.all()
    return render_template("admin_manage_users.html", users=users)


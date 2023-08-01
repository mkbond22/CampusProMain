"""
FILE TO STORE THE ROUTES/DIFFERENT PAGES THE USER CAN NAVIGATE TO.
"""

from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from .models import User, Course, Assignment, Submission, user_course
from .auth import *
from sqlalchemy import MetaData
from . import db
import json

views = Blueprint('views', __name__)

# ROUTE FOR THE HOMEPAGE
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if current_user.permissions == 0:
        return render_template("admin_dashboard.html")
    elif current_user.permissions == 1:
        return redirect(url_for('views.student_dash'))
    elif current_user.permissions == 2:
        return redirect(url_for('views.faculty_dash'))
    elif current_user.permissions == 3:
        return redirect(url_for('views.parent_guardian_dash'))
    return render_template("home.html")


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


@views.route('/user-profile/')
@login_required
def user_profile():
    return render_template("user_profile.html", current_user=current_user)


@views.route('/faculty-directory/')
@login_required
def faculty_directory():
    return render_template("faculty_directory.html", current_user=current_user)


################################     Student Pages     ################################
@views.route('/student')
def student():
    return render_template("_template_student.html")


@views.route('/student/dash', methods=['GET', 'POST'])
@login_required
def student_dash():
    id = current_user.id
    user = User.query.filter(User.id == id).first()

    #Get the courses that a user is currently enrolled in
    enrolled_courses = user.current_courses

    course = Course.query.filter(Course.id == 1).first()
    courseCode = course.course_code
    courseName = course.course_name

    #Get all the students that are enrolled in a course
    enrolled_students = course.enrolled_students

    users = User.query.all()
    return render_template("stu_dashboard.html", current_user=current_user, users=users, course=course, enrolled_courses=enrolled_courses, enrolled_students=enrolled_students)


@views.route('/student/grades', methods=['GET', 'POST'])
@login_required
def student_grades():
    return render_template("stu_grades.html")


@views.route('/student/courses', methods=['GET', 'POST'])
@login_required
def student_courses():
    return render_template("stu_courses.html", current_user=current_user)


@views.route('/student/course-register', methods=['GET', 'POST'])
@login_required
def student_course_registration():
    id = current_user.id

    #Get list of course options to display to student
    courses = Course.query.all()

    #Get User object for current student
    user = User.query.filter(User.id == id).first()

    if request.method == 'POST':
        courseCode = request.form.get('register')
        course = Course.query.filter(Course.course_code == courseCode).first()
        print(course)

        user.current_courses.append(course)
        db.session.commit()
    
    flash('Course Added Successfully!', category='success')
    return render_template("stu_course_registration.html", current_user=current_user, courses=courses)


################################     Admin Pages     ################################
@views.route('/admin')
@login_required
def admin():
    id = current_user.id
    user = User.query.get(id)
    return render_template("_template_admin.html", user=user)


@views.route('/admin/dash')
@login_required
def admin_dash():
    if current_user.permissions == 0:
        return render_template("admin_dashboard.html", current_user=current_user)
    else:
        if current_user.permissions == 1:
            flash('Invalid permissions. Must be admin to access this page', category='error')
            return redirect(url_for('views.student_dash'))
        elif current_user.permissions == 2:
            flash('Invalid permissions. Must be admin to access this page', category='error')
            return redirect(url_for('views.faculty_dash'))
        elif current_user.permissions == 3:
            flash('Invalid permissions. Must be admin to access this page', category='error')
            return redirect(url_for('views.parent_guardian_dash'))
        else:
            flash('Invalid permissions. Please contact an administrator', category='error')
            logout()
            


@views.route('/admin/manage_users')
@login_required
def admin_manage_users():

    id = current_user.id
    user = User.query.filter(User.id == id).first()

    #Get the courses that a user is currently enrolled in
    enrolled_courses = user.current_courses

    course = Course.query.filter(Course.id == 1).first()
    courseCode = course.course_code
    courseName = course.course_name

    #Get all the students that are enrolled in a course
    enrolled_students = course.enrolled_students

    users = User.query.all()
    return render_template("admin_manage_users.html", current_user=current_user, users=users, course=course, enrolled_courses=enrolled_courses, enrolled_students=enrolled_students)


@views.route('/admin/manage_courses')
@login_required
def admin_manage_courses():
    courses = Course.query.all()
    return render_template("admin_manage_courses.html", current_user=current_user, courses=courses)


################################     Faculty Pages     ################################
@views.route('/faculty')
@login_required
def faculty():
    return render_template("_template_faculty.html", current_user=current_user)


@views.route('/faculty/teacher-dash')
@login_required
def faculty_dash():
    return render_template("teach_dashboard.html", current_user=current_user)


@views.route('/faculty/teacher-courses')
@login_required
def faculty_courses():
    return render_template("teach_courses.html", current_user=current_user)


################################     Parent/Guardian Pages     ################################
@views.route('/guardian')
@login_required
def parent_guardian():
    return render_template("_template_parent.html", current_user=current_user)


@views.route('/parent-guardian/dash')
@login_required
def parent_guardian_dash():
    return render_template("par-guard_dashboard.html", current_user=current_user)


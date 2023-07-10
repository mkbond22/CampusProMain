
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import insert
import enum


#######################################################################
"""
USER REQUIREMENTS:
 - FirstName
 - LastName
 - Email
 - ContactNumber
 - Password
 When someone signs up, we need to have them read a user agreement and check a box to continue.
 After that is done, a uniqueID should be automatically generated for the user and 
 an automated email should be sent to the user's email with that uniqueID.

 USER TYPES: 0=ADMIN, 1=STUDENT, 2=TEACHER, 3=PARENT
"""
"""
USER TABLE COLUMNS:
ID | First Name | Last Name | Email | Phone Number | Password | Permissions ENUM('0', '1', '2', '3')

"CREATE TABLE Users (id int PRIMARY KEY AUTO_INCREMENT, 
                    first_name VARCHAR(50), 
                    last_name VARCHAR(50), 
                    email VARCHAR(100), 
                    phone_number int, 
                    passwd VARCHAR(50), 
                    permissions ENUM('0', '1', '2', '3')
                    )"

"""
#######################################################################

"""
        user_list = [("Tyler", "Selby", "t.selby@cpro.edu", 8598018793, "123pass", 0),
            ("Megan", "Bond", "m.bond@cpro.edu", 5734292338, "456pass", 0),
            ("Jim", "Beam", "j.beam@cpro.edu", 8593751289, "pass456", 1),
            ("Mary", "Poppins", "m.poppins@cpro.edu", 5734814889, "456pass", 1),
            ("Jon", "Snow", "j.snow@cpro.edu", 8591230956, "p123ass", 1),
            ("Isaac", "Newton", "i.newton@cpro.edu", 8593705989, "3pass21", 3),
            ("Carly", "Nickles", "c.nickles@cpro.edu", 5737894321, "pa123ss", 2),
            ("Gwen", "Stacey", "g.stacey@cpro.edu", 5736093383, "p456ass", 1),
            ("Joe", "Mama", "j.mama@cpro.edu", 8593215609, "pa456ss", 1),
            ("Mary", "Jane", "m.jane@cpro.edu", 5734837719, "6pass54", 2),
            ("Shawn", "Knight", "s.knight@cpro.edu", 859458989, "45pass6", 1),
            ("Steffany", "Lacy", "s.lacy@cpro.edu", 5736714812, "12pass3", 3),
            ("Greg", "Jones", "g.jones@cpro.edu", 8598937081, "789pass", 3)]

        db.session.bulk_save_objects(user_list)
        db.session.commit()
"""
class UserPermissions(enum.Enum):
    admin = 0
    student = 1
    teacher = 3
    parent = 4

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    phone_number = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(20))
    permissions = db.Column(db.Integer, None)
    courses = db.relationship('Course')  # When a class is added, this field will store the Courses.id

    """
    We want to be able to choose a user and be able to see all of their notes.
    To do this we need to add a notes field and add a relationship to the Note table.
    This will add the note (which includes all of the information of the 
    different fields in the notes database - id, data, date, user_id) to the user's profile 
    everytime they create a note which will allow us to find the note easier.
    """


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100))
    teacher = db.Column(db.String(50))
    year = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # The second 'user.id' is referencing the User table - matching it to 'user_id' in the courses table

    """
    We need to create a relationship between a course and the user who is enrolled.
    We can do this using a FOREIGN KEY. A foreign key is basically a column of a database
    tha always references a columns from another database.
    In this instance, for every course, we need to store the user who is enrolled in it.
    """

class Grades(db.Model):
    course_id = db.Column(db.Integer, primary_key=True)
    assignment_name = db.Column(db.String(50))
    date_assigned = db.Column(db.DateTime(timezone=True), default=func.now())
    date_due = db.Column(db.DateTime(timezone=True))
    grade = db.Column(db.Integer)
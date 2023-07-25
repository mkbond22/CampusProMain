
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
#from sqlalchemy import insert


#######################################################################
"""
USER REQUIREMENTS:
 - FirstName
 - LastName
 - Address
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
                    ("Mary", "Poppins", "m.poppins@cpro.edu", 5734814889, "456pass", 2),
                    ("Isaac", "Newton", "i.newton@cpro.edu", 8593705989, "3pass21", 3),
                    ("Jon", "Snow", "j.snow@cpro.edu", 8591230956, "p123ass", 1),
                    ("Carly", "Nickles", "c.nickles@cpro.edu", 5737894321, "pa123ss", 2),
                    ("Gwen", "Stacey", "g.stacey@cpro.edu", 5736093383, "p456ass", 1),
                    ("Joe", "Mama", "j.mama@cpro.edu", 8593215609, "pa456ss", 1),
                    ("Mary", "Jane", "m.jane@cpro.edu", 5734837719, "6pass54", 2),
                    ("Shawn", "Knight", "s.knight@cpro.edu", 859458989, "45pass6", 1),
                    ("Steffany", "Lacy", "s.lacy@cpro.edu", 5736714812, "12pass3", 3),
                    ("Jen", "Morris", "j.morris@cpro.edu", 5731672184, "pass123word", 3),
                    ("Greg", "Jones", "g.jones@cpro.edu", 8598937081, "789pass", 3)]

        # user1 = User(first_name="Tyler", last_name="Selby", address="12233 Eagle Ridge", 
        #                 city="Walton", zip_code=41094, state="KY", email="t.selby@cpro.edu", 
        #                 phone_number=8598018793, 
        #                 password=generate_password_hash("123pass", method='sha256'), 
        #                 permissions=0)
        # user2 = User(first_name="Megan", last_name="Bond", address="1234 Megan's Lane", 
        #                 city="Cape Girardeau", zip_code=63701, state="MO", email="m.bond@cpro.edu", 
        #                 phone_number=5734292338, 
        #                 password=generate_password_hash("456pass", method='sha256'), 
        #                 permissions=0)
        # user3 = User(first_name="Jim", last_name="Beam", address="555 Jim Avenue", 
        #                 city="Smalltown", zip_code=19091, state="AZ", email="j.beam@cpro.edu", 
        #                 phone_number=8593751289, 
        #                 password=generate_password_hash("pass456", method='sha256'), 
        #                 permissions=1)
        # user4 = User(first_name="Mary", last_name="Poppins", address="11 Umbrella Street", 
        #                 city="Poppinsville", zip_code=24923, state="MN", email="m.poppins@cpro.edu", 
        #                 phone_number=5734814889, 
        #                 password=generate_password_hash("456pass", method='sha256'), 
        #                 permissions=2)
        # user5 = User(first_name="Isaac", last_name="Newton", address="123 Gravity Street", 
        #                 city="ScienceVille", zip_code=65894, state="NJ", email="i.newton@cpro.edu", 
        #                 phone_number=8593705989, 
        #                 password=generate_password_hash("3pass21", method='sha256'), 
        #                 permissions=3)
        # db.session.add(user1)
        # db.session.add(user2)
        # db.session.add(user3)
        # db.session.add(user4)
        # db.session.add(user5)
        db.session.commit()
"""

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    zip_code = db.Column(db.Integer, nullable=False)
    state = db.Column(db.String(50))
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone_number = db.Column(db.String(15), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    permissions = db.Column(db.Integer, None)
    courses = db.relationship('Course')  # When a class is added, this field will store the Courses.id

    """
    We want to be able to choose a user and be able to see all of their notes.
    To do this we need to add a notes field and add a relationship to the Note table.
    This will add the note (which includes all of the information of the 
    different fields in the notes database - id, data, date, user_id) to the user's profile 
    everytime they create a note which will allow us to find the note easier.
    """

"""
COURSE_CODES AND SECTIONS (all classes will have at least sections A, B, C, and possibly more if needed):

~Freshman Math:
   - FRMA-A
   - FRMA-B
   - FRMA-C
~Freshman Science:
   - FRSC-A
   - FRSC-B
   - FRSC-C

~Sophomore Math:
   - SOMA-A
   - SOMA-B
   - SOMA-C

~Junior Math:
   - JRMA-A
   - JRMA-B
   - JRMA-C

~Senior Math:
   - SRMA-A
   - SRMA-B
   - SRMA-C

    # abbr = "FREN"
    # sec = "C"
    # courseCode = (f"{abbr}-{sec}").upper()

    # course1 = Course(course_name="Algebra I", course_abbr="FRMA", 
    #                 section="A", course_code= courseCode, 
    #                 teacher="Mary Poppins", year="2023-2024")
    # course2 = Course(course_name="Algebra I", course_abbr="FRMA",
    #               section="B", course_code= courseCode, 
    #               teacher="Carl Gauss", year="2023-2024")
    # course3 = Course(course_name="Geometry", course_abbr="SOMA", 
    #               section="A", course_code= courseCode, 
    #               teacher="Carly Nickles", year="2023-2024")
    # course4 = Course(course_name="Trigonometry", course_abbr="JRMA", 
    #               section="A", course_code= courseCode, 
    #               teacher="Mary Jane", year="2023-2024")
    # course5 = Course(course_name="Calculus I", course_abbr="SRMA", 
    #               section="A", course_code= courseCode, 
    #               teacher="Samos Pythagoras", year="2023-2024")
    # course6 = Course(course_name="English I", course_abbr="FREN", 
    #               section="C", course_code= courseCode, 
    #               teacher="George Orwell", year="2023-2024")

    # db.session.add(course1)
    # db.session.add(course2)
    # db.session.add(course3)
    # db.session.add(course4)
    # db.session.add(course5)
    # db.session.add(course6)
"""

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(50))
    course_abbr = db.Column(db.String(10))
    section = db.Column(db.String)                          # SUFFIX TO BE JOINED WITH COURSE_ABBR (A, B, C)
    course_code = db.Column(db.String(20), unique=True)     # Unique value in an f-string -- "course_abbr-section"
    #description = db.Column(db.String(100)) #DELETE COLUMN
    teacher = db.Column(db.String(50))
    #year = db.Column(db.DateTime(timezone=True), default=func.now())
    year = db.Column(db.String(20)) # EX. 2023-2024 SINCE SCHOOL YEAR GOES FROM AUGUST-MAY
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




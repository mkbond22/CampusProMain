
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import date
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
"CREATE TABLE Users (id int PRIMARY KEY AUTO_INCREMENT, 
                    first_name VARCHAR(50), 
                    last_name VARCHAR(50), 
                    email VARCHAR(100), 
                    phone_number int, 
                    passwd VARCHAR(50), 
                    permissions ENUM('0', '1', '2', '3')
                    )"
            
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

"""
#######################################################################

#~~~~~~~~~~WE HAVE TO PUT THE MANY-TO-MANY TABLES AT THE TOP SO WE DONT GET AN ERROR WITH THE SECONDARY

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
"""
Need to create a relationship table for "CourseStudents(db.Model)"

   ~~FILTER COURSES TO FIND THE COURSE WE WANT TO FORM A RELATIONSHIP WITH
        course = Course.query.filter(Course.id == 1).first()

   ~~FILTER USERS TO FIND THE USER WE WANT TO FORM A RELATIONSHIP WITH
        user = User.query.filter(User.id == 3).first()

   ~~
        user.current_courses.append(course)
        db.session.commit()

"""
user_course = db.Table('user_course',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'))
)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
"""
Need to create a relationship table for ""AssignmentStudents(db.Model)""
"""
# class AssignmentsStudents(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    assignment_name = db.Column(db.String(50))


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
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
    current_courses = db.relationship('Course', secondary=user_course, backref='enrolled_students')  # When a class is added, this field will store the Courses.id


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
"""
COURSE_CODES AND SECTIONS

~ex: Freshman Math section A:
   - FRMA-A
~ex: Sophomore English section C:
   - SOEN-C


Courses could be a many-to-many relationship because a course can 
have many students, and a student can have many courses.

A course could also have a one-to-many relationship with Assignments because
a course can have many assignments.

Will need to create a relationship database 
"CourseStudents(db.Model)"

A student should have a relationship with a course
   -> Each

"""
class Course(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   course_name = db.Column(db.String(50))
   course_abbr = db.Column(db.String(10))
   section = db.Column(db.String)                          # SUFFIX TO BE JOINED WITH COURSE_ABBR (A, B, C)
   course_code = db.Column(db.String(20), unique=True)     # Unique value in an f-string -- "course_abbr-section"
   teacher = db.Column(db.String(50))
   year = db.Column(db.String(20)) # EX. 2023-2024 SINCE SCHOOL YEAR GOES FROM AUGUST-MAY
   total_grade = db.Column(db.String(5), nullable=True)    # Will need some logic to calculate(get values for each User.Assignments.grade / number of assignmnets)
   assignments = db.relationship('Assignment', backref='course') #Creates the invisible "course" column in the Assignment table
                                                                 #Add "course=course_code" when adding an assignment

   
   #user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # The second 'user.id' is referencing the User table - matching it to 'user_id' in the courses table


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
"""
Assigmnets could be a many-to-many relationship because an assigment can 
have many students, and a student can have many assigments.

Assignments could also have a many-to-one relationship with Courses because
a course can have many assignments - so we could have a foreign key for that
in addition to the third table.

Will need to create a relationship database 
"AssignmentStudents(db.Model)"

**IMPORTANT**
   WHEN ADDING AN ASSIGNMENT WITH A COURSE-RELATIONSHIP, THE ForeignKey MUST
   BE IN THE FORM OF THE COURSE OBJECT
      ex:
         course = Course.query.filter().first()
         assignment2 = Assignment(assignment_creator="Jon Snow", assignment_name="Another Assignment", 
                        date_due=d, grade="-", course=course)
      
   ~~The .first() query method return the entire instance of the course object.
   ~~So we would then need to use .filter(Course.course_code == "FRMA-A") to find the instance
     with the correct course_code since "course_code" is a unique value

"""
class Assignment(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   assignment_creator =db.Column(db.String(50))
   assignment_name = db.Column(db.String(50))
   date_assigned = db.Column(db.Date(), default=func.current_date())
   date_due = db.Column(db.Date())
   grade = db.Column(db.String, None)
   course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
   submission = db.relationship('Submission', backref='assignment') #Creates the invisible "assignment" column in the submission table
                                                                    #Add "assignment=assignment_name" when adding a submission


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
"""
Submissions should be a one-to-one relationship since one assigment gets one attempt
"""
class Submission(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   filename = db.Column(db.String(100))
   date_submitted = db.Column(db.Date(), default=func.current_date())
   assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'))


   #Files should be stored in a file system or a service like S3
   #The metadata of the file should be stored in the database
   #data = db.Column(db.LargeBinary)



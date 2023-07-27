from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

#from flask_wtf import FlaskForm
#from wtforms import StringField, SubmitField
#from wtforms.validators import DataRequired
from os import path
from flask_login import LoginManager
#import mysql.connector

# new_db = mysql.connector.connect(host="localhost", user="root", passwd="$C0de1sco0L!", database="testdatabase")
# app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://root:$C0de1sco0L!@localhost/testdatabase'

db = SQLAlchemy()
DB_NAME = "database.db"


# Create a Flask Instance
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dj3!8rn*-q87b5mg$f0'

    # OLD DATABASE
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    
    # INITIALIZE THE DATABASE BY PASSING IT OUR APP
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Course
    # from .sql_db import Users

    with app.app_context():

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

        # abbr = "FREN"
        # sec = "C"
        # courseCode = (f"{abbr}-{sec}")

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

        # db.session.commit()

        # query = User.query.all()
        # print(query)
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'authentication.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


    return app


# def create_database(app):
#     if not path.exists('website/' + DB_NAME):
#         db.create_all(app=app)
#         print('Created Database!')

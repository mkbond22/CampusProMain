from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)


"""
ive app url
https://campuspro.onrender.com

FLASK COMMANDS:
~Run app
    py -m flask --app main run
~Initialize db
    py -m flask --app main db init
~Migrate
    py -m flask --app main db migrate
~Run upgrade/downgrade
    py -m flask --app main db upgrade

ADDING DB OBJECTS FROM VS TERMINAL:

>>py
>>from website.models import User, Course
"""

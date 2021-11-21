from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from os import getenv, path

from .views.views import views
from .views.auth import auth

app = Flask(__name__, instance_relative_config=True)

load_dotenv()
DB_CREDENTIALS = getenv('DB_CREDENTIALS')

print("OS", getenv('DB_CREDENTIALS'))


app.debug = True
app.config['SECRET_KEY'] = 'SECRET_KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DB_CREDENTIALS}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


app.register_blueprint(views, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')

from .models.department import Department
from .models.employee import Employee


def create_database(app):
    load_dotenv()
    if not path.exists('website/' + str(DB_CREDENTIALS)):
        db.create_all(app=app)
        print('Created Database!', DB_CREDENTIALS)


create_database(app)

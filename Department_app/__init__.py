from dotenv import load_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from os import getenv, path

app = Flask(__name__, instance_relative_config=True)

load_dotenv()
DB_CREDENTIALS = getenv('DB_CREDENTIALS')

app.debug = True
app.config['SECRET_KEY'] = 'SECRET_KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DB_CREDENTIALS}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# app.register_blueprint(routes, url_prefix='/')


def create_database():
    load_dotenv()
    if not path.exists('website/' + str(DB_CREDENTIALS)):
        # from .models import Department, Employee
        db.create_all()
        print('Created Database!')


create_database()


bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page_view"
login_manager.login_message_category = "info"

from . import routes

